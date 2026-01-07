import os
import shutil
import zipfile
from flask import Flask, render_template, request, redirect, url_for, send_from_directory, abort, jsonify

app = Flask(__name__)
UPLOAD_FOLDER = '/tmp/project_files'

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

@app.route('/')
def index():
    items = []
    if os.path.exists(UPLOAD_FOLDER):
        for name in os.listdir(UPLOAD_FOLDER):
            if not name.endswith('.zip'): # Don't show temp zip files
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
    full_path = os.path.join(UPLOAD_FOLDER, filename)
    if not os.path.exists(full_path): abort(404)
    
    if os.path.isdir(full_path):
        zip_name = f"{filename}.zip"
        zip_path = os.path.join(UPLOAD_FOLDER, zip_name)
        # Create zip
        shutil.make_archive(os.path.join(UPLOAD_FOLDER, filename), 'zip', full_path)
        return send_from_directory(UPLOAD_FOLDER, zip_name, as_attachment=True)
    
    return send_from_directory(UPLOAD_FOLDER, filename, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
