#include <iostream>
#include <fstream>
#include <vector>
#include <algorithm>
#include <opencv2/opencv.hpp>
// #define PY_SSIZE_T_CLEAN
#include <Python.h>



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


int main() {
    string pathBlackAndWhite = "../resources/Bosphorus_black_and_white.yuv";
    if (!ifstream(pathBlackAndWhite)) {
        // Generate a grayscale YUV file from a color one.
        cout << "Generating grayscaled YUV file..." << endl;
        grayScale(); // Call your function to generate the grayscale YUV file
        cout << "YUV file generated successfully!" << endl;
    }

    string pathMP4 = "../resources/black_and_white_22.mp4";

    if(!ifstream(pathMP4)) {
        cout << "Converting YUV to MP4..." << endl;
        convertYUVtoMP4(); // Call your function to convert the YUV file to MP4
        cout << "MP4 file generated successfully!" << endl;
    }

    // Initialize the Python interpreter
    Py_Initialize();

    // Run a Python script
    FILE* dataFile = fopen("../colorizeMP4.py", "r");
    if (!dataFile) {
        cerr << "Failed to open python script" << endl;
        exit(1);
    }

    // Execute the Python script
    PyRun_SimpleFile(dataFile, "../colorizeMP4.py");

    // Close the file
    fclose(dataFile);

    // Finalize the Python interpreter
    Py_Finalize();

    // colorizeMP4();

    return 0;
}
