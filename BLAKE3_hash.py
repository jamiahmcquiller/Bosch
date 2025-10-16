from blake3 import blake3
import time
from pathlib import Path
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

#Directory being watched, paste directory here
HASH_DIR = "/Users/file"


#Break down file into chunks, read in binary, and converto to hexidecimal hash
def hash_file(path):
    hasher = blake3()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            hasher.update(chunk)
    return hasher.hexdigest()

#Rename file in directory to BLAKE3 Hash
def rename_file(path, file_hash):
    try:
        file_ext = path.suffix
        rename = f"{file_hash}{file_ext}"
        new_path = path.parent / rename

        if new_path.exists():
            return new_path

        path.rename(new_path)
        return new_path
    except Exception as e:
        print(f"There was an error renaming {path.name}: {e}")
        return path


#create an observer class to see if the directory is updated
class obsFile(FileSystemEventHandler):
    def on_created(self, event):
        if not event.is_directory:
            path = Path(event.src_path)
            print(f"[+] File added to directory: {path.name}")
            try:
                file_hash = hash_file(path)
                print(f"     BLAKE3 Hash: {file_hash}\n")
                rename_file(path, file_hash)
            except Exception as e:
                print(f" ERROR, {path.name} not hashed: {e}")

#Matches directory name to verify the file path is correct / usable
if __name__ == '__main__':
    obs_path = Path(HASH_DIR)
    if not obs_path.exists():
        print(f"New directory created: {obs_path}")
        obs_path.mkdir(parents=True)
    
    print(f"Currently watching {obs_path.resolve()}")

#initialize and begin observer after directory is established
event_handler = obsFile()
observer = Observer()
observer.schedule(event_handler, str(obs_path), recursive=False)
observer.start()

#run observer until program is shut down, or input is entered in terminal
try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    print("\nStopping...")
    observer.stop()
observer.join()


