import os
from flask import Flask, render_template, request, url_for, jsonify, redirect
from dotenv import load_dotenv
from peewee import *
import datetime
from playhouse.shortcuts import model_to_dict

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

    # Formatted as [latitude, longitude, description]
    # latitude: S is negative, longitude: W is negative
    locations = [
        [40.2442, -74.0296, "Ocean Township, NJ, USA - Hometown"],
        [40.8007, -73.7276, "Great Neck, NY, USA - Previously Lived"],
        [34.0522, -118.2437, "Los Angeles, CA, USA - Love to visit"],
        [40.4862, -74.4518, "New Brunswick, NJ, USA - Rutgers University"]
    ]

    return render_template('index.html', title="MLH Fellow", url=os.getenv("URL"), active_page = 'home', locations=locations)

@app.route('/about')
def about():
    return render_template('about.html', title="About Me", active_page='about')

@app.route('/work')
def work():
    work_experiences = [
        {
            "role": "Self Employed Personal Trainer",
            "company": "Jimmy Mishan Personal Training",
            "description": (
                "Launched and managed a personal training business, utilizing data analysis to track client progress "
                "and develop customized training plans. Effectively communicated with clients to set goals and provide progress updates. "
                "Used social media for client acquisition and maintained flexibility in scheduling."
            ),
            "dates": "Aug 2022 - Jan 2024",
            "link": "https://www.linkedin.com/in/jimmymishan/",
            "img_url": "https://picsum.photos/200/300"
        },
        {
            "role": "Information Technology Intern",
            "company": "New Jersey Courts (Supreme Court of NJ)",
            "description": (
                "Developed an asynchronous Node.js application for processing CSV and JSON files, improving data integrity "
                "and reducing manual data entry time by 50%. Initiated the development of a mobile attendance system using Ionic and Angular, "
                "and implemented data validation techniques to achieve 99.9% accuracy."
            ),
            "dates": "June 2024 - Present",
            "link": "https://www.njcourts.gov/",
            "img_url": "https://picsum.photos/200/300"
        },
        {
            "role": "Production Engineering Fellow",
            "company": "Meta (via MLH)",
            "description": (
                "Engineered and deployed a multi-component web application with Flask, MySQL, and NGINX, achieving 99% uptime. "
                "Developed Bash scripts for automated API endpoint testing and application updates. Containerized the application using Docker, "
                "reducing deployment time by 50% and improving scalability."
            ),
            "dates": "June 2024 - Present",
            "link": "https://fellowship.mlh.io/",
            "img_url": "https://picsum.photos/200/300"
        }
    ]

    return render_template('work.html', title="Work Experience", active_page = 'work', work_experiences=work_experiences)

@app.route('/projects')
def projects():

    projects = [
        {
            "title": "Prerequisite Checker",
            "description": "Java program for university course prerequisite analysis, potentially assisting students in identifying course prereqs and resolving class-related queries, showcasing data structures and graph theory application. Architected a DAG with adjacency lists for efficient course prerequisite modeling. Applied depth-first search and cycle detection algorithms for efficient graph traversal. Formulated file I/O strategies to enhance data accuracy and error resilience.",
            "github_url": "https://github.com/jimmyMsh/PreReqChecker"
        },
        {
            "title": "Personal Website",
            "description": "Engineered and deployed a sophisticated personal website that serves as a portfolio showcasing my software engineering abilities and web development expertise. Key features include interactive elements using DOM, CSS animations, and asynchronous JavaScript for real-time functionality. Integrated LinkedIn, GitHub, and Calendly for enhanced professional networking and scheduling.",
            "github_url": "https://jimmymishan.com/"
        },
        {
            "title": "Music Playlist Application",
            "description": "Created a Java application replicating streaming service operations with various features: Managed song sequences using circular linked lists for playlist navigation. Automated song library generation from CSV files for user-driven playlist customization. Implemented playlist manipulation capabilities, including merge, reverse, and shuffle functions, optimized by song popularity metrics to demonstrate intricate data structure utilization.",
            "github_url": "https://github.com/jimmyMsh/Data-Structures/tree/master/MusicPlaylist"
        }
    ]

    return render_template('projects.html', title="projects", active_page = 'projects', projects = projects)

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
