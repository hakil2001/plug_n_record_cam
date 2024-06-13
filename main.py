import os
import psutil
import time
import datetime
from picamera import PiCamera
import shutil

# Define the interval (in seconds) for checkpoints
CHECKPOINT_INTERVAL = 30  # 30 seconds

# Define the directory where checkpoints are stored
CHECKPOINTS_DIR = '/home/picam/Recordings'

def get_free_space_mb():
    statvfs = os.statvfs('/')
    block_size = statvfs.f_frsize
    free_blocks = statvfs.f_bfree
    free_space_mb = (free_blocks * block_size) / (1024**2)
    return free_space_mb

def start_recording():
    camera = PiCamera()
    camera.resolution = (1920, 1080)  # Set resolution to Full HD
    camera.framerate = 30
    camera.sharpness = 50  # Adjust sharpness if needed
    camera.contrast = 50  # Adjust contrast if needed
    camera.brightness = 60  # Adjust brightness if needed
    camera.ISO = 400  # Set ISO if needed
    camera.exposure_mode = 'auto'
    camera.awb_mode = 'auto'
    filename = '/home/picam/Recordings/video_' + datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S") + '.h264'
    camera.start_recording(filename, bitrate=10000000)  # Set a higher bitrate for better quality
    return camera, filename

def stop_recording(camera, filename):
    camera.stop_recording()
    # No need to rename or move the file, filename is already the correct path

def create_checkpoint(current_file):
    # Create a timestamp for the checkpoint
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

    # Create a directory for the checkpoint
    checkpoint_dir = os.path.join(CHECKPOINTS_DIR, timestamp)
    os.makedirs(checkpoint_dir, exist_ok=True)

    # Copy the video file to the checkpoint directory
    shutil.copy2(current_file, os.path.join(checkpoint_dir, os.path.basename(current_file)))

def main():
    camera, current_file = start_recording()
    last_checkpoint_time = time.time()

    while True:
        free_space = get_free_space_mb()

        if free_space < 100:
            stop_recording(camera, current_file)
            break

        try:
            # Check if it's time to create a checkpoint
            if time.time() - last_checkpoint_time >= CHECKPOINT_INTERVAL:
                create_checkpoint(current_file)
                last_checkpoint_time = time.time()

            time.sleep(1)

        except KeyboardInterrupt:
            stop_recording(camera, current_file)
            break
        except Exception as e:
            print(f"An error occurred: {e}")
            stop_recording(camera, current_file)
            break

if __name__ == "__main__":
    main()
