#include <iostream>
#include <fstream>
#include <vector>
#include <algorithm>
#include <opencv2/opencv.hpp>


#include <cstdlib> // for system()

#include "../include/header.h" // Include your header file containing the function definitions

using namespace std;

constexpr int HEIGHT = 1080;
constexpr int WIDTH = 1920;
constexpr int FPS = 120;


void convertYUVtoMP4() {
    // Command to execute
    const char* command = "ffmpeg -f rawvideo -s:v 1920x1080 -pix_fmt yuv420p -r 120 -i ../resources/Bosphorus_black_and_white.yuv -c:v libx264 -preset medium -qp 22 -c:a copy ../resources/black_and_white_22.mp4";

    // Execute the command
    int result = system(command);

    // Check the result
    if (result == 0) {
        // Command executed successfully
        cout << "FFmpeg command executed successfully.\n";
    } else {
        // Command failed
        cerr << "Error executing FFmpeg command.\n";
    }
}


void colorizeMP4() {
    string pathMP4 = "../resources/ouput22.mp4";

    // Open the MP4 file for reading
    cv::VideoCapture inputVideo(pathMP4);
    if (!inputVideo.isOpened()) {
        cerr << "Error opening input video file\n";
        exit(1);
    }

    // Create a VideoWriter object to write the output
    cv::VideoWriter outputVideo("../resources/colorized22.mp4", cv::VideoWriter::fourcc('X', '2', '6', '4'), FPS, cv::Size(WIDTH, HEIGHT));
    if (!outputVideo.isOpened()) {
        cerr << "Error opening output video file for writing\n";
        exit(1);
    }

    // Process each frame
    cv::Mat frame;
    while (inputVideo.read(frame)) {
        // Apply color manipulation (example: invert colors)
        cv::bitwise_not(frame, frame);

        // Write the modified frame to the output video
        outputVideo.write(frame);
    }
}


int main() {
    string pathBlackAndWhite = "../resources/Bosphorus_black_and_white.yuv";
    if (!ifstream(pathBlackAndWhite)) {
        // Generate a grayscale YUV file from a color one.
        cout << "Generating grayscaled YUV file..." << endl;
        grayScale(); // Call your function to generate the grayscale YUV file
        cout << "YUV file generated successfully!" << endl;
    }

    convertYUVtoMP4();

    colorizeMP4();

    return 0;
}
