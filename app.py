import os
import shutil
import urllib.parse
from flask import Flask, render_template, request, redirect, url_for, send_from_directory, abort

app = Flask(__name__)
# Vercel temporary storage
UPLOAD_FOLDER = '/tmp/project_files'

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/')
def index():
    items = []
    if os.path.exists(UPLOAD_FOLDER):
        for name in os.listdir(UPLOAD_FOLDER):
            if not name.endswith('.zip'):
                path = os.path.join(UPLOAD_FOLDER, name)
                items.append({'name': name, 'is_dir': os.path.isdir(path)})
    return render_template('index.html', items=items)

@app.route('/upload', methods=['POST'])
def upload_file():
    files = request.files.getlist("file")
    for file in files:
        if file.filename:
            file_path = os.path.join(UPLOAD_FOLDER, file.filename)
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            file.save(file_path)
    return redirect(url_for('index'))

@app.route('/download/<path:filename>')
def download_item(filename):
    decoded_name = urllib.parse.unquote(filename)
    full_path = os.path.join(UPLOAD_FOLDER, decoded_name)
    
    if not os.path.exists(full_path):
        return f"File {decoded_name} not found.", 404
    
    if os.path.isdir(full_path):
        safe_zip_name = decoded_name.replace(" ", "_")
        zip_base = os.path.join(UPLOAD_FOLDER, safe_zip_name)
        archive_path = shutil.make_archive(zip_base, 'zip', full_path)
        return send_from_directory(UPLOAD_FOLDER, os.path.basename(archive_path), as_attachment=True)
    
    return send_from_directory(UPLOAD_FOLDER, decoded_name, as_attachment=True)
