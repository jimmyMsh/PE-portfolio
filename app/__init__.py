import os
from flask import Flask, render_template, request, url_for, jsonify, redirect
from dotenv import load_dotenv
from peewee import *
import datetime
from playhouse.shortcuts import model_to_dict
import requests
import json

load_dotenv()
app = Flask(__name__)
app.config['DEBUG'] = True

db_host = os.getenv('MYSQL_HOST')
db_user = os.getenv('MYSQL_USER')
db_password = os.getenv('MYSQL_PASSWORD')
db_name = os.getenv('MYSQL_DATABASE')

# Initializing mydb with a temporary in-memory sqlite database for testing
if os.getenv("TESTING") == 'true':
    print("Running in test mode")
    mydb = SqliteDatabase('file:memory?mode=memory&cache=shared', uri=True)
else:
    mydb = MySQLDatabase(db_name,
        user=db_user,
        password=db_password,
        host=db_host,
        port=3306
    )

print(mydb)

# Create DB model that reflects fields for timeline posts
class TimelinePost(Model):
    name = CharField()
    email = CharField()
    content = TextField()
    created_at = DateTimeField(default=datetime.datetime.now)
    
    class Meta:
        database = mydb

# Connect to db
mydb.connect()
# Add the above defined table
mydb.create_tables([TimelinePost])

# Formats the datetime so that it is consistent on template page
@app.template_filter('format_datetime')
def format_datetime(value):
    if value is None:
        return ""
    return value.strftime('%Y-%m-%d %H:%M:%S')

# Helper function to create a hash of the email so that it could be used to fetch the emails
@app.template_filter('to_md5')
def to_md5_filter(email):
    import hashlib
    result = hashlib.md5(email.strip().lower().encode('utf-8')).hexdigest()
    return result

# ------------------------------ API endpoint definitions ------------------------------
@app.route('/api/health')
def check_website_health():
    # Load API key
    TEST_HEALTH_CHECK_API_KEY = os.getenv('TEST_HEALTH_CHECK_API_KEY')
    # Check for API key to use this header
    if request.headers.get('Testing-API-Key') != TEST_HEALTH_CHECK_API_KEY:
        return "Invalid Request", 403 # Forbidden
    
    # Otherwise, create return JSON for the status of the web health
    status = {
        'template_rendering' : 'Healthy',
        'database_connection' : 'Healthy',
        'db_write_delete' : 'Healthy'
    }
    
    # Test the if the main page template can render
    try:
        render_template('index.html')
    except Exception as e:
        status['template_rendering'] = f'Unhealthy: {str(e)}'
    
    # Next, test if we the database is responsive
    try:
        TimelinePost.select().limit(1).execute()
    except Exception as e:
        status['database_connection'] = f'Unhealthy: {str(e)}'
        
    try:
        test_post = TimelinePost.create(name = 'Jimmy', email = 'Jim@test.com', content = 'Some test content')
        test_post.delete_instance()
    except Exception as e:
        status['db_write_delete'] = f'Unhealthy: {str(e)}'
        
    # Generate error status code if either test failed. 
    status_code = 200 if all(response == "Healthy" for response in status.values()) else 500
    
    return status, status_code 
        
@app.route('/api/timeline_post', methods=['POST'])
def post_time_line_post():
    # Retrieve form data and validate
    name = request.form.get('name')
    email = request.form.get('email')
    content = request.form.get('content')

    # Validate 'name' to ensure it is not empty
    if not name:
        return "Invalid name", 400

    # Validate 'email' to check for presence and basic format
    if not email or '@' not in email:
        return "invalid email", 400  

    # Validate 'content' to ensure it is not empty
    if not content:
        return "Invalid content", 400
    
    # Create a new TimelinePost record in the database with the retrieved form data
    timeline_post = TimelinePost.create(name = name, email = email, content = content)
    
    # Convert the created TimelinePost model instance to a dictionary and return it as the response
    return model_to_dict(timeline_post)

@app.route('/api/timeline_post', methods=['GET'])
def get_time_line_post():
    return {
    'timeline_posts':
        [
             # Fetch all TimelinePost records from the database, ordered by 'created_at' in descending order
            model_to_dict(p) for p in TimelinePost.select().order_by(TimelinePost.created_at.desc())
        ]
    }

@app.route('/api/timeline_post/<int:post_id>', methods = ['DELETE'])
def delete_time_line_post(post_id):
    try:
        # Attempt to get post by ID
        post = TimelinePost.get_by_id(post_id)
        # If found, delete the post
        post.delete_instance()
        # Return a message with the status code 200
        return jsonify({'message': 'Timeline post deleted successfully'}), 200
    except TimelinePost.DoesNotExist:
        # If the post does not exist, return an error message with status code 404
        return jsonify({'error': 'Timeline post not found'}), 404

# ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^ API endpoint definitions ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

@app.route('/')
def index():
    return render_template('index.html', title="Home", url=os.getenv("URL"), active_page = 'home')

@app.route('/about')
def about():
    return render_template('about.html', title="About Me", active_page='about')

@app.route('/work')
def work():
    with open('app/static/files/work_experiences.json', 'r') as f:
        work_experiences = json.load(f)  # Load data from JSON file
        
    return render_template('work.html', title="Work Experience", active_page='work', work_experiences=work_experiences)

@app.route('/projects')
def projects():
    # Fetch repository data from GitHub API
    response = requests.get("https://api.github.com/users/jimmyMsh/repos")
    
    if response.status_code == 200:
        github_projects = response.json()
        projects = [
            {
                "title": repo["name"],
                "description": repo["description"] or "No description available.",
                "github_url": repo["html_url"],
                "updated_at": datetime.datetime.strptime(repo["updated_at"], "%Y-%m-%dT%H:%M:%SZ").strftime("%B %d, %Y"),
                "tech": ", ".join(repo.get("topics", []))
            }
            for repo in github_projects
        ]
    else:
        projects = []  # Fallback in case the API fails
    
    # Order the projects by last updated date (most recent first)
    projects.sort(key=lambda x: datetime.datetime.strptime(x["updated_at"], "%B %d, %Y"), reverse=True)

    return render_template('projects.html', title="Projects", active_page='projects', projects=projects)

@app.route('/contact')
def contact():
    return render_template('contact.html', title="Contact", active_page = 'contact')

@app.route('/timeline', methods=['GET', 'POST'])
def timeline():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        content = request.form['content']
        
        TimelinePost.create(name=name, email=email, content=content)
        
        return redirect(url_for('timeline'))

    timeline_posts = [model_to_dict(p) for p in TimelinePost.select().order_by(TimelinePost.created_at.desc())]
    return render_template('timeline.html', title="Timeline", active_page='timeline', timeline_posts=timeline_posts)

if __name__ == '__main__':
    app.run(debug=True)
