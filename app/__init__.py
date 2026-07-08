import os
from flask import Flask, render_template, request
from dotenv import load_dotenv
from peewee import *
import datetime
from playhouse.shortcuts import model_to_dict 

load_dotenv()
app = Flask(__name__)

mydb = MySQLDatabase(os.getenv("MYSQL_DATABASE"),
                      host=os.getenv("MYSQL_HOST"),
                      user=os.getenv("MYSQL_USER"),
                      password=os.getenv("MYSQL_PASSWORD"),
                      port=3306)
print(mydb)

class TimelinePost(Model):
    name = CharField()
    email = CharField()
    content = TextField()
    created_at = DateTimeField(default=datetime.datetime.now)

    class Meta:
        database = mydb

mydb.connect()
mydb.create_tables([TimelinePost])

@app.context_processor
def inject_pages():
    return dict(pages=[
        {"name": "Home", "endpoint": "index"},
        {"name": "Hobbies", "endpoint": "index2"},
        {"name": "Timeline", "endpoint": "timeline"}
    ])

@app.context_processor
def inject_contact():
    return { "contact_email": "varotpava@gmail.com", "contact_phone": "+1 672-338-4317" }

@app.route('/')
def index():
    
    return render_template('index.html', title="MLH Fellow", url=os.getenv("URL"), 
    work_experience = [
    {
        "name": "IFS Copperleaf",
        "title": "Software Developer - PlatOps (Co-op)",
         "description": [
            "Designed and deployed cloud reverse proxy infrastructure across 10+ Azure regions with a multi-module Terraform IaC codebase (NGINXaaS, networking, Key Vault/SSL, monitoring) and a parameterized CI/CD pipeline, reducing deployment to a single pipeline run per environment.",
            "Hardened infrastructure security through NAT gateway outbound IP control, SDP-style NSG restrictions, and asystem-assigned managed identity for the TFSProxy service.",
        ],
    },
    {
        "name": "Agoda (Booking Holdings)",
        "title": "Infrastructure Intern",
         "description": [
            "Enabled real-time SSD utilization and power monitoring for 6,000+ ILO servers by extending Go-based scanning tools and building Grafana time-series dashboards (histograms, gauges, statistics).",
            "Improved predictive maintenance and reduced manual intervention for the infrastructure team.",
        ],
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

@app.route('/timeline')
def timeline():
    return render_template('timeline.html', title="Timeline")

@app.route('/api/timeline_post', methods=['POST'])
def post_time_line_post():
    name = request.form.get('name')
    email = request.form.get('email')
    content = request.form.get('content')
    timeline_post = TimelinePost.create(name=name, email=email, content=content)
    return model_to_dict(timeline_post)

@app.route('/api/timeline_post', methods=['GET'])
def get_time_line_post():
    return {
        'timeline_posts': [
            model_to_dict(p)
            for p in TimelinePost.select().order_by(TimelinePost.created_at.desc())
        ]
    }

@app.route('/api/timeline_post/<int:post_id>', methods=['DELETE'])
def delete_time_line_post(post_id):
    try:
        post = TimelinePost.get_by_id(post_id)
        post.delete_instance()
        return {'message': 'Timeline post deleted successfully'}
    except TimelinePost.DoesNotExist:
        return {'error': 'Timeline post not found'}, 404
    
