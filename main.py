import os
import subprocess
import time
import json
from bisect import bisect_left
from mutagen import File

# "Global" variables
main_path = r"D:\Audio_Conversion_Test"
flac_folder = r"Flac_Folder"
opus_folder = r"Opus_Folder"
sync_folder = r"SyncThing_Folder"
temp_folder = r"Conversion_Temp_Folder"
backslash = "\\"
image_extension = ".png"
week_long = 604800
day_long = 86400


# Values to pass in but set to values for testing
current_folder = r""
current_file_with_extension = r""
current_file_without_extension = r""
first_file_with_extension = r""

# Use All O(1) structure to store most frequent artist name. Use this to decide what artist folder it goes in.
# Otherwise put in Unknown Artist folder

def get_json():
    with open("data.json", "r") as f:
        data = json.load(f)

    return data

def get_folders():
    path = main_path + backslash + sync_folder
    print(path)
    directories = [os.path.join(path, name) for name in os.listdir(path) if os.path.isdir(os.path.join(path, name))]
    folders = [os.path.basename(item) for item in directories]
    created_date = [os.path.getctime(item) for item in directories]
    modified_date = [os.path.getmtime(item) for item in directories]

    return folders, created_date, modified_date

#Use Global pass in variables to start testing all functions, then remove them later and pass in values
#def extract_album_name(current_folder, first_file_with_extension):
def get_album_name():
    audio = File(main_path + backslash + sync_folder + backslash + current_folder + backslash + first_file_with_extension)
    if audio:
        return audio.get("album") or audio.get("ALBUM")

#def cover_extract(current_folder, first_file_with_extension):
def cover_extract():
    cover_extract_command = [
        "ffmpeg",
        "-i", main_path + backslash + sync_folder + backslash + current_folder + backslash + first_file_with_extension,
        "-map", "0:v",
        "-frames:v", "1",
        main_path + backslash + sync_folder + backslash + current_folder + backslash + "cover.png"
    ]

    return cover_extract_command

#def get_artist_name(current_folder, current_file_with_extension):
def get_artist_name():
    audio = File(main_path + backslash + sync_folder + backslash + current_folder + backslash + first_file_with_extension)
    if audio:
        return audio.get("artist") or audio.get("ARTIST")

#def convert_audio(current_folder, current_file_without_extension):
def convert_audio():
    convert_audio_command = [
        "ffmpeg",
        "-i", main_path + backslash + sync_folder + backslash + current_folder + backslash + current_file_with_extension,
        "-c:a", "libopus",
        "-b:a", "128k",
        "-map_metadata", "0",
        main_path + backslash + temp_folder + backslash + current_file_without_extension + ".opus",
    ]

    return convert_audio_command

# Cover art command
r'''tageditor-cli set cover=D:\Documents\Programming\Audio_Conversion\audioConversion\cover.jpg --files D:\Documents\Programming\Audio_Conversion\audioConversion\01_Bathtub.opus'''
def apply_cover_art():
    apply_cover_command = [
        "tageditor-cli", "set",
        "cover=" + main_path + backslash + sync_folder + backslash + current_folder + backslash + "cover" + image_extension,
        "--files", main_path + backslash + temp_folder + backslash + current_file_without_extension + ".opus",
    ]

def main_convert():
    return None

def main():
    data = get_json()

    folders, created_date, modified_date = get_folders()

    current_time = time.time()

    print(folders)
    print(time.ctime(current_time-created_date[0]))

    new_data = [{"folder": folders, "created-date": created, "modified-date": modified} for folders, created, modified in zip(folders, created_date, modified_date)]

    if not data:
        with open("data.json", "w") as f:
            json.dump(new_data, f, indent=4)

    elif len(data) != len(folders):
        data_index = 0
        for i in range(len(folders)):
            if folders[i] != data[i]["folder"]:
                data.insert(i, {"folder": folders[i], "created-date": created_date[i], "modified-date": modified_date[i]})
            elif (data[i]["folder"] != folders[i]) and (time.time() - created_date[i] > week_long) and (modified_date[i] - created_date[i] > day_long):

                print("None")

    return None

'''while True:
    main()
    time.sleep(30)'''

main()



#subprocess.run(command, check=True)