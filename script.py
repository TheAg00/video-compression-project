import numpy as np
# import tensorflow as tf

import grayScaleYUV

# Θέτουμε το ύψος και πλάτος του βίντεο.
HEIGHT = 1080
WIDTH = 1920

# def colorise(yuv_frame):
#     # Φορτώνουμε το pre-trained μοντέλο για χρωματισμό.
#     model = tf.keras.models.load_model("colorization_model.h5")

#     yuv_frame = model.predict(yuv_frame)


if __name__ == "__main__":
    # Δημιουργούμε ένα ασπρόμαυρο ασυμπίστο αρχείο από ένα ένχρωμο.
    print("Generating grayscaled YUV file...")
    grayScaleYUV.grayScale()
    print("YUV file generated successfully!")

    # with open("Bosphorus_black_and_white.yuv", "rb") as fd:
    #     yuv_data = fd.read()
    
    # # Υπολογίζουμε το μέγεθος κάθε yuv frame.
    # frameSize = int(WIDTH * HEIGHT * 3 / 2)

    # # Μετατρέπουμε τα YUV data σε NumPy πίνακα.
    # yuv_frame = np.frombuffer(yuv_data, dtype=np.uint8)
    # frames = [yuv_frame[i*frameSize:(i+1)*frameSize] for i in range(len(yuv_data) // frameSize)]

    # colorisedFrames = []
    # for frame in frames:
    #     aFrame = np.copy(frame)
    #     colorise(aFrame)
    #     colorisedFrames.append(aFrame)
    
    # with open("Bosphorus_colorized.yuv", "wb") as fd2:
    #     for frame in colorisedFrames:
    #         fd2.write(frame.tobytes())