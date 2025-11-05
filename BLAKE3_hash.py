from blake3 import blake3
import time
import os
import datetime
from pathlib import Path
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

#import apacheparquet libraries
from fastparquet import ParquetFile, write
import pandas as pd


#Directory being watched, paste directory here
HASH_DIR = "(path)"
META_DIR = Path("(path)")


#Break down file into chunks, read in binary, and converto to hexidecimal hash
def hash_file(path):
    hasher = blake3()
    #log time of process
    start_time = time.perf_counter()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            hasher.update(chunk)
        hash_value = hasher.hexdigest()
        end_time = time.perf_counter()

    #calculate the process time (ms)
    time_ms = (end_time - start_time) * 1000
    return hash_value, time_ms


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


#create an observer class to see if the directory is updated, record and store metdata and original name
class obsFile(FileSystemEventHandler):
    def on_created(self, event):
        if not event.is_directory:
            path = Path(event.src_path)
            print(f"[+] File added to directory: {path.name}")
            try:
                # File is hashed here
                file_hash, hash_time = hash_file(path)
                print(f"     BLAKE3 Hash: {file_hash}\n")

                #Original file metadata stored
                stats = path.stat()

                try:
                    time_of_creation = datetime.datetime.fromtimestamp(stats.st_birthtime)
                except AttributeError:
                    time_of_creation = datetime.datetime.fromtimestamp(stats.st_ctime)

                modified = datetime.datetime.fromtimestamp(stats.st_mtime)
                file_size = stats.st_size
                original_name = path.name

                #rename to hash
                new_path = rename_file(path, file_hash)
                time_of_hash = datetime.datetime.now()

                #reapply original timestamps for original file metadata
                try:
                    os.utime(new_path, (modified.timestamp(), modified.timestamp()))
                except Exception as e:
                    print(f"Error, timestamps for {new_path.name} not restored: {e} ")
    

                #Format metadata for file
                metadata = {
                    "original_path": original_name,
                    "hashed_path": new_path.name,
                    "hash_value": file_hash,
                    "file_size(bytes)": file_size,
                    "Hash process time(ms)": round(hash_time, 2),
                    "created": time_of_creation.strftime("%Y-%m-%d %H:%M:%S"),
                    "modified last": modified.strftime("%Y-%m-%d %H:%M:%S"),
                    "hashed": time_of_hash.strftime("%Y-%m-%d %H:%M:%S")
                }

                #Verify metadata directory
                META_DIR.mkdir(parents=True, exist_ok=True)

                meta_master = "MData/master_metadata.parq"

                #convert dictionary into dataframe
                metadata_df = pd.DataFrame([metadata])
                
                #Verify master file's existence, establish new master file if not already in metadata directory
                if os.path.exists(meta_master):
                    pf = ParquetFile(meta_master)
                    existing = pf.to_pandas()
                    new_df = pd.concat([existing, metadata_df], ignore_index=True)
                else:
                    new_df = metadata_df

                write(str(meta_master), new_df, compression='GZIP', file_scheme='simple')

                print(f"[+] New metadata entry written to {meta_master}")


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
