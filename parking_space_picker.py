import cv2
import pickle
import utils

from constants import (RECTANGLES_FILEPATH, IMAGE_TITLE, BASE_IMAGE_FILEPATH,
                       RECTANGLE_WIDTH, RECTANGLE_HEIGHT)


def on_mouse_click(pos_list, event, x, y, flags, params):
    if event == cv2.EVENT_LBUTTONDOWN:
        pos_list.append((x, y))

    elif event == cv2.EVENT_RBUTTONDOWN:
        for i, pos in enumerate(pos_list[:]):
            x1, y1 = pos
            if x1 < x < x1 + RECTANGLE_WIDTH and y1 < y < y1 + RECTANGLE_HEIGHT:
                pos_list.pop(i)

    with open(RECTANGLES_FILEPATH, "wb") as f:
        pickle.dump(pos_list, f)


if __name__ == "__main__":
    pos_list = utils.load_pos_list()
    while True:
        img = cv2.imread(BASE_IMAGE_FILEPATH)
        for pos in pos_list:
            cv2.rectangle(img, pos, (pos[0] + RECTANGLE_WIDTH, pos[1] + RECTANGLE_HEIGHT), (255, 0, 255), 2)
        cv2.imshow(IMAGE_TITLE, img)
        cv2.setMouseCallback(IMAGE_TITLE, lambda *args, **kwargs: on_mouse_click(pos_list, *args, **kwargs))
        cv2.waitKey(1)
