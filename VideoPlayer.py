
import threading
import cv2
from ThreadedQueue import ThreadQueue

def extractFrames(fileName, outputBuffer, maxFramesToLoad=9999):
    # initialize frame count
    count = 0
    # open the video clip
    vidcap = cv2.VideoCapture(fileName)
    # read first image
    success,image = vidcap.read()

    print(f'Reading frame {count} {success}')
    while(success):
        # add the frame to the buffer
        outputBuffer.put(image)

        success,image = vidcap.read()
        print(f'Reading frame {count} {success}')
        count += 1
    outputBuffer.put('~')
    print('Frame extraction complete')

def convertToGrayscale(colored, grayscaled):
    # initialize frame count
    count = 0
    # load the frame
    frame = colored.get()
    while frame is not '~':
        print(f'Converting frame {count}')

        # convert the image to grayscale
        grayscaleFrame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # put grayscaleFrame into grayscaled queue
        grayscaled.put(grayscaleFrame)

        count+=1
        # get the next frame from colored
        frame = colored.get()
    grayscaled.put('~')

def displayFrames(inputBuffer):
    # initialize frame count
    count = 0
    # load the frame
    frame = inputBuffer.get()
    # go through each frame in the buffer until the buffer is empty
    while frame is not '~':
        print(f'Displaying frame {count}')
        # Display the frame in a window called "Video"
        cv2.imshow('Video', frame)

        # Wait for 42 ms and check if the user wants to quit
        if cv2.waitKey(42) and 0xFF == ord("q"):
            break

        count += 1
        # Get the next frame from inputBuffer
        frame = inputBuffer.get()
    print('Finished displaying all frames')
    # Cleans up the windows
    cv2.destroyAllWindows()

file = 'clip.mp4'

colored = ThreadQueue()
grayscaled = ThreadQueue()

extract = threading.Thread(target = extractFrames, args = (file, colored, 72))
convert = threading.Thread(target = convertToGrayscale, args = (colored, grayscaled))
display = threading.Thread(target = displayFrames, args = (grayscaled,))

extract.start()
convert.start()
display.start()