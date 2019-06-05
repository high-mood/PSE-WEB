from flask import send_from_directory, jsonify, json, render_template, redirect, request, session,flash
from app import app
from app import db
# Refactor later
from app import models




@app.route("/index", methods=['GET', 'POST'])
@app.route("/", methods=['GET', 'POST'])
def index():
    return "Hello World"
