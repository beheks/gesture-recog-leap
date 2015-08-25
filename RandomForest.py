import sys
import math
import numpy as np
import cv2

class ClassifierRandomForest():

    def __init__(self):
        self.classifier = cv2.RTrees()
        self.classifier.load("classifier/forest")
        inp = open("classifier/classes.txt", "rU")
        self.number_class = eval(inp.readline())
        inp.close()

    def determine_class_one_frame(self, frame):
        frame = np.array(frame, dtype = np.float32)
        prediction_class = int(self.classifier.predict(frame))
        print prediction_class
        return self.number_class[prediction_class]


    def determine_class(self, frames):       
        classes_frames = list()
        winner = 0
        for row in range(0, len(self.number_class.keys())):
            classes_frames.append(0)
        for frame in frames:
            frame_array = np.array(frame, dtype = np.float32)
            print frame_array
            prediction_class = int(self.classifier.predict(frame_array))
            classes_frames[prediction_class] += 1
            if classes_frames[prediction_class] > classes_frames[winner]:
                winner = prediction_class
        return self.number_class[winner]

