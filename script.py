import numpy as np
import os

import grayScaleYUV

# Θέτουμε το ύψος και πλάτος του βίντεο.
HEIGHT = 1080
WIDTH = 1920


if __name__ == "__main__":
    if not os.path.exists("Bosphorus_black_and_white.yuv"):
        # Δημιουργούμε ένα ασπρόμαυρο ασυμπίστο αρχείο από ένα ένχρωμο.
        print("Generating grayscaled YUV file...")
        grayScaleYUV.grayScale()
        print("YUV file generated successfully!")
