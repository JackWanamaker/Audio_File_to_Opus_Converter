import os
import subprocess
import time
import json
from bisect import bisect_left
from mutagen import File

from folder_detection import test_func

# "Global" variables
main_path = r"D:\Audio_Conversion_Test"
flac_folder = r"Flac_Folder"
opus_folder = r"Opus_Folder"
backslash = "\\"
image_extension = ".png"


# Values to pass in but set to values for testing
current_folder = r""
current_file_with_extension = r""
current_file_without_extension = r""
first_file_with_extension = r""

# Use All O(1) structure to store most frequent artist name. Use this to decide what artist folder it goes in.
# Otherwise put in Unknown Artist folder

def get_json():
    with open("processed.json", "r") as f:
        processed = json.load(f)
    with open("unprocessed.json", "r") as f:
        unprocessed = json.load(f)

    return processed, unprocessed

def

#Use Global pass in variables to start testing all functions, then remove them later and pass in values
#def extract_album_name(current_folder, first_file_with_extension):
def get_album_name():
    audio = File(main_path + backslash + flac_folder + backslash + current_folder + backslash + first_file_with_extension)
    if audio:
        return audio.get("album") or audio.get("ALBUM")

#def cover_extract(current_folder, first_file_with_extension):
def cover_extract():
    cover_extract_command = [
        "ffmpeg",
        "-i", main_path + backslash + flac_folder + backslash + current_folder + backslash + first_file_with_extension,
        "-map", "0:v",
        "-frames:v", "1",
        main_path + backslash + flac_folder + backslash + current_folder + backslash + "cover.png"
    ]

    return cover_extract_command

#def get_artist_name(current_folder, current_file_with_extension):
def get_artist_name():
    audio = File(main_path + backslash + flac_folder + backslash + current_folder + backslash + first_file_with_extension)
    if audio:
        return audio.get("artist") or audio.get("ARTIST")

#def convert_audio(current_folder, current_file_without_extension):
def convert_audio():
    convert_audio_command = [
        "ffmpeg",
        "-i", main_path + backslash + flac_folder + backslash + current_folder + backslash + current_file_with_extension,
        "c:a", "libopus",
        "-map_metadata", "0",
              main_path + backslash + opus_folder + backslash + current_folder + backslash + current_file_without_extension + ".opus",
    ]

    return convert_audio_command

# Cover art command
r'''tageditor-cli set cover=D:\Documents\Programming\Audio_Conversion\audioConversion\cover.jpg --files D:\Documents\Programming\Audio_Conversion\audioConversion\01_Bathtub.opus'''
def apply_cover_art():
    apply_cover_command = [
        "tageditor-cli", "set",
        "cover=" + main_path + backslash + flac_folder + backslash + current_folder + backslash + "cover" + image_extension,
        "--files", main_path + backslash + opus_folder + backslash + current_folder + backslash + current_file_without_extension + ".opus",
    ]

def main():
    processed, unprocessed = get_json()




    return None

while True:
    main()
    time.sleep(30)



#subprocess.run(command, check=True)