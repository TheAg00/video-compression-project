import cv2
import numpy as np

# Θέτουμε το ύψος και πλάτος του βίντεο.
HEIGHT = 1080
WIDTH = 1920


# Μετατρέπουμε το frame σε grayscaled.
def convert_to_grayscale(yuv_frame):
    # Θέτουμε τις τιμές των U και V σε 128, δηλαδή γκρίζο χρώμα.
    yuv_frame[WIDTH * HEIGHT : WIDTH * HEIGHT * 5 // 4] = 128  # U στοιχείο.
    yuv_frame[WIDTH * HEIGHT * 5 // 4 : WIDTH * HEIGHT * 3 // 2] = 128  # V στοιχείο.


if __name__ == "__main__":
    # Διαβάζουμε το yuv αρχείο.
    with open("./Bosphorus_1920x1080_120fps_420_8bit_YUV_RAW/Bosphorus_1920x1080_120fps_420_8bit_YUV.yuv", "rb+") as fd:
        yuv_data = fd.read()

    # Υπολογίζουμε το μέγεθος κάθε yuv frame.
    frameSize = int(WIDTH * HEIGHT * 3 / 2)
    print("yo")

    # Μετατρέπουμε τα YUV data σε NumPy πίνακα.
    yuv_frame = np.frombuffer(yuv_data, dtype=np.uint8)
    print("-1")
    frames = [yuv_frame[i*frameSize:(i+1)*frameSize] for i in range(len(yuv_data) // frameSize)]
    print("0")

    # Μετατρέπουμε κάθε frame σε grayscaled.
    for frame in frames:
        aFrame = np.copy(frame)
        convert_to_grayscale(aFrame)
    print("2")

    # Αντιστοιχούμε κάθε ασπρόμαυρο frame στο fd2 αρχείο.
    with open("Bosphorus.yuv", "wb") as fd2:
        for frame in frames:
            fd2.write(frame.tobytes())