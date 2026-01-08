import os
import io
import zipfile
import requests
from flask import Flask, render_template, request, redirect, url_for, send_file
from vercel_blob import put, list, delete

app = Flask(__name__)
STORAGE_LIMIT_GB = 100000

@app.route('/')
def index():
    try:
        response = list()
        blobs = response.get('blobs', [])
        folders = {}
        total_bytes = 0
        for blob in blobs:
            total_bytes += blob['size']
            parts = blob['pathname'].split('/')
            folder_name = parts[0] if len(parts) > 1 else "Root Files"
            if folder_name not in folders: folders[folder_name] = []
            folders[folder_name].append(blob)
        used_gb = round(total_bytes / (1024**3), 4)
        percent = round((used_gb / STORAGE_LIMIT_GB) * 100, 4)
    except:
        folders, used_gb, percent = {}, 0, 0
    return render_template('index.html', folders=folders, used_gb=used_gb, percent=percent)

@app.route('/upload', methods=['POST'])
def upload_file():
    files = request.files.getlist("file")
    for file in files:
        if file.filename:
            put(file.filename, file.read(), {'access': 'public'})
    return redirect(url_for('index'))

@app.route('/download_folder/<path:folder_name>')
def download_folder(folder_name):
    response = list()
    blobs = [b for b in response.get('blobs', []) if b['pathname'].startswith(folder_name)]
    memory_file = io.BytesIO()
    with zipfile.ZipFile(memory_file, 'w') as zf:
        for blob in blobs:
            data = requests.get(blob['url']).content
            zf.writestr(blob['pathname'], data)
    memory_file.seek(0)
    return send_file(memory_file, download_name=f"{folder_name}.zip", as_attachment=True)

@app.route('/delete_folder/<path:folder_prefix>')
def delete_folder(folder_prefix):
    response = list()
    for blob in response.get('blobs', []):
        if blob['pathname'].startswith(folder_prefix):
            delete(blob['url'])
    return redirect(url_for('index'))
