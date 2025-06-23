import subprocess
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import time
import base64

command0 = [
    "ffmpeg",
    "-i", r"D:\Documents\Programming\Audio_Conversion\01_Bathtub.flac",
    "-f", "ffmetadata",
    r"D:\Documents\Programming\Audio_Conversion\metadata.txt"
]

command1 = [
    "ffmpeg",
    "-i", r"D:\Documents\Programming\Audio_Conversion\01_Bathtub.flac",
    "-map", "0:v",
    "-frames:v", "1",
    r"D:\Documents\Programming\Audio_Conversion\cover.jpg"
]

def convert_to_base64():
    with open(r"D:\Documents\Programming\Audio_Conversion\cover.jpg", "rb") as img_file:
        b64_string = base64.b64encode(img_file.read()).decode('utf-8')
    return b64_string


class SimpleHandler(FileSystemEventHandler):
    def on_created(self, event):
        print(f"File created: {event.src_path}")
        #subprocess.run(command0, check=True)
        #subprocess.run(command1, check=True)
        #b64_string = convert_to_base64()
        command2 = [
            "ffmpeg",
            "-i", r"D:\Documents\Programming\Audio_Conversion\01_Bathtub.flac",
            "-i", r"D:\Documents\Programming\Audio_Conversion\metadata.txt",
            "-map_metadata", "1",
            "-codec:a", "libopus",
            "-b:a", "128k",
            r"D:\Documents\Programming\Audio_Conversion\01_Bathtub.opus"
        ]

        #meta_file = open(r"D:\Documents\Programming\Audio_Conversion\metadata.txt", "a")
       # meta_file.write("METADATA_BLOCK_PICTURE=" + b64_string)
        #subprocess.run(command2, check=True)

    def on_modified(self, event):
        print(f"File modified: {event.src_path}")

    def on_deleted(self, event):
        print(f"File deleted: {event.src_path}")

if __name__ == "__main__":
    path = r"D:\Documents\Programming\Audio_Conversion\audioConversion"
    event_handler = SimpleHandler()
    observer = Observer()
    observer.schedule(event_handler, path=path, recursive=False)
    observer.start()

    try:
        print(f"Watching for changes in: {path}")
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()

    observer.join()

#subprocess.run(command, check=True)