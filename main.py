import os
import subprocess
import time
import json
import shutil
import ctypes
from mutagen import File
from all_o_one_ben import AllOne

# Global variables
MAIN_PATH = r"D:\Muusic"
FLAC_FOLDER = r"LIBRARY\FLAC\Soulseek"
OPUS_FOLDER = r"OPUS LIBRARY\COMPLETE\OPUS\Soulseek"
SYNC_FOLDER = "SyncThing_Folder"
TEMP_FOLDER = "Conversion_Temp_Folder"
BACKSLASH = "\\"
'''DAY = 86400
THIRTY_MINUTES = 30'''
DAY = 1
THIRTY_MINUTES = 5
IMAGE_EXTENSION = {'.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp', '.tiff'}
LOSSLESS_AUDIO = {".flac", ".alac", ".wav", ".aiff", ".wv", ".dsf", ".dff"}
LOSSY_AUDIO = {".mp3", ".aac", ".m4a", ".ogg", ".opus", ".wma", ".amr"}
FILE_ATTRIBUTE_SYSTEM = 0x4
INVALID_CHARACTERS = {'\\', '/', ':', '*', '?', '"', '<', '>', '|'}


def get_json():
    with open(r"D:\Documents\Programming\Audio_Conversion\audioConversion\data.json", "r") as f:
        data = json.load(f)

    return data


def get_folders(source_folder):
    path = source_folder
    directories = [os.path.join(path, name) for name in os.listdir(path) if (os.path.isdir(os.path.join(path, name))) and (not name.startswith("."))]
    folders = [os.path.basename(item) for item in directories]
    created_date = [os.path.getctime(item) for item in directories]

    return folders, created_date


def has_temp_files(source_folder):
    with os.scandir(source_folder) as entries:
        for entry in entries:
            if entry.is_file() and entry.name.lower().endswith(".tmp"):
                return True

    return False


def get_other_directories(source_folder, destination_folder):
    with os.scandir(source_folder) as entries:
        for entry in entries:
            if entry.is_file() and ((os.path.splitext(entry.name)[1] in LOSSLESS_AUDIO) or (os.path.splitext(entry.name)[1] in LOSSY_AUDIO)):
                main_convert(source_folder, destination_folder)
                break
            elif entry.is_dir():
                get_other_directories(source_folder + BACKSLASH + entry.name, destination_folder)


def is_system_file(path):
    attributes = ctypes.windll.kernel32.GetFileAttributesW(path)

    return bool(attributes & FILE_ATTRIBUTE_SYSTEM)


def get_audio_files_and_check_for_cover(source_folder):
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
                cover_file = entry.name
                has_img = True

    return lossless_audio_files, lossy_audio_files, cover_file


def get_album_name(source_folder, first_file_with_extension):
    audio = File(source_folder + BACKSLASH + first_file_with_extension)
    if audio:
        return audio.get("album")[0] or audio.get("ALBUM")[0]


def extract_cover(source_folder, first_file_with_extension):
    cover_extract_command = [
        "ffmpeg",
        "-i", source_folder + BACKSLASH + first_file_with_extension,
        "-map", "0:v?",
        "-frames:v", "1",
        source_folder + BACKSLASH + "cover.png"
    ]

    subprocess.run(cover_extract_command)


def get_artist_name_from_song(source_folder, current_file_with_extension):
    audio = File(source_folder + BACKSLASH + current_file_with_extension)
    if audio:
        return audio.get("artist")[0] or audio.get("ARTIST")[0]


def remove_invalid_characters(input_string):
    for char in input_string:
        if char in INVALID_CHARACTERS:
            input_string = input_string.replace(char, "")

    return input_string


def convert_audio(source_folder, destination_folder, current_file_with_extension, current_file_without_extension):
    convert_audio_command = [
        "ffmpeg",
        "-i", source_folder + BACKSLASH + current_file_with_extension,
        "-c:a", "libopus",
        "-b:a", "160k",
        "-map_metadata", "0",
        "-y", destination_folder + BACKSLASH + current_file_without_extension + ".opus",
    ]

    subprocess.run(convert_audio_command)


# Cover art command
def apply_cover_art(source_folder, destination_folder, current_file_without_extension, cover_file):
    dest_path = MAIN_PATH + BACKSLASH + TEMP_FOLDER + BACKSLASH + current_file_without_extension + ".opus"

    apply_cover_command = [
        "tageditor-cli", "set",
        "cover=" + source_folder + BACKSLASH + cover_file,
        "--files", destination_folder + BACKSLASH + current_file_without_extension + ".opus",
    ]

    subprocess.run(apply_cover_command)

    if os.path.isfile(dest_path + ".bak"):
        os.remove(dest_path + ".bak")


def create_artist_directory(destination_folder, artist_name):
    path = MAIN_PATH + BACKSLASH + destination_folder + BACKSLASH + artist_name
    if not os.path.exists(path):
        os.mkdir(path)


def create_album_directory(destination_folder, artist_name, album_name):
    path = MAIN_PATH + BACKSLASH + destination_folder + BACKSLASH + artist_name + BACKSLASH + album_name
    if not os.path.exists(path):
        os.mkdir(path)


def move_flac_files(source_folder, artist_name, album_name):
    dest_path = MAIN_PATH + BACKSLASH + FLAC_FOLDER + BACKSLASH + artist_name + BACKSLASH + album_name
    move_files(source_folder, dest_path)


def move_opus_files(artist_name, album_name):
    src_path = MAIN_PATH + BACKSLASH + TEMP_FOLDER
    dest_path = MAIN_PATH + BACKSLASH + OPUS_FOLDER + BACKSLASH + artist_name + BACKSLASH + album_name
    move_files(src_path, dest_path)


def move_files(src_path, dest_path):
    for item in os.listdir(src_path):
        shutil.move(src_path + BACKSLASH + item, dest_path + BACKSLASH + item)


def delete_old_contents(source_folder, destination_folder):
    shutil.rmtree(source_folder)
    shutil.rmtree(destination_folder)
    os.mkdir(destination_folder)


def main_convert(source_folder, destination_folder):
    print("Main Convert Started")
    lossless_audio_files, lossy_audio_files, cover_file = get_audio_files_and_check_for_cover(source_folder)
    print(lossless_audio_files)
    if not cover_file:
        if lossless_audio_files:
            extract_cover(source_folder, lossless_audio_files[0])
        else:
            extract_cover(source_folder, lossy_audio_files[0])
        if os.path.isfile(source_folder + BACKSLASH + "cover.png"):
            cover_file = "cover.png"
    if lossless_audio_files:
        album_name = get_album_name(source_folder, lossless_audio_files[0])
    elif lossy_audio_files:
        album_name = get_album_name(source_folder, lossy_audio_files[0])
    else:
        return None

    album_name = remove_invalid_characters(album_name)

    artist_names = AllOne()

    for current_file_with_extension in lossless_audio_files:
        artist_names.inc(get_artist_name_from_song(source_folder, current_file_with_extension))
        current_file_without_extension = os.path.splitext(current_file_with_extension)[0]
        convert_audio(source_folder, destination_folder, current_file_with_extension, current_file_without_extension)
        apply_cover_art(source_folder, destination_folder, current_file_without_extension, cover_file)

    for audio_file in lossy_audio_files:
        shutil.copy(source_folder + BACKSLASH + audio_file, destination_folder + BACKSLASH)
        artist_names.inc(get_artist_name_from_song(source_folder, audio_file))

    artist_name = artist_names.getMaxKey()
    artist_name = remove_invalid_characters(artist_name)

    create_artist_directory(FLAC_FOLDER, artist_name)
    create_artist_directory(OPUS_FOLDER, artist_name)

    create_album_directory(FLAC_FOLDER, artist_name, album_name)
    create_album_directory(OPUS_FOLDER, artist_name, album_name)

    move_flac_files(source_folder, artist_name, album_name)
    move_opus_files(artist_name, album_name)

    delete_old_contents(source_folder, destination_folder)

    print(album_name + " converted")


# Main program. Will run every half hour to check if anything needs converting
def main():
    print("Program Started")
    data = get_json()
    source_folder = MAIN_PATH + BACKSLASH + SYNC_FOLDER
    folders, created_date = get_folders(source_folder)
    current_time = time.time()

    if (not data) and folders:
        new_data = [{"folder": folders, "created-date": created} for folders, created in zip(folders, created_date)]
        with open(r"D:\Documents\Programming\Audio_Conversion\audioConversion\data.json", "w") as f:
            json.dump(new_data, f, indent=4)

    else:
        print("Checking data")
        new_data = data[:]
        data_offset = 0
        data_length = len(data)
        for i in range(len(folders)):
            print(folders)
            print(data)

            if (i >= data_length) or (folders[i] != data[i]["folder"]):
                new_data.insert(i + data_offset, {"folder": folders[i], "created-date": created_date[i]})
                if i < data_length:
                    data_offset += 1
            elif (data[i]["folder"] == folders[i]) and (current_time - created_date[i] > DAY):
                has_temp = has_temp_files(source_folder)

                if not has_temp:
                    print("Im here")
                    get_other_directories(source_folder + BACKSLASH + folders[i],
                                 MAIN_PATH + BACKSLASH + TEMP_FOLDER + BACKSLASH)
                    del new_data[i + data_offset]
                    data_offset -= 1
                else:
                    print("Added a day")
                    data[i]["created-date"] += DAY
            else:
                print("Strange error")

        with open(r"D:\Documents\Programming\Audio_Conversion\audioConversion\data.json", "w") as f:
            json.dump(new_data, f, indent=4)


while True:
    main()
    print("Waiting")
    time.sleep(THIRTY_MINUTES)
