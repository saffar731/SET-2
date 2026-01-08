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
        total_bytes = sum(blob['size'] for blob in blobs)
        used_gb = round(total_bytes / (1024**3), 6)
        percent = round((used_gb / STORAGE_LIMIT_GB) * 100, 4)
    except:
        blobs, used_gb, percent = [], 0, 0
    
    return render_template('index.html', items=blobs, used_gb=used_gb, percent=percent)

@app.route('/upload', methods=['POST'])
def upload_file():
    files = request.files.getlist("file")
    for file in files:
        if file.filename:
            put(file.filename, file.read(), {'access': 'public'})
    return redirect(url_for('index'))

@app.route('/delete/<path:url>')
def delete_item(url):
    delete(url)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
