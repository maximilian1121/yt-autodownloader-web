import asyncio
import subprocess
from flask import Flask, request
import requests
from spotdl import Spotdl
import yt_dlp
import os
import threading

app = Flask(__name__)

def get_root_domain(url):
    while '://' in url:
        url = url.split('://', 1)[1]

    hostname = url.split('/')[0].split(':')[0]

    parts = hostname.split('.')
    if len(parts) < 2:
        return None

    return '.'.join(parts[-2:])

@app.route('/tailwind.js')
def tailwind_js():
    res = requests.get('https://cdn.tailwindcss.com')
    content = res.text.replace('console.warn("cdn.tailwindcss.com should not be used in production. To use Tailwind CSS in production, install it as a PostCSS plugin or use the Tailwind CLI: https://tailwindcss.com/docs/installation");', '\n')
    return content

def run_spotdl_download_cli(url):
    command = [
        "spotdl",
        "--bitrate", "320k",
        "--output", os.path.expanduser("~/Music"),
        url
    ]
    subprocess.run(command, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

@app.route('/download')
async def downloadSong():
    url = request.args.get('url')
    if not url:
        return {'success': False, 'error': 'No URL provided'}, 400

    tld = get_root_domain(url)
    try:
        if tld and tld.startswith('spotify'):
            
            threading.Thread(target=run_spotdl_download_cli, args=(url,), daemon=True).start()
        else:
            ydl_opts = {
                "format": "bestaudio/best",
                "extractaudio": True,
                "audioformat": "wav",
                "outtmpl": os.path.expanduser("~/Music/%(title)s.%(ext)s"),
                "quiet": True,
            }
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
    except Exception as e:
        return {'success': False, 'error': str(e)}, 500

    return {
        'success': True,
        'message': 'Download started successfully!'
    }


@app.route('/')
def index():
    return """
<!doctype html>
<html>
<head>
    <title>Music downloader</title>
    <script src="/tailwind.js"></script>
</head>
<body class="bg-gray-700 text-white flex flex-col items-center justify-start h-screen p-8 space-y-4">
    <h1 class="text-4xl font-bold">Music downloader</h1>
    <input id="songUrl" class="h-10 w-full max-w-xs bg-gray-800 text-white border border-gray-600 rounded p-2" type="text" placeholder="Enter song URL...">
    <button id="select" class="bg-blue-600 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded">Select</button>
</body>
<script>
document.getElementById('select').addEventListener('click', function() {
    const url = document.getElementById('songUrl').value;
    if (url) {
        fetch(`/download?url=${encodeURIComponent(url)}`)
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    alert('Download started successfully!');
                } else {
                    alert('Error: ' + data.error);
                }
            })
            .catch(error => {
                console.error('Error:', error);
                alert('An error occurred while trying to download the song.');
            });
    } else {
        alert('Please enter a valid URL');
    }
});
</script>
</html>
"""

