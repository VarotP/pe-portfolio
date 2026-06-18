import os
from flask import Flask, render_template, request
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)


@app.route('/')
def index():
    
    return render_template('index.html', title="MLH Fellow", url=os.getenv("URL"), 
    work_experience = [
    {
        "name": "IFS Copperleaf",
        "title": "PlatOps-Coop",
        "description": "My first project.",
        "link": "https://example.com"
    },
    {
        "name": "Agoda (Booking Holdings)", 
        "title": "Infrastructure Intern",
        "description": "This is the content I just added.", 
        "link": "https://newproject.com"
    }],
    about_me = "As a fourth-year Computer Science student at the University of British Columbia, I’ve spent my time mastering the balance between clean code and creative problem-solving. Having completed internships in cloud infrastructure and AI, I specialize in building robust, scalable systems that solve complex problems. I believe the best technology is rooted in curiosity, a principle I carry into both my development projects and my work as a photographer.",
    )

@app.route('/hobbies')
def index2():
    return render_template('hobbies.html', title="Hobbies", hobbies = [
        {"name": "Piano",
         "pictures": [
             "./static/img/hobbies/piano.png",
             "./static/img/hobbies/piano2.jpeg"
         ]},
        {"name": "Photography",
         "pictures": [
             "./static/img/hobbies/photography.jpeg",
             "./static/img/hobbies/photography2.jpeg"
         ]},
        {"name": "Cooking",
         "pictures": [
             "./static/img/hobbies/cooking.jpeg",
             "./static/img/hobbies/cooking2.jpeg"
         ]},
         {"name": "Traveling",
         "pictures": [
             "./static/img/hobbies/countries.png"]}]
    )