import os
import subprocess
import shutil

SRC_DIR = r"D:\Muusic\LIBRARY\FLAC"
DEST_DIR = r"D:\Muusic\OPUS LIBRARY\NEW_OPUS"
BACKSLASH = "\\"
IMAGE_EXTENSION = {'.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp', '.tiff'}
LOSSLESS_AUDIO = {".flac", ".alac", ".wav", ".aiff", ".wv", ".dsf", ".dff"}
LOSSY_AUDIO = {".mp3", ".aac", ".m4a", ".ogg", ".opus", ".wma", ".amr"}


#i love you

def get_folders(path):
    directories = [os.path.join(path, name) for name in os.listdir(path) if
                   os.path.isdir(os.path.join(path, name))]
    folders = [os.path.basename(item) for item in directories]

    return folders


def get_audio_folders():
    folders = get_folders(SRC_DIR)

    for folder in folders:
        current_source_path = SRC_DIR + BACKSLASH + folder
        current_destination_path = DEST_DIR + BACKSLASH + folder
        os.mkdir(current_destination_path)

        print(current_source_path)

        get_album_folders(current_source_path, current_destination_path)


def get_album_folders(source_folder, destination_folder):
    folders = get_folders(source_folder)

    for folder in folders:
        current_source_path = source_folder + BACKSLASH + folder
        current_destination_path = destination_folder + BACKSLASH + folder
        os.mkdir(current_destination_path)
        print(current_source_path)
        print(current_destination_path)

        get_artist_folders(current_source_path, current_destination_path)


def get_artist_folders(source_folder, destination_folder):
    folders = get_folders(source_folder)

    for folder in folders:
        current_source_path = source_folder + BACKSLASH + folder
        current_destination_path = destination_folder + BACKSLASH + folder
        os.mkdir(current_destination_path)
        print(current_source_path)
        print(current_destination_path)

        get_other_directories(current_source_path, current_destination_path)


def get_other_directories(source_folder, destination_folder):
    with os.scandir(source_folder) as entries:
        for entry in entries:
            if entry.is_file() and ((os.path.splitext(entry.name)[1] in LOSSLESS_AUDIO) or (os.path.splitext(entry.name)[1] in LOSSY_AUDIO)):
                print(entry.name)
                process_audio(source_folder, destination_folder)
                break
            elif entry.is_dir():
                print(entry.name)
                get_other_directories(source_folder + BACKSLASH + entry.name, destination_folder)


def process_audio(source_folder, destination_folder):
    lossless_audio_files, lossy_audio_files, cover_file = get_audio_files_and_check_for_cover(source_folder)
    if not cover_file:
        if lossless_audio_files:
            extract_cover(source_folder, lossless_audio_files[0])
        else:
            extract_cover(source_folder, lossy_audio_files[0])
        if os.path.isfile(source_folder + BACKSLASH + "cover.png"):
            cover_file = "cover.png"
    for current_file_with_extension in lossless_audio_files:
        print(current_file_with_extension)
        current_file_without_extension = os.path.splitext(current_file_with_extension)[0]
        convert_audio(source_folder, destination_folder, current_file_with_extension,
                      current_file_without_extension)
        if cover_file:
            apply_cover_art(source_folder, destination_folder, current_file_without_extension,
                            cover_file)

    for audio_file in lossy_audio_files:
        print(source_folder + BACKSLASH + audio_file)
        print(destination_folder + BACKSLASH)
        shutil.copy(source_folder + BACKSLASH + audio_file, destination_folder + BACKSLASH)

def get_audio_files_and_check_for_cover(current_folder):
    lossless_audio_files = []
    lossy_audio_files = []
    cover_file = ""
    has_img = False
    with os.scandir(current_folder) as entries:
        for entry in entries:
            if entry.is_file() and os.path.splitext(entry.name)[1] in LOSSLESS_AUDIO:
                lossless_audio_files.append(entry.name)
            elif entry.is_file() and os.path.splitext(entry.name)[1] in LOSSY_AUDIO:
                print(entry.name)
                lossy_audio_files.append(entry.name)
            elif (entry.is_file()) and (os.path.splitext(entry.name)[1].lower() in IMAGE_EXTENSION) and (not has_img):
                cover_file = entry.name
                has_img = True

    return lossless_audio_files, lossy_audio_files, cover_file


def extract_cover(current_folder, first_file_with_extension):
    cover_extract_command = [
        "ffmpeg",
        "-i", current_folder + BACKSLASH + first_file_with_extension,
        "-map", "0:v?",
        "-frames:v", "1",
        current_folder + BACKSLASH + "cover.png"
    ]

    subprocess.run(cover_extract_command)


def convert_audio(current_folder, destination_folder, current_file_with_extension, current_file_without_extension):
    print(destination_folder)
    convert_audio_command = [
        "ffmpeg",
        "-i", current_folder + BACKSLASH + current_file_with_extension,
        "-c:a", "libopus",
        "-b:a", "160k",
        "-map_metadata", "0",
        "-y", destination_folder + BACKSLASH + current_file_without_extension + ".opus",
    ]

    subprocess.run(convert_audio_command)


def apply_cover_art(current_folder, destination_folder, current_file_without_extension, cover_file):

    apply_cover_command = [
        "tageditor-cli", "set",
        "cover=" + current_folder + BACKSLASH + cover_file,
        "--files", destination_folder + BACKSLASH + current_file_without_extension + ".opus",
    ]

    subprocess.run(apply_cover_command)

    if os.path.isfile(destination_folder + BACKSLASH + current_file_without_extension + ".opus" + ".bak"):
        os.remove(destination_folder + BACKSLASH + current_file_without_extension + ".opus" + ".bak")


def main():
    get_audio_folders()



main()