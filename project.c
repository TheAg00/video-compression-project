#include <stdio.h>
#include <stdlib.h>

// Καθορίζουμε το ύψος και το πλάτος του βίντεο.
#define HEIGHT 1080
#define WIDTH 1920
#define BLOCK_SIZE 4

int yplane[HEIGHT][WIDTH];

int main() {
    // Διαβάζουμε το yuv αρχείο.
    FILE *fd = fopen("./Bosphorus_1920x1080_120fps_420_8bit_YUV_RAW/Bosphorus_1920x1080_120fps_420_8bit_YUV.yuv", "rb");

    // Ελέγχουμε αν το αρχείο φορτώθηκε κανονικά.
    if (fd == NULL) {
        perror("Error opening video file");
        return 1;
    }

    // Υπολογίζουμε το μέγεθος κάθε yuv frame.
    size_t frameSize = WIDTH * HEIGHT * 3 / 2;

    // Δεσμεύουμε μνήμη για το yuv frame.
    unsigned char *yuvFrame = (unsigned char*) malloc(frameSize);

    if (yuvFrame == NULL) {
        printf("Error allocating memory.\n");
        fclose(fd);
        return 1;
    }

    // Κάνουμε iterate όλα τα frames του ασυμπίεστου ασπρόμαυρου βίντεο.
    while(fread(yuvFrame, 1, frameSize, fd) == frameSize) {

    }

    // Κλείνουμε το αρχείο και αποδεσμεύουμε τη μνήμη.
    fclose(fd);
    free(yuvFrame);

    return 0;
}