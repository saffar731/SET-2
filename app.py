import os
from flask import Flask, render_template, request, redirect, url_for
from vercel_blob import put, list, delete

app = Flask(__name__)

STORAGE_LIMIT_GB = 100000

@app.route('/')
def index():
    try:
        response = list()
        blobs = response.get('blobs', [])
        
        # Group files by their top-level folder name
        folders = {}
        total_bytes = 0
        
        for blob in blobs:
            total_bytes += blob['size']
            # Get the top folder name from the path
            parts = blob['pathname'].split('/')
            folder_name = parts[0] if len(parts) > 1 else "Root Files"
            
            if folder_name not in folders:
                folders[folder_name] = []
            folders[folder_name].append(blob)

        used_gb = round(total_bytes / (1024**3), 6)
        percent = round((used_gb / STORAGE_LIMIT_GB) * 100, 4)
    except Exception as e:
        print(f"Error: {e}")
        folders, used_gb, percent = {}, 0, 0
    
    return render_template('index.html', folders=folders, used_gb=used_gb, percent=percent)

@app.route('/upload', methods=['POST'])
def upload_file():
    files = request.files.getlist("file")
    for file in files:
        if file.filename:
            # The filename here includes the folder path from the webkitRelativePath
            put(file.filename, file.read(), {'access': 'public'})
    return redirect(url_for('index'))

@app.route('/delete_folder/<path:folder_prefix>')
def delete_folder(folder_prefix):
    # To delete a "folder", we delete all blobs starting with that prefix
    response = list()
    for blob in response.get('blobs', []):
        if blob['pathname'].startswith(folder_prefix):
            delete(blob['url'])
    return redirect(url_for('index'))
