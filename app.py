import os
import shutil
from flask import Flask, render_template, request, redirect, url_for, send_from_directory

app = Flask(__name__)
UPLOAD_FOLDER = 'project_files'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Ensure the upload directory exists
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

@app.route('/')
def index():
    items = []
    if os.path.exists(UPLOAD_FOLDER):
        for name in os.listdir(UPLOAD_FOLDER):
            path = os.path.join(UPLOAD_FOLDER, name)
            items.append({
                'name': name, 
                'is_dir': os.path.isdir(path)
            })
    return render_template('index.html', items=items)

@app.route('/upload', methods=['POST'])
def upload_file():
    uploaded_files = request.files.getlist("file")
    for file in uploaded_files:
        if file.filename != '':
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            # Create subfolders if a directory was uploaded
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            file.save(file_path)
    return redirect(url_for('index'))

@app.route('/download/<path:filename>')
def download_item(filename):
    full_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    
    # If the user tries to download a folder, zip it first
    if os.path.isdir(full_path):
        zip_path = shutil.make_archive(full_path, 'zip', full_path)
        return send_from_directory(app.config['UPLOAD_FOLDER'], os.path.basename(zip_path), as_attachment=True)
    
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)