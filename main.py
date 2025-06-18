import subprocess
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import time
import base64

command = [
    "ffmpeg",
    "-i", r"D:\Documents\Programming\Audio_Conversion\flac_meta_test.flac",
    "-codec:a", "libopus",
    "-b:a", "128k",
    "-c:v", "copy",
    r"D:\Documents\Programming\Audio_Conversion\flac_meta_test.opus"
]

class SimpleHandler(FileSystemEventHandler):
    def on_created(self, event):
        print(f"File created: {event.src_path}")
        subprocess.run(command, check=True)
        with open(r"D:\Documents\Programming\Audio_Conversion\cover.jpg", "rb") as img_file:
            b64_string = base64.b64encode(img_file.read()).decode('utf-8')
        print(b64_string)

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