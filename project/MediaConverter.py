import os
import shutil

import tempfile
from moviepy.video.io.VideoFileClip import VideoFileClip
from moviepy.audio.io.AudioFileClip import AudioFileClip


def movetoDownloads():
    current_path = os.getcwd()
    tempfile_path = os.path.join(current_path, 'tempfile')
    download_path = os.path.join(current_path, 'downloads')

    # Get the list of files in the temporary directory
    files = os.listdir(tempfile_path)

    for file in os.listdir(tempfile_path):
        if file != ".gitkeep":
            file_name = file
    file_path = os.path.join(tempfile_path, file_name)
    download_file_path = os.path.join(download_path, file_name)

    # Move the file to the downloads folder
    shutil.move(file_path, download_file_path)

    # Return the path to the downloaded file
    return download_file_path



def convert_audio_format(input_name, input_format, output_format):
    """
    Convert a video file in the temporary directory to the desired format and
    delete the original file afterwards.

    Args:
        output_format (str): Desired output format extension (e.g. ".mp4").

    Returns:
        str: Path to the converted video file.
    """
    # Get the path to the input video file in the temporary directory
    currentPath = os.getcwd()
    folderName = 'tempfile'
    tempfile_path = os.path.join(currentPath,folderName)
    input_file = input_name
    input_path = os.path.join(tempfile_path, input_file)
    print("input path : "+input_path)

    # Get the path to the output video file in the temporary directory
    output_name = input_name + "." + output_format
    output_path = os.path.join(os.path.join(currentPath,"downloads"), output_name)

    # Load the input video file using moviepy
    audio = AudioFileClip(input_path)

    # Convert the input video to the desired output format
    audio.write_audiofile(output_path)

    # Delete the original input file
    os.remove(input_path)

    # Return the path to the converted output file
    return output_path
def convert_video_format(input_name, input_format, output_format):
    """
    Convert a video file in the temporary directory to the desired format and
    delete the original file afterwards.

    Args:
        output_format (str): Desired output format extension (e.g. ".mp4").

    Returns:
        str: Path to the converted video file.
    """
    # Get the path to the input video file in the temporary directory
    currentPath = os.getcwd()
    folderName = 'tempfile'
    tempfile_path = os.path.join(currentPath,folderName)
    input_file = input_name
    input_path = os.path.join(tempfile_path, input_file)
    print("input path : "+input_path)

    # Get the path to the output video file in the temporary directory
    output_name = input_name + "." + output_format
    output_path = os.path.join(os.path.join(currentPath,"downloads"), output_name)

    # Load the input video file using moviepy
    video = VideoFileClip(input_path)

    # Convert the input video to the desired output format
    video.write_videofile(output_path)

    # Delete the original input file
    os.remove(input_path)

    # Return the path to the converted output file
    return output_path

