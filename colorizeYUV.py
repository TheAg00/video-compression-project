import numpy as np
import cv2

def colorizeYUV():
    with open("Bosphorus_1920x1080_120fps_420_8bit_YUV_RAW/Bosphorus_1920x1080_120fps_420_8bit_YUV.yuv", "rb") as fd:
        dataYUV = fd.read()

    # Υπολογίζουμε το μέγεθος κάθε yuv frame.
    frameSize = WIDTH * HEIGHT * 3 // 2

    # Μετατρέπουμε τα YUV data σε NumPy πίνακα.
    frameYUV = np.frombuffer(dataYUV, dtype=np.uint8)
    frames = [frameYUV[i * frameSize:(i + 1) * frameSize] for i in range(len(dataYUV) // frameSize)]

    # Load the pre-trained colorization model
    prototxt = "models/colorization_deploy_v2.prototxt"
    model = "models/colorization_release_v2.caffemodel"
    net = cv2.dnn.readNetFromCaffe(prototxt, model)

    for frame in frames:
        # Resize the grayscale array to the required input size of the model
        scaled = cv2.resize(frame, (224, 224))

        # Normalize the input array
        input_blob = cv2.dnn.blobFromImage(scaled)

        # Set the input to the model
        net.setInput(input_blob)

        # Perform colorization
        output = net.forward()

        # Reshape the output to the proper image shape
        output = output[0, :, :, :].transpose((1, 2, 0))
        output = cv2.resize(output, (frame.shape[1], frame.shape[0]))

        # Concatenate the original grayscale array with the colorized array
        colorized_array = np.concatenate((frame[:, :, np.newaxis], output), axis=2)

        # Convert the colorized array from LAB to BGR
        colorized_array = cv2.cvtColor(colorized_array, cv2.COLOR_LAB2BGR)

        # Display or save the colorized image
        cv2.imshow("Colorized Image", colorized_array)
        cv2.waitKey(0)
        cv2.destroyAllWindows()