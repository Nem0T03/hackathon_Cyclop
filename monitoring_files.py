import subprocess
import sys

# Check if a module is installed
def is_module_installed(module_name):
    try:
        __import__(module_name)
        return True
    except ImportError:
        return False

# Install a module using pip
def install_module(module_name):
    subprocess.check_call([sys.executable, "-m", "pip", "install", module_name])

# Check and install watchdog if not installed
if not is_module_installed('watchdog'):
    print("Installing watchdog...")
    install_module('watchdog')

# Check and install psutil if not installed
if not is_module_installed('psutil'):
    print("Installing psutil...")
    install_module('psutil')

# Now you can import the modules    
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import psutil

def list_all_disks():
    temp = []
    for disk in psutil.disk_partitions(all=True):
        if disk.fstype:
            temp.append(disk.device)
    return temp

class FileEventHandler(FileSystemEventHandler):
    def on_created(self, event):
        if event.is_directory:
            return
        print("File created:", event.src_path)

    def on_modified(self, event):
        if event.is_directory:
            return
        print("File modified:", event.src_path)

def monitor_files(directory):
    observer = Observer()
    observer.schedule(FileEventHandler(), directory, recursive=True)
    print("Monitoring directory:", directory)
    observer.start()
    while True:
        observer.join()
        if KeyboardInterrupt:
            observer.stop()

if __name__ == "__main__":
    for disk in list_all_disks():
        drive_to_monitor = disk
        monitor_files(drive_to_monitor)
