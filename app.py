from flask import Flask, request, send_file, render_template
import yt_dlp
import os
import uuid

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/download', methods=['POST'])
def download_video():
    url = request.form['url']
    video_id = str(uuid.uuid4())
    output_path = f'{video_id}.mp4'

ydl_opts = {
    'outtmpl': output_path,
    'format': 'bestvideo+bestaudio/best',
    'merge_output_format': 'mp4',
    'ffmpeg_location': r'C:\Users\levir\Downloads\ffmpeg\bin',  # << your actual path here
}
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

    return send_file(output_path, as_attachment=True, download_name='video.mp4')

@app.after_request
def cleanup(response):
    # Optional: Delete all .mp4 files after sending
    for file in os.listdir('.'):
        if file.endswith('.mp4'):
            os.remove(file)
    return response

if __name__ == '__main__':
    app.run(debug=True)

