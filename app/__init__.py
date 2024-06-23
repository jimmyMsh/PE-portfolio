import os
from flask import Flask, render_template, request
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html', title="MLH Fellow", url=os.getenv("URL"))

@app.route('/about')
def about():
    return render_template('about.html', title="About Me")

@app.route('/work')
def work():
    return render_template('work.html', title="Work Experience")

@app.route('/hobbies')
def hobbies():
    return render_template('hobbies.html', title="Hobbies")

@app.route('/education')
def education():
    return render_template('education.html', title="Education")

@app.route('/contact')
def contact():
    return render_template('contact.html', title="Contact")

if __name__ == '__main__':
    app.run(debug=True)