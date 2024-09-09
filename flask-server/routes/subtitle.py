from flask import Blueprint, request, jsonify, session
import os
import subprocess

subtitle_bp = Blueprint('subtitle', __name__)

@subtitle_bp.route('/create-video/<file_id>', methods=['POST'])
def create_video(file_id):
    print("starting creation process")
    try:
        # Find the correct file extension
        print("get correct file extension")
        files = session.get('files', [])
        file_info = next((file for file in files if file['id'] == file_id), None)
        if not file_info:
            return jsonify({"error": "File not found in session."}), 404

        # Define paths
        file_extension = os.path.splitext(file_info['name'])[1]
        video_path = f'/Users/danielzhao/Documents/Github/fluentsubs/flask-server/file_downloads/{file_id}{file_extension}'
        srt_path = f'/Users/danielzhao/Documents/Github/fluentsubs/flask-server/srt_files/{file_id}.srt'
        output_dir = '/Users/danielzhao/Documents/Github/fluentsubs/flask-server/file_output_downloads'
        output_video_path = f'{output_dir}/{file_id}_with_subtitles.mp4'

        # Check if video and SRT files exist
        if not os.path.exists(video_path):
            return jsonify({"error": "Video file not found."}), 404
        if not os.path.exists(srt_path):
            return jsonify({"error": "SRT file not found."}), 404

        # Create the output directory if it doesn't exist
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        print("generating commands")

        # Add subtitles using FFmpeg
        command = [
            'ffmpeg',
            '-i', video_path,
            '-vf', f"subtitles={srt_path}:force_style='FontName=Arial,FontSize=24'",
            '-c:a', 'copy',  # Keep the original audio
            '-y',  # Overwrite output file if it exists
            output_video_path
        ]
        print("running subprocess")
        result = subprocess.run(command, capture_output=True, text=True)
        print("subprocess complete")

        # Print the stdout and stderr for debugging
        print("FFmpeg stdout:", result.stdout)
        print("FFmpeg stderr:", result.stderr)

        if result.returncode != 0:
            return jsonify({"error": "FFmpeg failed: " + result.stderr}), 500

        print("video creation success")
        return jsonify({"message": "Video created successfully", "video_path": output_video_path})

    except Exception as e:
        print(e)
        return jsonify({"error": str(e)}), 500
