import os
import subprocess
import time
import json
import shutil
from mutagen import File
from all_o_one_ben import AllOne

# Global variables
MAIN_PATH = r"D:\Audio_Conversion_Test"
FLAC_FOLDER = "Flac_Folder"
OPUS_FOLDER = "Opus_Folder"
SYNC_FOLDER = "SyncThing_Folder"
TEMP_FOLDER = "Conversion_Temp_Folder"
BACKSLASH = "\\"
'''FIVE_DAYS = 432000
DAY = 86400
THIRTY_MINUTES = 30'''
FIVE_DAYS = 1
DAY = 1
THIRTY_MINUTES = 5
IMAGE_EXTENSION = {'.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp', '.tiff'}


def get_json():
    with open("data.json", "r") as f:
        data = json.load(f)

    return data


def get_folders():
    path = MAIN_PATH + BACKSLASH + SYNC_FOLDER
    directories = [os.path.join(path, name) for name in os.listdir(path) if os.path.isdir(os.path.join(path, name))]
    folders = [os.path.basename(item) for item in directories]
    created_date = [os.path.getctime(item) for item in directories]

    return folders, created_date


def has_temp_files(current_folder):
    with os.scandir(MAIN_PATH + BACKSLASH + SYNC_FOLDER + BACKSLASH + current_folder) as entries:
        for entry in entries:
            if entry.is_file() and entry.name.lower().endswith(".tmp"):
                return True

    return False


def get_audio_files_and_check_for_cover(current_folder):
    audio_files = []
    cover_file = ""
    has_img = False
    with os.scandir(MAIN_PATH + BACKSLASH + SYNC_FOLDER + BACKSLASH + current_folder) as entries:
        for entry in entries:
            if entry.is_file() and entry.name.lower().endswith(".flac"):
                audio_files.append(entry.name)
            elif (entry.is_file()) and (os.path.splitext(entry.name)[1].lower() in IMAGE_EXTENSION) and (not has_img):
                cover_file = entry.name
                has_img = True

    return audio_files, cover_file


def get_album_name(current_folder, first_file_with_extension):
    audio = File(MAIN_PATH + BACKSLASH + SYNC_FOLDER + BACKSLASH + current_folder + BACKSLASH + first_file_with_extension)
    if audio:
        return audio.get("album")[0] or audio.get("ALBUM")[0]


def extract_cover(current_folder, first_file_with_extension):
    cover_extract_command = [
        "ffmpeg",
        "-i", MAIN_PATH + BACKSLASH + SYNC_FOLDER + BACKSLASH + current_folder + BACKSLASH + first_file_with_extension,
        "-map", "0:v?",
        "-frames:v", "1",
        MAIN_PATH + BACKSLASH + SYNC_FOLDER + BACKSLASH + current_folder + BACKSLASH + "cover.png"
    ]

    subprocess.run(cover_extract_command)


def get_artist_name_from_song(current_folder, current_file_with_extension):
    audio = File(MAIN_PATH + BACKSLASH + SYNC_FOLDER + BACKSLASH + current_folder + BACKSLASH + current_file_with_extension)
    if audio:
        return audio.get("artist")[0] or audio.get("ARTIST")[0]


def convert_audio(current_folder, current_file_with_extension, current_file_without_extension):
    convert_audio_command = [
        "ffmpeg",
        "-i", MAIN_PATH + BACKSLASH + SYNC_FOLDER + BACKSLASH + current_folder + BACKSLASH + current_file_with_extension,
        "-c:a", "libopus",
        "-b:a", "160k",
        "-map_metadata", "0",
        "-y", MAIN_PATH + BACKSLASH + TEMP_FOLDER + BACKSLASH + current_file_without_extension + ".opus",
    ]

    subprocess.run(convert_audio_command)


# Cover art command
def apply_cover_art(current_folder, current_file_without_extension, cover_file):
    dest_path = MAIN_PATH + BACKSLASH + TEMP_FOLDER + BACKSLASH + current_file_without_extension + ".opus"

    apply_cover_command = [
        "tageditor-cli", "set",
        "cover=" + MAIN_PATH + BACKSLASH + SYNC_FOLDER + BACKSLASH + current_folder + BACKSLASH + cover_file,
        "--files", MAIN_PATH + BACKSLASH + TEMP_FOLDER + BACKSLASH + current_file_without_extension + ".opus",
    ]

    subprocess.run(apply_cover_command)

    if os.path.isfile(dest_path + ".bak"):
        os.remove(dest_path + ".bak")


'''def get_final_artist_name(artist_names):
    invalid_chars = r'<>:"/\\|?*'
    print(artist_names.getMaxKey())
    print(type(artist_names.getMaxKey()))
    for artist_name in artist_names.getMaxKey():
        if not any(char in artist_name for char in invalid_chars):
            return artist_name

    return "Unknown Artist"'''


def create_artist_directory(destination_folder, artist_name):
    path = MAIN_PATH + BACKSLASH + destination_folder + BACKSLASH + artist_name
    if not os.path.exists(path):
        os.mkdir(path)


def create_album_directory(destination_folder, artist_name, album_name):
    path = MAIN_PATH + BACKSLASH + destination_folder + BACKSLASH + artist_name + BACKSLASH + album_name
    if os.path.exists(path):
        shutil.rmtree(path)
    os.mkdir(path)


def move_flac_files(source_folder, artist_name, album_name):
    src_path = MAIN_PATH + BACKSLASH + SYNC_FOLDER + BACKSLASH + source_folder
    dest_path = MAIN_PATH + BACKSLASH + FLAC_FOLDER + BACKSLASH + artist_name + BACKSLASH + album_name
    move_files(src_path, dest_path)


def move_opus_files(artist_name, album_name):
    src_path = MAIN_PATH + BACKSLASH + TEMP_FOLDER
    dest_path = MAIN_PATH + BACKSLASH + OPUS_FOLDER + BACKSLASH + artist_name + BACKSLASH + album_name
    move_files(src_path, dest_path)


def move_files(src_path, dest_path):
    for item in os.listdir(src_path):
        shutil.move(src_path + BACKSLASH + item, dest_path + BACKSLASH + item)


def delete_old_contents(current_folder):
    shutil.rmtree(MAIN_PATH + BACKSLASH + SYNC_FOLDER + BACKSLASH + current_folder)
    shutil.rmtree(MAIN_PATH + BACKSLASH + TEMP_FOLDER)
    os.mkdir(MAIN_PATH + BACKSLASH + TEMP_FOLDER)


def main_convert(current_folder):
    print("Main Convert Started")
    audio_files, cover_file = get_audio_files_and_check_for_cover(current_folder)
    if not cover_file:
        extract_cover(current_folder, audio_files[0])
        cover_file = "cover.png"
    album_name = get_album_name(current_folder, audio_files[0])
    print("Album: " + album_name)
    artist_names = AllOne()

    for current_file_with_extension in audio_files:
        artist_names.inc(get_artist_name_from_song(current_folder, current_file_with_extension))
        current_file_without_extension = os.path.splitext(current_file_with_extension)[0]
        convert_audio(current_folder, current_file_with_extension, current_file_without_extension)
        apply_cover_art(current_folder, current_file_without_extension, cover_file)

    artist_name = artist_names.getMaxKey()

    create_artist_directory(FLAC_FOLDER, artist_name)
    create_artist_directory(OPUS_FOLDER, artist_name)

    create_album_directory(FLAC_FOLDER, artist_name, album_name)
    create_album_directory(OPUS_FOLDER, artist_name, album_name)

    move_flac_files(current_folder, artist_name, album_name)
    move_opus_files(artist_name, album_name)

    delete_old_contents(current_folder)

    print(album_name + " converted")


# Main program. Will run every half hour to check if anything needs converting
def main():
    print("Program Started")
    data = get_json()
    folders, created_date = get_folders()
    current_time = time.time()

    if (not data) and folders:
        new_data = [{"folder": folders, "created-date": created} for folders, created in zip(folders, created_date)]
        with open("data.json", "w") as f:
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
            elif (data[i]["folder"] == folders[i]) and (current_time - created_date[i] > FIVE_DAYS):
                has_temp = has_temp_files(folders[i])

                if not has_temp:
                    print("Im here")
                    main_convert(folders[i])
                    del new_data[i + data_offset]
                    data_offset -= 1
                else:
                    print("Added a day")
                    data[i]["created-date"] += DAY
            else:
                print("Strange error")

        with open("data.json", "w") as f:
            json.dump(new_data, f, indent=4)


while True:
    main()
    print("Waiting")
    time.sleep(THIRTY_MINUTES)
