from flask import Flask, request, send_file, after_this_request
import yt_dlp
import os
import uuid

app = Flask(__name__)

@app.route('/download')
def download():
    video_url = request.args.get('url')
    if not video_url:
        return "URL missing", 400

    unique_id = str(uuid.uuid4())
    filename = f"video_{unique_id}.mp4"
    
    # Full HD (1080p) settings
    ydl_opts = {
        'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
        'outtmpl': filename,
        'merge_output_format': 'mp4',
        'noplaylist': True,
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([video_url])
        
        @after_this_request
        def cleanup(response):
            try:
                os.remove(filename)
            except Exception as e:
                print(f"Error deleting file: {e}")
            return response

        return send_file(filename, as_attachment=True)

    except Exception as e:
        return str(e), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
    