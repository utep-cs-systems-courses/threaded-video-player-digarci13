
import cv2
import threading
from ThreadedQueue import ThreadQueue # separated ThreadQueue class for modularization


VIDEO = "../clip.mp4"  # video
DELIMITER = "\0"
FRAMEDELAY = 42


def extractFrames(filename, frameQueue):
    print('Extracting frames from: ', filename)
    i = 0
    video = cv2.VideoCapture(filename)
    success, image = video.read()  # Reading each frame 1 by 1

    print('Extracted Frame # {i} {success}')

    while success:
        frameQueue.put(image)
        success, image = video.read()
        i += 1
        print(f'Frame # {i} {success}')

    print('Frame extraction completed')
    frameQueue.put(DELIMITER)


def convertGrayscale(colorFrames, grayFrames):
    print("Converting to grayscale...")
    i = 0
    colorFrame = colorFrames.obtain()

    while colorFrame is not DELIMITER:
        print(f'Converting frame # {i}')

        grayFrame = cv2.cvtColor(colorFrame, cv2.COLOR_BGR2GRAY)  # convert the image to grayscale
        grayFrames.put(grayFrame)  # enqueue frame
        i += 1
        colorFrame = colorFrames.obtain()  # dequeue next frame

    print('Process completed')
    grayFrames.put(DELIMITER)


def displayFrames(frames):
    print('Displaying frames...')
    i = 0

    frame = frames.obtain()

    while frame is not DELIMITER:
        print(f'Displaying frame # {i}')
        cv2.imshow('Video Play', frame)

        if cv2.waitKey(FRAMEDELAY) and 0xFF == ord("q"):
            break

        i += 1
        frame = frames.obtain()

    print('Process completed')
    cv2.destroyAllWindows()  # Cleaning opened windows
if __name__ == "__main__":
    colorFrames = ThreadQueue()
    grayFrames = ThreadQueue()
    # three functions needed: extract frames, convert frames to grayscale,
    # and display frames at original framerate (24fps)
    extractThread = threading.Thread(target = extractFrames, args = (VIDEO, colorFrames))
    convertThread = threading.Thread(target = convertGrayscale, args = (colorFrames, grayFrames))
    displayThread = threading.Thread(target = displayFrames, args = (grayFrames,)) # <- needed to suppress error
    # start threads
    extractThread.start()
    convertThread.start()
    displayThread.start()