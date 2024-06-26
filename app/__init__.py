import os
from flask import Flask, render_template, request, url_for
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html', title="MLH Fellow", url=os.getenv("URL"), active_page = 'home', mapsApiKey=os.getenv("MAPS_API_KEY"))

@app.route('/about')
def about():
    hobbies = [
        {"name": "Working out", "description": "Love to workout ", "img_url": url_for('static', filename='img/gym.jpg')},
        {"name": "Traveling", "description": "Exploring new places, especially around the city", "img_url": url_for('static', filename='img/traveling.jpg')},
        {"name": "Eating out", "description": "Trying different restaurant cuisines", "img_url": url_for('static', filename='img/restaurant.jpg')},
        {"name": "Programing", "description": "Learning new programing concepts!", "img_url": url_for('static', filename='img/Programing.jpg')},
    ]
    
    # If you prefer a separate loop for adding URLs, use the following:
    # for hobby in hobbies:
    #     hobby['img_url'] = url_for('static', filename='img/' + hobby['img'])
    
    return render_template('about.html', title="About Me", active_page = 'about', hobbies = hobbies)

@app.route('/work')
def work():
    work_experiences = [
        {
            "role": "Role Name",
            "company": "Company Name",
            "description": "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.",
            "dates": "June 2024 - Present",
            "link": "http://www.google.com",
            "img_url": url_for('static', filename='img/logo.jpg')
        },
        {
            "role": "Role Name",
            "company": "Company Name",
            "description": "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.",
            "dates": "June 2024 - Present",
            "link": "http://www.google.com",
            "img_url": url_for('static', filename='img/logo.jpg')
        },
        {
            "role": "Role Name",
            "company": "Company Name",
            "description": "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.",
            "dates": "June 2024 - Present",
            "link": "http://www.google.com",
            "img_url": url_for('static', filename='img/logo.jpg')
        }
    ] 
    
    return render_template('work.html', title="Work Experience", active_page = 'work', work_experiences=work_experiences)

@app.route('/projects')
def projects():
    return render_template('projects.html', title="projects", active_page = 'projects')

@app.route('/contact')
def contact():
    return render_template('contact.html', title="Contact", active_page = 'contact')

if __name__ == '__main__':
    app.run(debug=True)
