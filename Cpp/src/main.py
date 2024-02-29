import os
import subprocess

import colorizeMP4


def grayscaleYUV():
    # Command to compile the C++ file
    compile_command = "g++ grayScaleYUV.cpp -o convertYUVtoGrayscale"

    # Command to execute the compiled C++ program
    execute_command = "./convertYUVtoGrayscale"

    # Compile the C++ file
    compile_result = subprocess.run(compile_command, shell=True)

    if compile_result.returncode != 0:
        print("Error compiling the C++ file.")
        exit(1)

    # Compilation successful, execute the compiled program
    execute_result = subprocess.run(execute_command, shell=True)

    if execute_result.returncode != 0:
        print("Error executing the compiled C++ program.")
        exit(1)
    

def convertYUVtoMP4(qp):
    print("Converting YUV to MP4 for qp = " + str(qp) + "...")
    # Command to execute
    command = "ffmpeg -f rawvideo -s:v 1920x1080 -pix_fmt yuv420p -r 120 -i ../resources/Bosphorus_black_and_white.yuv -c:v libx264 -preset medium -qp " + str(qp) + " -c:a copy ../resources/black_and_white_22.mp4"

    # Execute the command
    result = os.system(command)

    # Check the result
    if result == 0:
        # Command executed successfully
        print("FFmpeg command executed successfully.")
    else:
        # Command failed
        print("Error executing FFmpeg command.")


if __name__ == "__main__":
    pathBlackAndWhite = "../resources/Bosphorus_black_and_white.yuv"
    if not os.path.exists(pathBlackAndWhite):
        # Generate a grayscale YUV file from a color one.
        print("Generating grayscaled YUV file...")
        grayscaleYUV()  # Call your function to generate the grayscale YUV file
    
    print("YUV file is grayscaled!")

    pathMP4 = "../resources/black_and_white_22.mp4"

    if not os.path.exists(pathMP4):
        # Call your function to convert the YUV file to MP4
        convertYUVtoMP4(22)
        convertYUVtoMP4(27)
        convertYUVtoMP4(32)
        convertYUVtoMP4(37)
    
    print("YUV file has been converted to MP4!")

    pathColorized = "../resources/colorized22.mp4"
    if not os.path.exists(pathColorized):
        print("Colorizing MP4...")
        colorizeMP4.colorize()
    
    print("MP4 has been colorized!")