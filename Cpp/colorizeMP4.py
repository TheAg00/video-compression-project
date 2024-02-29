import numpy as np
import argparse
import cv2
import os

PROTOTXT = "colorization_deploy_v2.prototxt"
POINTS = "pts_in_hull.npy"
MODEL = "colorization_release_v2.caffemodel"


# # argparser
# ap = argparse.ArgumentParser()
# ap.add_argument("-i", "--input", type=str, required=True, help="path to input black and white video (.yuv)")
# ap.add_argument("-o", "--output", type=str, required=True, help="path to output colorized video")
# args = vars(ap.parse_args())

# load the model
print("Loading model...")
net = cv2.dnn.readNetFromCaffe(PROTOTXT, MODEL)
pts = np.load(POINTS, allow_pickle=True)

# load centers for ab channel quantization used for rebalancing
class8 = net.getLayerId("class8_ab")
conv8 = net.getLayerId("conv8_313_rh")
pts = pts.transpose().reshape(2, 313, 1, 1)
net.getLayer(class8).blobs = [pts.astype("float32")]
net.getLayer(conv8).blobs = [np.full([1, 313], 2.606, dtype="float32")]

# # Open input video
# input_video = cv2.VideoCapture(args["input"])
# if not input_video.isOpened():
#     print("Error: Could not open input video.")
#     exit()

# Open input video
input_video = cv2.VideoCapture(args["input"])
if not input_video.isOpened():
    print("Error: Could not open input video.")
    exit()

# Get video properties
frame_width = int(input_video.get(cv2.CAP_PROP_FRAME_WIDTH))
frame_height = int(input_video.get(cv2.CAP_PROP_FRAME_HEIGHT))
fps = int(input_video.get(cv2.CAP_PROP_FPS))

# Define the codec and create VideoWriter object
fourcc = cv2.VideoWriter_fourcc(*'XVID')
output_video = cv2.VideoWriter(args["output"], fourcc, fps, (frame_width, frame_height))


n = 0
while True:
    ret, frame = input_video.read()
    if not ret:
        break

    # Convert frame to LAB color space
    scaled = frame.astype("float32") / 255.0
    lab = cv2.cvtColor(scaled, cv2.COLOR_BGR2LAB)
    resized = cv2.resize(lab, (224, 224))
    L = cv2.split(resized)[0]
    L -= 50

    # Colorize the image
    net.setInput(cv2.dnn.blobFromImage(L))
    ab = net.forward()[0, :, :, :].transpose((1, 2, 0))
    ab = cv2.resize(ab, (frame.shape[1], frame.shape[0]))
    L = cv2.split(lab)[0]
    colorized = np.concatenate((L[:, :, np.newaxis], ab), axis=2)
    colorized = cv2.cvtColor(colorized, cv2.COLOR_LAB2BGR)

    # Write the colorized frame to the output video
    output_video.write((colorized * 255).astype("uint8"))

    n=n+1
    print(n)
    

# Release input and output videos
input_video.release()
output_video.release()

print("Colorized video saved successfully.")
