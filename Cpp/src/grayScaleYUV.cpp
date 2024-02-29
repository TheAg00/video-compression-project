#include <iostream>
#include <fstream>
#include <vector>
#include <algorithm>
#include <filesystem>

#include "../include/header.h"

using namespace std;

namespace fs = filesystem;

constexpr int HEIGHT = 1080;
constexpr int WIDTH = 1920;

void convertToGrayscale(vector<unsigned char>& frameYUV) {
    // Set the values of U and V to 128, i.e., gray color
    fill(frameYUV.begin() + WIDTH * HEIGHT, frameYUV.begin() + WIDTH * HEIGHT * 5 / 4, 128); // U component
    fill(frameYUV.begin() + WIDTH * HEIGHT * 5 / 4, frameYUV.begin() + WIDTH * HEIGHT * 3 / 2, 128); // V component
}

void grayScale() {
    string pathYUV = "../resources/Bosphorus_1920x1080_120fps_420_8bit_YUV.yuv";
    // Read the YUV file.
    ifstream inputFile(pathYUV, ios::binary);

    if(!inputFile.is_open()) {
        cerr << "Error: Failed to open input file." << endl;
        exit(1);
    }

    // Calculate the size of a YUV frame
    size_t frameSize = WIDTH * HEIGHT * 3 / 2;

    // Get the size of the file
    inputFile.seekg(0, ios::end);
    streampos fileSize = inputFile.tellg();
    inputFile.seekg(0, ios::beg);

    // Read each frame one by one
    vector<unsigned char> frameData(frameSize); // Buffer to store one frame

    string pathBlackAndWhite = "../resources/Bosphorus_black_and_white.yuv";
    // Create the output YUV file for writing in binary mode
    ofstream outputFile(pathBlackAndWhite, ios::binary);
    if (!outputFile.is_open()) {
        cerr << "Error opening output file." << endl;
        inputFile.close();
        exit(1);
    }

    int frameNumber = 1;
    while(true) {
        inputFile.read(reinterpret_cast<char*>(frameData.data()), frameSize);

        // Check if the read operation was successful
        if (!inputFile) {
            // If not successful, check if it's the end of the file or an error
            if (inputFile.eof()) {
                // End of file reached
                break;
            }

            // Error occurred
            cerr << "Error: Failed to read frame " << frameNumber << endl;
            exit(1);

        }

        convertToGrayscale(frameData);
        // Write the modified frame to the output file
        outputFile.write(reinterpret_cast<const char*>(frameData.data()), frameSize);

        frameNumber++;
    }

    // Close the input and output files
    inputFile.close();
    outputFile.close();

    return;
}