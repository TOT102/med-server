from flask import request, render_template, jsonify, flash, url_for, redirect, send_file, send_from_directory
from flask import Blueprint
from werkzeug.utils import secure_filename
import os
import json
#from app import parser
from app.parser import parse_pdf
from datetime import datetime

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
@routes.route('/download-latest')
def download_latest():
    try:
        pdf_files = [f for f in os.listdir(UPLOAD_FOLDER) if f.lower().endswith('.pdf')]

        if not pdf_files:
            flash("No PDF reports found.")
            return redirect(url_for('routes.index'))

        # 'DDMMYYYY.pdf'
        def extract_date(filename):
            try:
                base = os.path.splitext(filename)[0]
                return datetime.strptime(base, "%d%m%Y")
            except ValueError:
                return datetime.min 

        latest_file = max(pdf_files, key=extract_date)
        latest_file_path = os.path.join(UPLOAD_FOLDER, latest_file)

        return send_file(latest_file_path, as_attachment=True)

    except Exception as e:
        flash(f"Error downloading file: {e}")
        return redirect(url_for('routes.index'))

@routes.route('/list-reports')
def list_reports():
    try:
        pdf_files = [f for f in os.listdir(UPLOAD_FOLDER) if f.lower().endswith('.pdf')]

        def extract_date(filename):
            try:
                return datetime.strptime(os.path.splitext(filename)[0], "%d%m%Y")
            except ValueError:
                return datetime.min

        pdf_files.sort(key=extract_date, reverse=True)

        # Pass list to template
        return render_template('list_reports.html', files=pdf_files)

    except Exception as e:
        flash(f"Error listing reports: {e}")
        return redirect(url_for('routes.index'))

@routes.route('/download/<filename>')
def download_file(filename):
    file_path = os.path.join(UPLOAD_FOLDER, filename)
    if os.path.exists(file_path):
        return send_file(file_path, as_attachment=True)
    else:
        flash("File not found.")
        return redirect(url_for('routes.list_reports'))
    
# @routes.route('/chart-data/<indicator>')
# def chart_data(indicator):
#     indicator_data = []
    
#     for filename in sorted(os.listdir(OUTPUT_FOLDER)):
#         if filename.endswith('.json'):
#             date = filename.replace('.json', '') 
#             filepath = os.path.join(OUTPUT_FOLDER, filename)
#             with open(filepath, 'r', encoding='utf-8') as f:
#                 data = json.load(f)

#                 for category in data.values():
#                     for entry in category:
#                         if entry["indicator"] == indicator:
#                             indicator_data.append({
#                                 "date": f"{date[4:]}-{date[2:4]}-{date[:2]}",
#                                 "value": entry["value"]
#                             })

#     return jsonify(indicator_data)

@routes.route('/indicators')
def get_indicators():
    indicators = set()
    for filename in os.listdir(OUTPUT_FOLDER):
        if filename.endswith('.json'):
            with open(os.path.join(OUTPUT_FOLDER, filename), encoding='utf-8') as f:
                data = json.load(f)
                for category in data.values():
                    for entry in category:
                        indicators.add(entry['indicator'])
    return jsonify(sorted(indicators))

@routes.route('/chart-data')
def chart_data():
    indicator = request.args.get('indicator')
    indicator_data = []

    for filename in sorted(os.listdir(OUTPUT_FOLDER)):
        if filename.endswith('.json'):
            date = filename.replace('.json', '')
            with open(os.path.join(OUTPUT_FOLDER, filename), encoding='utf-8') as f:
                data = json.load(f)
                for category in data.values():
                    for entry in category:
                        if entry['indicator'] == indicator:
                            indicator_data.append({
                                "date": f"{date[4:]}-{date[2:4]}-{date[:2]}",
                                "value": entry["value"]
                            })

    return jsonify(indicator_data)

@routes.route("/get-min")
def get_min():
    indicator = request.args.get("indicator")
    indicator_data = []

    for filename in sorted(os.listdir(OUTPUT_FOLDER)):
        if filename.endswith('.json'):
            date = filename.replace('.json', '')
            with open(os.path.join(OUTPUT_FOLDER, filename), encoding='utf-8') as f:
                data = json.load(f)
                for category in data.values():
                    for entry in category:
                        if entry['indicator'] == indicator:
                            indicator_data.append(entry["value"])
                            
    return jsonify(min(indicator_data))

@routes.route("/get-max")
def get_max():
    indicator = request.args.get("indicator")
    indicator_data = []

    for filename in sorted(os.listdir(OUTPUT_FOLDER)):
        if filename.endswith('.json'):
            date = filename.replace('.json', '')
            with open(os.path.join(OUTPUT_FOLDER, filename), encoding='utf-8') as f:
                data = json.load(f)
                for category in data.values():
                    for entry in category:
                        if entry['indicator'] == indicator:
                            indicator_data.append(entry["value"])
                            
    return jsonify(max(indicator_data))

@routes.route("/get-avg")
def get_avg():
    indicator = request.args.get("indicator")
    indicator_data = []

    for filename in sorted(os.listdir(OUTPUT_FOLDER)):
        if filename.endswith('.json'):
            date = filename.replace('.json', '')
            with open(os.path.join(OUTPUT_FOLDER, filename), encoding='utf-8') as f:
                data = json.load(f)
                for category in data.values():
                    for entry in category:
                        if entry['indicator'] == indicator:
                            indicator_data.append(entry["value"])

    indicator_avg = sum(indicator_data)/len(indicator_data)                   
    return jsonify(indicator_avg)