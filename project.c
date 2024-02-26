#include <stdio.h>
#include <stdlib.h>

// Καθορίζουμε το ύψος και το πλάτος του βίντεο.
#define HEIGHT 1080
#define WIDTH 1920

// int yplane[HEIGHT][WIDTH];

// Μετατρέψουμε το yuv frame σε grayscaled.
void convertToGrayscale(unsigned char *yuvFrame) {
    int i;
    for (i = WIDTH * HEIGHT + 1; i < WIDTH * HEIGHT * 5 / 4 + 1; i++) {
        // Θέτουμε τις τιμές των u και v σε 128, δηλαδή γκρίζο χρώμα.
        yuvFrame[i] = 128; // U στοιχείο.
    }

    for (i = WIDTH * HEIGHT * 5 / 4 + 1; i < WIDTH * HEIGHT * 3 / 2; i++) {
        yuvFrame[i] = 128; // V στοιχείο.
    }
}


int main() {
    // Διαβάζουμε το yuv αρχείο.
    FILE *fd = fopen("./Bosphorus_1920x1080_120fps_420_8bit_YUV_RAW/Bosphorus_1920x1080_120fps_420_8bit_YUV.yuv", "rb");
    FILE *fd2 = fopen("Bosphorus.yuv", "wb");

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
        // Μετατρέπουμε το frame σε grayscaled.
        convertToGrayscale(yuvFrame);

        // Αντιστοιχούμε κάθε ασπρόμαυρο frame στο fd2 αρχείο.
        fwrite(yuvFrame, 1, frameSize, fd2);


    }


    // Κλείνουμε το αρχείο και αποδεσμεύουμε τη μνήμη.
    fclose(fd);
    fclose(fd2);
    free(yuvFrame);

    return 0;
}