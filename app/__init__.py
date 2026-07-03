import os
from flask import Flask, render_template, request
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)

@app.context_processor
def inject_pages():
    return dict(pages=[
        {"name": "Home", "endpoint": "index"},
        {"name": "Hobbies", "endpoint": "index2"}
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