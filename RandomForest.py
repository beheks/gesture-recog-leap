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
        #convert to numpy array
        frame = np.array(frame, dtype = np.float32)
        
        #use opencv's implementation of Random Trees to classify
        prediction_class = int(self.classifier.predict(frame))
        
        return self.number_class[prediction_class]


    def determine_class(self, frames):       
        classes_frames = list()
        winner = 0
        
        #build classes list to decide most voted class in pool
        for row in range(0, len(self.number_class.keys())):
            classes_frames.append(0)
        
        #classify every frame to decide winner
        for frame in frames:
        
            #convert to numpy array
            frame_array = np.array(frame, dtype = np.float32)
            
            #use opencv's implementation of Random Trees to classify
            prediction_class = int(self.classifier.predict(frame_array))
            
            #check if the current class is the most common one
            classes_frames[prediction_class] += 1
            if classes_frames[prediction_class] > classes_frames[winner]:
                winner = prediction_class
                
        #return most common class
        return self.number_class[winner]

