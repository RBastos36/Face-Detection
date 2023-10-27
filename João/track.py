# Sistemas Avançados de Visão Industrial (SAVI 23-24)
# Grupo 6, DEM, UA
# Afonso Simões, nMec100090
# João Nogueiro, nMec111807
# Ricardo Bastos, nMec103983

import cv2
import numpy as np

class Detection():
    def __init__(self, left, right, top, bottom, id, stamp, name):
        self.left = left*2
        self.right = right*2
        self.top = top*2
        self.bottom = bottom*2
        self.cx = int((left + right)/2)*2
        self.cy = int((top + bottom)/2)*2
        self.detection_id = id
        self.stamp = stamp
        self.name = name

    def draw(self, image, color, draw_position='bottom', text=None):
        start_point = (self.left, self.top)
        end_point = (self.right, self.bottom)
        cv2.rectangle(image, start_point, end_point, color, 2)

        # if text is None:
        #     text = 'Det ' + self.detection_id

        if text is None:
            text = self.name

        if draw_position == 'bottom':
            position = (self.left, self.bottom + 30)
        else:
            position = (self.left, self.top-10)

        #cv2.putText(image, text, position, cv2.FONT_HERSHEY_SIMPLEX, 1, color, 2, cv2.LINE_AA)
        cv2.rectangle(image, (self.left, self.bottom + 35), (self.right, self.bottom), (0, 0, 255), cv2.FILLED)
        font = cv2.FONT_HERSHEY_DUPLEX
        cv2.putText(image, text, (self.left + 6, self.bottom + 29), font, 1.0, (255, 255, 255), 1)
    
