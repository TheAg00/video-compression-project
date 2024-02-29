import numpy as np
import cv2

PROTOTXT = "../models/colorization_deploy_v2.prototxt"
POINTS = "../models/pts_in_hull.npy"
MODEL = "../models/colorization_release_v2.caffemodel"

WIDTH = 1920
HEIGHT = 1080
FPS = 120

def colorize():
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

    # Open input video
    input_video = cv2.VideoCapture("../resources/black_and_white_22.mp4")
    if not input_video.isOpened():
        print("Error: Could not open input video.")
        exit()

    # Define the codec and create VideoWriter object
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    output_video = cv2.VideoWriter("../resources/colorized22.mp4", fourcc, FPS, (WIDTH, HEIGHT))


    n = 0
    while True:
        ret, frame = input_video.read()

        if not ret: break

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

        n += 1
        print("Colorizing frame: " + str(n) + "/600")
        

    # Release input and output videos
    input_video.release()
    output_video.release()

    print("Colorized video saved successfully.")
