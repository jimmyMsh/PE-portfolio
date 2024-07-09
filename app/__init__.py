import os
from flask import Flask, render_template, request, url_for
from dotenv import load_dotenv
from peewee import *

load_dotenv()
app = Flask(__name__)

db_host = os.getenv('MYSQL_HOST')
db_user = os.getenv('MYSQL_USER')
db_password = os.getenv('MYSQL_PASSWORD')
db_name = os.getenv('MYSQL_DB')

mydb = MySQLDatabase(db_name,
    user=db_user,
    password=db_password,
    host=db_host,
    port=3306
)

print(mydb)

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

if __name__ == '__main__':
    app.run(debug=True)
