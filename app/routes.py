from flask import request, render_template, jsonify, flash, url_for, redirect
from flask import Blueprint
from werkzeug.utils import secure_filename
import os
import json
from app import parser
from app.parser import parse_pdf

# Create a Blueprint
routes = Blueprint('routes', __name__)

ALLOWED_EXTENSIONS = {'pdf'}

#Folder stuff
BASE_DIR = os.path.abspath(os.path.dirname(__file__))  # Path to routes.py
UPLOAD_FOLDER = os.path.join(BASE_DIR, 'uploads')
OUTPUT_FOLDER = os.path.join(BASE_DIR, 'output')

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Route: Home Page (frontend)
@routes.route('/')
def index():
    return render_template('index.html')

# Route: Upload (button on front end)
@routes.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']

        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        
        if file and allowed_file(file.filename): 
            filename = secure_filename(file.filename)
            file_path = os.path.join(UPLOAD_FOLDER, filename)
            print(f"Saving file to: {file_path}")
            file.save(file_path)

           # Run the parser and save JSON
            json_filename = os.path.splitext(filename)[0] + '.json'
            json_path = os.path.join(OUTPUT_FOLDER, json_filename)
            try:
                results = parse_pdf(file_path, output_json_path=json_path)
                flash('File successfully uploaded and parsed.')
            except Exception as e:
                flash(f'Error parsing PDF: {e}')
                return redirect(request.url)

            return redirect(url_for('routes.upload_file'))
        else:
            flash('Invalid file type. Only PDF files are allowed.')
            return redirect(request.url)

    # If GET request -> render simple upload frontend 
    return '''
    <!doctype html>
    <title>Upload PDF</title>
    <h1>Upload PDF File</h1>
    <form method=post enctype=multipart/form-data>
      <input type=file name=file accept="application/pdf">
      <input type=submit value=Upload>
    </form>
    '''



