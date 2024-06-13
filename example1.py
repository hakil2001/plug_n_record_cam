import os
import psutil
import time
import datetime
from picamera import PiCamera

def get_free_space_mb():
	statvfs = os.statvfs('/')
	block_size = statvfs.f_frsize
	free_blocks = statvfs.f_bfree
	free_space_mb = (free_blocks * block_size) / (1024**2)
	return free_space_mb

def start_recording():
	camera = PiCamera()
	camera.resolution = (1280, 720)
	camera.framerate = 30
	filename = '/home/pi/video_' + datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S") + '.h264'
	camera.start_recording(filename)
	return camera, filename

def stop_recording(camera, filename):
	camera.stop_recording()
	destination = '/var/www/html/files/' + os.path.basename(filename)
	os.rename(filename, destination)

def main():
	camera, current_file = start_recording()
    
	while True:
    	free_space = get_free_space_mb()
   	 
    	if free_space < 100:
        	stop_recording(camera, current_file)
        	break
   	 
    	try:
        	time.sleep(10)
    	except KeyboardInterrupt:
        	stop_recording(camera, current_file)
        	break
    	except Exception as e:
        	stop_recording(camera, current_file)
        	break

if __name__ == "__main__":
	main()
