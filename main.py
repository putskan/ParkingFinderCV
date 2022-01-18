import sys
import cv2
import numpy as np
import cvzone
import utils

from constants import (VIDEO_FILEPATH, VIDEO_TITLE,
                       RECTANGLE_WIDTH, RECTANGLE_HEIGHT,
                       OUTPUT_FILEPATH, OPT_SAVE, OPT_DISPLAY)


def check_parking_space(img, processed_img, pos_list):
    """
    check and mark empty parking spaces on img
    :param img: np.array cv2 img
    :param processed_img: np.array cv2 img
    """
    empty_spaces = 0
    rec_thickness = 2

    for pos in pos_list:
        x, y = pos

        cropped_img = processed_img[y: y + RECTANGLE_HEIGHT, x: x + RECTANGLE_WIDTH]
        count = cv2.countNonZero(cropped_img)
        is_occupied = count > 800

        if is_occupied:
            rec_color = (0, 0, 255)
            rec_thickness = 2

        else:
            rec_color = (0, 200, 0)
            empty_spaces += 1

        cvzone.putTextRect(img, str(count), (x + 4, y + RECTANGLE_HEIGHT - 4),
                           scale=1, thickness=2, offset=0, colorR=rec_color)
        cv2.rectangle(img, pos, (pos[0] + RECTANGLE_WIDTH, pos[1] + RECTANGLE_HEIGHT), rec_color, rec_thickness)

    cvzone.putTextRect(img, f"{empty_spaces}/{len(pos_list)} parking spaces are available", (100, 50),
                       scale=1, thickness=1, colorR=(0, 200, 0), font=cv2.QT_FONT_NORMAL)


def get_processed_img(img):
    """
    create an image for processing
    :return: np.array image
    """
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    img_blur = cv2.GaussianBlur(img_gray, (3, 3), 1)
    img_threshold = cv2.adaptiveThreshold(img_blur, 255,
                                          cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                          cv2.THRESH_BINARY_INV, 25, 16)
    img_median = cv2.medianBlur(img_threshold, 5)
    dilate_kernel = np.ones((3, 3), np.uint8)
    return cv2.dilate(img_median, dilate_kernel, iterations=1)


def save_to_file(cap, pos_list):
    size = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)), int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fourcc = cv2.VideoWriter_fourcc(*"mp4v")
    video = cv2.VideoWriter(OUTPUT_FILEPATH, fourcc, 24.0, size)

    while cap.get(cv2.CAP_PROP_POS_FRAMES) != cap.get(cv2.CAP_PROP_FRAME_COUNT):
        success, img = cap.read()
        processed_img = get_processed_img(img)
        check_parking_space(img, processed_img, pos_list)
        video.write(img)

    video.release()
    print(f"{OUTPUT_FILEPATH} file created successfully")


def display(cap, pos_list):
    while True:
        if cap.get(cv2.CAP_PROP_POS_FRAMES) == cap.get(cv2.CAP_PROP_FRAME_COUNT):
            cap.set(cv2.CAP_PROP_POS_FRAMES, 0)

        success, img = cap.read()
        processed_img = get_processed_img(img)
        check_parking_space(img, processed_img, pos_list)
        cv2.imshow(VIDEO_TITLE, img)
        cv2.waitKey(1)


if __name__ == "__main__":
    if len(sys.argv) != 2 or sys.argv[1] not in [OPT_DISPLAY, OPT_SAVE]:
        print(f"usage: main.py {OPT_DISPLAY}/{OPT_SAVE}")
    else:
        cap = cv2.VideoCapture(VIDEO_FILEPATH)
        pos_list = utils.load_pos_list()

        if sys.argv[1] == OPT_DISPLAY:
            display(cap, pos_list)

        if sys.argv[1] == OPT_SAVE:
            save_to_file(cap, pos_list)
