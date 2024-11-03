from transformers import pipeline
from tqdm import tqdm
from PIL import Image
import requests
import glob
import cv2
import ffmpeg
import os
import shutil

# load pipe
pipe = pipeline(task="depth-estimation", model="depth-anything/Depth-Anything-V2-Small-hf")

# Create a folder named rgb
if not os.path.exists('rgb'):
    os.makedirs('rgb')

# Create a folder named output/rgb
if not os.path.exists('output/rgb'):
    os.makedirs('output/rgb')


video_path = 'video.mp4'

# Extract frames from video into png_frames
ffmpeg.input(video_path).output('rgb/frame%04d.png').run()

for image in tqdm(glob.glob("./rgb/*.png")):
    img = Image.open(image)
    depth = pipe(image)["depth"]
    depth = depth.convert('L')
    output_path = 'output/'+image
    depth.save(output_path)

# convert saved frames to video
ffmpeg.input('output/frame%04d.png', framerate=25).output('output_video.mp4').run()

# remove the rgb folder
shutil.rmtree('rgb')

# remove the output folder
shutil.rmtree('output')