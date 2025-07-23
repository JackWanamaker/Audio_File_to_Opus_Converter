import os
import subprocess
import time
from datetime import datetime
import json
import shutil
import ctypes
import mutagen
from mutagen import File
from all_o_one_ben import AllOne
import sys

# Global variables
#Testing Environment
#MAIN_PATH = r"D:\Audio_Conversion_Test"
#FLAC_FOLDER = r"Flac_Folder"
#OPUS_FOLDER = r"OPUS_Folder"
#SYNC_FOLDER = r"SyncThing_Folder"
#TEMP_FOLDER = r"Conversion_Temp_Folder"
MAIN_PATH = r"D:\Muusic"
FLAC_FOLDER = r"LIBRARY\FLAC\Soulseek"
OPUS_FOLDER = r"OPUS LIBRARY\COMPLETE\OPUS\Soulseek"
SYNC_FOLDER = "SyncThing_Folder"
TEMP_FOLDER = "Conversion_Temp_Folder"
JSON_PATH = r"D:\Documents\Programming\Audio_Conversion\audioConversion\data.json"
LOG_PATH = r"D:\Documents\Programming\Audio_Conversion\audioConversion\log.txt"
BACKSLASH = "\\"
#DAY = 86400
#THIRTY_MINUTES = 30
WEEK = 604800
DAY = 1
THIRTY_MINUTES = 5
#WEEK = 180
IMAGE_EXTENSION = {'.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp', '.tiff'}
LOSSLESS_AUDIO = {".flac", ".alac", ".wav", ".aiff", ".wv", ".dsf", ".dff"}
LOSSY_AUDIO = {".mp3", ".aac", ".m4a", ".ogg", ".opus", ".wma", ".amr"}
FILE_ATTRIBUTE_SYSTEM = 0x4
INVALID_CHARACTERS = {'\\', '/', ':', '*', '?', '"', '<', '>', '|'}


def delete_text_file():
    if os.path.getctime(LOG_PATH) > WEEK + time.time():
        print("Log File Deleted")
        os.remove(LOG_PATH)
        with open(LOG_PATH, "w") as f:
            f.write("File created\n")

#Gets the information from the JSON file
def get_json():
    print("Getting JSON data")
    with open(JSON_PATH, "r") as f:
        data = json.load(f)

    return data


#Gets the current folder names and creation dates
def get_folders(source_folder):
    print("Getting folders")
    path = source_folder
    directories = [os.path.join(path, name) for name in os.listdir(path) if (os.path.isdir(os.path.join(path, name))) and (not name.startswith("."))]
    folders = [os.path.basename(item) for item in directories]
    created_date = [os.path.getctime(item) for item in directories]

    return folders, created_date


#Checks if there are any SyncThing temporary files in the directory
def has_temp_files(source_folder):
    print("Checking for temp files")
    with os.scandir(source_folder) as entries:
        for entry in entries:
            if entry.is_file() and entry.name.lower().endswith(".tmp"):
                return True

    return False

#Finds directories in which we can convert audio
def get_other_directories(source_folder, destination_folder):
    print("Exploring for further directories")
    with os.scandir(source_folder) as entries:
        for entry in entries:
            if entry.is_file() and ((os.path.splitext(entry.name)[1] in LOSSLESS_AUDIO) or (os.path.splitext(entry.name)[1] in LOSSY_AUDIO)):
                main_convert(source_folder, destination_folder)
                return True
            elif entry.is_dir():
                return get_other_directories(source_folder + BACKSLASH + entry.name, destination_folder)
    return False


#Checks if a file is a Windows system file
def is_system_file(path):
    print("Checking if its a system file")
    attributes = ctypes.windll.kernel32.GetFileAttributesW(path)

    return bool(attributes & FILE_ATTRIBUTE_SYSTEM)


#Gathers all audio files and a cover file given a directory by get_other_directories
def get_audio_files_and_check_for_cover(source_folder):
    print("Getting Audio Files and Checking For Covers")
    lossless_audio_files = []
    lossy_audio_files = []
    cover_file = ""
    has_img = False
    with (os.scandir(source_folder) as entries):
        for entry in entries:
            if entry.is_file() and os.path.splitext(entry.name)[1] in LOSSLESS_AUDIO:
                lossless_audio_files.append(entry.name)
            elif entry.is_file() and os.path.splitext(entry.name)[1] in LOSSY_AUDIO:
                lossy_audio_files.append(entry.name)
            elif (entry.is_file()) and (os.path.splitext(entry.name)[1].lower() in IMAGE_EXTENSION) and (not has_img) and (not is_system_file(source_folder + BACKSLASH + entry.name)):
                print("Found cover file")
                cover_file = entry.name
                has_img = True

    return lossless_audio_files, lossy_audio_files, cover_file


#Gets the album name from the first file. Returns None if there is an error
def get_album_name(source_folder, first_file_with_extension):
    print("Getting Album Name")
    try:
        audio = File(source_folder + BACKSLASH + first_file_with_extension)
    except mutagen.MutagenError:
        print("Error Getting Album")
        return None
    if audio:
        album_name = audio.get("album") or audio.get("ALBUM")
        if album_name:
            return album_name[0]


#Runs a command to extract the album cover from the first audio file
def extract_cover(source_folder, first_file_with_extension):
    print("Extracting Cover")
    cover_extract_command = [
        "ffmpeg",
        "-i", source_folder + BACKSLASH + first_file_with_extension,
        "-map", "0:v?",
        "-frames:v", "1",
        source_folder + BACKSLASH + "cover.png"
    ]

    with open(LOG_PATH, "a") as f:
        subprocess.run(cover_extract_command, stdout=f, stderr=f)



#Gets artist name from a song. Returns None if there is an error
def get_artist_name_from_song(source_folder, current_file_with_extension):
    print("Getting Artist Name From Song: " + current_file_with_extension)
    try:
        audio = File(source_folder + BACKSLASH + current_file_with_extension)
    except mutagen.MutagenError:
        print("Error Getting Artist")
        return None
    if audio:
        artist_name = audio.get("artist") or audio.get("ARTIST")
        if artist_name:
            return artist_name[0]


#Removes invalid characters for folders
def remove_invalid_characters(input_string):
    print("Removing invalid characters")
    for char in input_string:
        if char in INVALID_CHARACTERS:
            print("Removed character: " + char)
            input_string = input_string.replace(char, "")

    return input_string


#Command that converts audio from source and puts it in the destination as opus
def convert_audio(source_folder, destination_folder, current_file_with_extension, current_file_without_extension):
    print("Converting Audio File: " + current_file_with_extension)
    convert_audio_command = [
        "ffmpeg",
        "-i", source_folder + BACKSLASH + current_file_with_extension,
        "-c:a", "libopus",
        "-b:a", "160k",
        "-map_metadata", "0",
        "-y", destination_folder + BACKSLASH + current_file_without_extension + ".opus",
    ]

    with open(LOG_PATH, "a") as f:
        subprocess.run(convert_audio_command, stdout=f, stderr=f)


#Applies cover art to a converted file
def apply_cover_art(source_folder, destination_folder, current_file_without_extension, cover_file):
    print("Applying Cover: " + current_file_without_extension + ".opus")
    dest_path = MAIN_PATH + BACKSLASH + TEMP_FOLDER + BACKSLASH + current_file_without_extension + ".opus"

    apply_cover_command = [
        "tageditor-cli", "set",
        "cover=" + source_folder + BACKSLASH + cover_file,
        "--files", destination_folder + BACKSLASH + current_file_without_extension + ".opus",
    ]

    with open(LOG_PATH, "a") as f:
        subprocess.run(apply_cover_command, stdout=f, stderr=f)

    if os.path.isfile(dest_path + ".bak"):
        print("Removed temp file")
        os.remove(dest_path + ".bak")


#Creates a folder based on the artist name
def create_artist_directory(destination_folder, artist_name):
    print("Creating Artist Directory")
    path = MAIN_PATH + BACKSLASH + destination_folder + BACKSLASH + artist_name
    if not os.path.exists(path):
        print("Created Directory")
        os.mkdir(path)


#Creates a folder based on the album name
def create_album_directory(destination_folder, artist_name, album_name):
    print("Creating Album Directory")
    path = MAIN_PATH + BACKSLASH + destination_folder + BACKSLASH + artist_name + BACKSLASH + album_name
    if not os.path.exists(path):
        print("Created Directory")
        os.mkdir(path)


#Moves flac files to their archive
def move_flac_files(source_folder, artist_name, album_name):
    print("Moving FLAC files")
    dest_path = MAIN_PATH + BACKSLASH + FLAC_FOLDER + BACKSLASH + artist_name + BACKSLASH + album_name
    move_files(source_folder, dest_path)


#Moves opus files to their archive
def move_opus_files(artist_name, album_name):
    print("Moving OPUS files")
    src_path = MAIN_PATH + BACKSLASH + TEMP_FOLDER
    dest_path = MAIN_PATH + BACKSLASH + OPUS_FOLDER + BACKSLASH + artist_name + BACKSLASH + album_name
    move_files(src_path, dest_path)


#Moves files
def move_files(src_path, dest_path):
    print("Moving Files")
    for item in os.listdir(src_path):
        if os.path.isfile(dest_path + BACKSLASH + item):
            os.remove(dest_path + BACKSLASH + item)
        shutil.move(src_path + BACKSLASH + item, dest_path + BACKSLASH + item)


#Deletes files in the source and destination folders after everything is done
def delete_old_contents(source_folder, destination_folder):
    print("Deleting Old Contents")
    shutil.rmtree(source_folder)
    shutil.rmtree(destination_folder)
    os.mkdir(destination_folder)


#Main convert function
def main_convert(source_folder, destination_folder):
    print("Main Convert Started")
    lossless_audio_files, lossy_audio_files, cover_file = get_audio_files_and_check_for_cover(source_folder)

    #Extracts cover based on if one was found in the folder or not
    if not cover_file:
        if lossless_audio_files:
            extract_cover(source_folder, lossless_audio_files[0])
        else:
            extract_cover(source_folder, lossy_audio_files[0])
        if os.path.isfile(source_folder + BACKSLASH + "cover.png"):
            cover_file = "cover.png"

    #Gets the album name depending on audio file types
    if lossless_audio_files:
        album_name = get_album_name(source_folder, lossless_audio_files[0])
    elif lossy_audio_files:
        album_name = get_album_name(source_folder, lossy_audio_files[0])
    else:
        delete_old_contents(source_folder, destination_folder)
        return None

    #Returns None if no album name is found. Some fatal error
    if not album_name:
        delete_old_contents(source_folder, destination_folder)
        return None

    print("Removing Invalid Characters From Album Name")
    album_name = remove_invalid_characters(album_name)

    #Uses an AllO(1) data structure to pick the most frequent artist name out of all the files
    artist_names = AllOne()

    #Processes/converts lossless audio
    for current_file_with_extension in lossless_audio_files:
        temp_artist_name = get_artist_name_from_song(source_folder, current_file_with_extension)
        if temp_artist_name:
            artist_names.inc(temp_artist_name)
        current_file_without_extension = os.path.splitext(current_file_with_extension)[0]
        convert_audio(source_folder, destination_folder, current_file_with_extension, current_file_without_extension)
        apply_cover_art(source_folder, destination_folder, current_file_without_extension, cover_file)

    #Copies lossy audio. No conversion
    for audio_file in lossy_audio_files:
        shutil.copy(source_folder + BACKSLASH + audio_file, destination_folder + BACKSLASH)
        temp_name = get_artist_name_from_song(source_folder, audio_file)
        if temp_name:
            artist_names.inc(temp_name)

    #Gets most common artist name from AllO(1)
    artist_name = artist_names.getMaxKey()

    #If no artist name, returns None. Fatal error
    if not artist_name:
        delete_old_contents(source_folder, destination_folder)
        return None

    artist_name = remove_invalid_characters(artist_name)

    #Creates artist folders for new files
    create_artist_directory(FLAC_FOLDER, artist_name)
    create_artist_directory(OPUS_FOLDER, artist_name)

    #Creates album folders for new files
    create_album_directory(FLAC_FOLDER, artist_name, album_name)
    create_album_directory(OPUS_FOLDER, artist_name, album_name)

    #Moves finished files to their destination
    move_flac_files(source_folder, artist_name, album_name)
    move_opus_files(artist_name, album_name)

    #Deletes old contents
    delete_old_contents(source_folder, destination_folder)

    print(album_name + " converted")


# Main program. Will run every half hour to check if anything needs converting
def main():
    current_time = time.time()
    current_date_time = datetime.fromtimestamp(current_time)
    print("Program Started: " + str(current_date_time))
    #Gets important variables
    data = get_json()
    source_folder = MAIN_PATH + BACKSLASH + SYNC_FOLDER
    folders, created_date = get_folders(source_folder)

    #If no data in JSON, adds all folder data to it
    if (not data) and folders:
        print("No data in JSON. Adding all folders to it")
        new_data = [{"folder": folders, "created-date": created} for folders, created in zip(folders, created_date)]
        with open(JSON_PATH, "w") as f:
            json.dump(new_data, f, indent=4)

    #Otherwise, we search through and see if any need converting
    else:
        print("Data in JSON. Now checking")
        new_data = data[:]
        data_offset = 0
        print("Printing Folders")
        print(folders)
        print("Printing JSON Data")
        print(data)
        for i in range(len(folders)):

            #If the folder is not in the JSON, or no JSON is left, we add the items
            if (i >= len(new_data)) or (folders[i] != new_data[i+data_offset]["folder"]):
                print("Current Iteration I: " + str(i))
                print("Current Iteration Plus Offset: " + str(data_offset))
                print("Current Folder: " + folders[i])
                print("Current JSON Folder: " + new_data[i+data_offset]["folder"])
                new_data.insert(i+data_offset, {"folder": folders[i], "created-date": created_date[i]})
            #Otherwise, we start converting the audio
            elif (new_data[i+data_offset]["folder"] == folders[i]) and (current_time - created_date[i] > DAY):
                has_temp = has_temp_files(source_folder)

                if not has_temp:
                    has_audio_files = get_other_directories(source_folder + BACKSLASH + folders[i],MAIN_PATH + BACKSLASH + TEMP_FOLDER + BACKSLASH)
                    print("Directory Has Audio Files: " + str(has_audio_files))
                    if has_audio_files:
                        print("Deleted Converted JSON")
                        del new_data[i + data_offset]
                        data_offset -= 1
                    else:
                        print("Added a day")
                        new_data[i + data_offset]["created-date"] += DAY
                #If temp files exist, we add another day to the creation date so it is converted later
                else:
                    print("Added a day")
                    new_data[i + data_offset]["created-date"] += DAY
            else:
                print("Folders are equal and need no change, or strange error")

        with open(JSON_PATH, "w") as f:
            json.dump(new_data, f, indent=4)


while True:
    with open(LOG_PATH, "a") as f:
        sys.stdout = f
        main()
    sys.stdout = sys.__stdout__
    print("Deleting")
    delete_text_file()
    time.sleep(THIRTY_MINUTES)
