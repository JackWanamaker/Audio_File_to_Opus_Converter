# This file tests to make sure that files will be converted one after another with no issues

import subprocess

# "Global" variables
main_path = r"D:\Audio_Conversion_Test"
flac_folder = r"Flac_Folder"
opus_folder = r"Opus_Folder"
sync_folder = r"SyncThing_Folder"
temp_folder = r"Conversion_Temp_Folder"
backslash = "\\"
current_folder = "Doggystyle"

current_file_with_extension = "01_Bathtub.flac"
current_file_without_extension = "01_Bathtub"

print(main_path + backslash + temp_folder + backslash + current_folder + backslash + current_file_without_extension + ".opus")

convert_audio_command = [
        "ffmpeg",
        "-i", main_path + backslash + sync_folder + backslash + current_folder + backslash + current_file_with_extension,
        "-c:a", "libopus",
        "-b:a", "128k",
        "-map_metadata", "0",
        main_path + backslash + temp_folder + backslash + current_file_without_extension + ".opus",
    ]

subprocess.run(convert_audio_command)

current_file_with_extension = "02_G_Funk_Intro.flac"
current_file_without_extension = "02_G_Funk_Intro"

convert_audio_command = [
        "ffmpeg",
        "-i", main_path + backslash + sync_folder + backslash + current_folder + backslash + current_file_with_extension,
        "-c:a", "libopus",
        "-b:a", "128k",
        "-map_metadata", "0",
        main_path + backslash + temp_folder + backslash + current_file_without_extension + ".opus",
    ]

subprocess.run(convert_audio_command)