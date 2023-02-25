import cv2
import numpy as np
import keras
import imutils
from solver import *

def imgsudoku(imgfile):

    classes = np.arange(0, 10)

    model = keras.models.load_model("model-OCR.h5")
    input_size = 48

    def get_perspective(img, location, height = 900, width = 900):
        pts1 = np.float32([location[0], location[3], location[1], location[2]])
        pts2 = np.float32([[0, 0], [width, 0], [0, height], [width, height]])

        matrix = cv2.getPerspectiveTransform(pts1, pts2)
        result = cv2.warpPerspective(img, matrix, (width, height))
        return result

    def get_InvPerspective(img, masked_num, location, height = 900, width = 900):
        pts1 = np.float32([[0, 0], [width, 0], [0, height], [width, height]])
        pts2 = np.float32([location[0], location[3], location[1], location[2]])

        matrix = cv2.getPerspectiveTransform(pts1, pts2)
        result = cv2.warpPerspective(masked_num, matrix, (img.shape[1], img.shape[0]))
        return result

    def find_board(img):
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        bfilter = cv2.bilateralFilter(gray, 13, 20, 20)
        edged = cv2.Canny(bfilter, 30, 180)
        keypoints = cv2.findContours(edged.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        contours  = imutils.grab_contours(keypoints)

        newimg = cv2.drawContours(img.copy(), contours, -1, (0, 255, 0), 3)

        contours = sorted(contours, key=cv2.contourArea, reverse=True)[:15]
        location = None
        
        for contour in contours:
            approx = cv2.approxPolyDP(contour, 15, True)
            if len(approx) == 4:
                location = approx
                break
        result = get_perspective(img, location)
        return result, location

    def split_boxes(board):
        rows = np.vsplit(board,9)
        boxes = []
        for r in rows:
            cols = np.hsplit(r,9)
            for box in cols:
                box = cv2.resize(box, (input_size, input_size))/255.0
                boxes.append(box)
        cv2.destroyAllWindows()
        return boxes

    def displayNumbers(img, numbers, color=(255, 255, 255)):
        W = int(img.shape[1]/9)
        H = int(img.shape[0]/9)
        for i in range (9):
            for j in range (9):
                if numbers[(j*9)+i] !=0:
                    cv2.putText(img, str(numbers[(j*9)+i]), (i*W+int(W/2)-int((W/4)), int((j+0.7)*H)), cv2.FONT_HERSHEY_COMPLEX, 2, color, 2, cv2.LINE_AA)
        return img

    img = cv2.imread(imgfile)

    board, location = find_board(img)

    gray = cv2.cvtColor(board, cv2.COLOR_BGR2GRAY)
    rois = split_boxes(gray)
    rois = np.array(rois).reshape(-1, input_size, input_size, 1)

    prediction = model.predict(rois)

    predicted_numbers = []
    for i in prediction: 
        index = (np.argmax(i))
        predicted_number = classes[index]
        predicted_numbers.append(predicted_number)

    board_num = np.array(predicted_numbers).astype('uint8').reshape(9, 9)

    try:
        solved_board_nums = get_board(board_num)
        binArr = np.where(np.array(predicted_numbers)>0, 0, 1)
        flat_solved_board_nums = solved_board_nums.flatten()*binArr
        mask = np.zeros_like(board)
        solved_board_mask = displayNumbers(mask, flat_solved_board_nums)
        inv = get_InvPerspective(img, solved_board_mask, location)
        combined = cv2.addWeighted(img, 0.7, inv, 1, 0)
        
    except:
        print("Solution doesn't exist. Model misread digits.")

    combined = cv2.resize(combined, (600,600))
    cv2.imshow("Final Result", combined)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
