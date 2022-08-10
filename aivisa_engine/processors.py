import cv2
import numpy as np
from math import ceil

from rembg import remove
from rembg.session_factory import new_session

from .enums import Paper_4R

cascade_classifier = cv2.CascadeClassifier(
    f"{cv2.data.haarcascades}haarcascade_frontalface_alt.xml")

# This function detect face and crop image based on the detected shape
def detect_face(image, shapeWidth, shapeHeight, faceHeight, draw=False):
    # Convert the image to grayscale for easier computation
    image_grey = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)

    detected_objects = cascade_classifier.detectMultiScale(image_grey,
                                                           scaleFactor=1.05,
                                                           minNeighbors=5,
                                                           minSize=(100, 100))

    if len(detected_objects) != 0:
        x, y, w, h = detected_objects[0]

        calculatedShapeWidth = w * shapeWidth // faceHeight
        calculatedShapeHeight = h * shapeHeight // faceHeight

        midX = x + w // 2
        midY = y + h // 2
        X = midX - (calculatedShapeWidth // 2)
        Y = midY - (calculatedShapeHeight // 2)
        W = calculatedShapeWidth
        H = calculatedShapeHeight

        if draw:
            cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 6)
            cv2.rectangle(image, (X, Y), (X + W, Y + H), (0, 0, 255), 6)
            return image

        X2 = min(X + W, image.shape[1])
        Y2 = min(Y + H, image.shape[0])
        X1 = max(0, X)
        Y1 = max(0, Y)
        return cv2.resize(image[Y1:Y2, X1:X2], (shapeHeight, shapeWidth))
    else:
        return None


# This function perform SOD to remove background from the input image
def remove_background(data):
    session = new_session("u2net_human_seg")

    output = remove(data=data,
                    alpha_matting=True,
                    # alpha_matting_foreground_threshold=300,
                    # alpha_matting_background_threshold=20,
                    alpha_matting_erode_size=5,
                    # only_mask=True,
                    post_process_mask=True,
                    session=session
                    )

    return output


# This function prepare printable image
def prepare_printable_4R(image):
    pageHeight, pageWidth, padding = Paper_4R.getSizePixel()

    blank_image = 255 * np.ones(shape=[pageHeight, pageWidth, 3], dtype=np.uint8)

    verticalImageCount = ceil((pageHeight - 2 * padding) // image.shape[0])
    horiszontalImageCount = ceil((pageWidth - 2 * padding) // image.shape[1])

    endRow = 0
    for row in range(verticalImageCount):
        startRow = endRow + padding
        endRow = startRow + image.shape[0]
        endCol = 0

        for col in range(horiszontalImageCount):
            startCol = endCol + padding
            endCol = startCol + image.shape[1]

            blank_image[startRow:endRow, startCol:endCol, :] = image


    return blank_image
