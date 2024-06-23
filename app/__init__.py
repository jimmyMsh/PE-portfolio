import os
from flask import Flask, render_template, request
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html', title="MLH Fellow", url=os.getenv("URL"), active_page = 'home', mapsApiKey=os.getenv("MAPS_API_KEY"))

@app.route('/about')
def about():
    return render_template('about.html', title="About Me", active_page = 'about')

@app.route('/work')
def work():
    return render_template('work.html', title="Work Experience", active_page = 'work')

@app.route('/projects')
def projects():
    return render_template('projects.html', title="projects", active_page = 'projects')

@app.route('/contact')
def contact():
    return render_template('contact.html', title="Contact", active_page = 'contact')

if __name__ == '__main__':
    app.run(debug=True)
