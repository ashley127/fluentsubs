from flask import Blueprint, request, jsonify, session, send_file
import os
import subprocess

# Set up the blueprint
subtitle_bp = Blueprint('subtitle', __name__)

# Helper function to generate SRT content
def generate_srt(timestamps, text):
    srt_content = ""
    for i, (start, end) in enumerate(timestamps):
        srt_content += f"{i+1}\n"
        srt_content += f"{start} --> {end}\n"
        srt_content += f"{text[i]}\n\n"
    return srt_content

@subtitle_bp.route('/create-video/<file_id>', methods=['POST'])
def create_video(file_id):
    try:
        # Assuming text and timestamps are sent in the POST request
        data = request.json
        timestamps = data['timestamps']  # List of tuples with start and end times
        text = data['text']  # List of strings corresponding to each timestamp

        # Generate the SRT file content
        srt_content = generate_srt(timestamps, text)
        srt_filename = f'/path/to/output/{file_id}.srt'
        with open(srt_filename, 'w') as srt_file:
            srt_file.write(srt_content)

        # Path to the MP4 file
        mp4_file_path = f'/Users/danielzhao/Documents/Github/fluentsubs/flask-server/file_downloads/{file_id}.mp3' # mp3 since test file is mp3
        output_video_path = f'/path/to/output/{file_id}_subtitled.mp4'

        ffmpeg_command = [
            'ffmpeg',
            '-i', mp4_file_path,
            '-vf', f'subtitles={srt_filename}',
            '-c:a', 'copy',
            output_video_path
        ]
        subprocess.run(ffmpeg_command, check=True)

        # Optionally, return the video file as a response
        return send_file(output_video_path, as_attachment=True)

    except Exception as e:
        return jsonify({"error": str(e)}), 500
