import lib.Leap.Leap as Leap
from PoseData import FrameData
from DataProcessor import DataProcessor
from RandomForest import ClassifierRandomForest
import numpy
import cv2

class CaptureFrame(Leap.Listener):

    def __init__(self, windowArg):
        Leap.Listener.__init__(self)
        self.dataProcessor = DataProcessor()
        self.classifier = ClassifierRandomForest()
        self.showWindow = False
        
        self.usePool = True
        self.poolSize = 5
        self.pool = list()
        
        self.timeToShowResult = False
        
        if windowArg == "-w" or windowArg == "--window":
            self.showWindow = True

    def on_init(self, controller):
        self.frames = list()
        self.begin = True
        self.time = True
        print "Frame Capture Initialized"

    def on_disconnect(self, controller):
        print "Frame Capture Disconnected"
        
    def on_exit(self, controller):
        print "Exited"

    def on_frame(self, controller):
        #Get current frame seen by Leap Motion
        frame = controller.frame()

        if frame.is_valid and not frame.hands.is_empty:
        
            #Allocate a FrameData object that structures the data from the frame and 
            #use the DataProcessor class to calculate the features used to classify
            frameData = FrameData(frame)
            current_frame = self.dataProcessor.get_features(frameData)
            
            if current_frame != None:  
                if self.usePool:
                    #If a pooling system is being used, let it accumulate to the set amount before sending to the classifier
                    if len(self.pool) == self.poolSize:
                        result = self.classifier.determine_class(self.pool)
                        self.timeToShowResult = True
                        self.pool = list()
                    else:
                        self.pool.append(current_frame)
                        
                #if every frame is being classified, send straight to the classifier
                else:
                    result = self.classifier.determine_class_one_frame(current_frame)
                    self.timeToShowResult = True
                
                #show result
                if self.timeToShowResult == True:
                    self.showResult(result)
                    self.timeToShowResult = False
                
    def showResult(self, result):
    
        if self.showWindow:
            cv2.namedWindow("Real Time Hand Gesture Recognition", cv2.CV_WINDOW_AUTOSIZE)
            self.backgroundImage = numpy.zeros((1080, 1800, 3), dtype=numpy.uint8)
            cv2.putText(self.backgroundImage, result, (170,540), cv2.FONT_HERSHEY_SIMPLEX, 3, (122, 122, 122), 5)
            cv2.imshow("Real Time Hand Gesture Recognition", self.backgroundImage)
            cv2.waitKey(13)
            self.background_image = numpy.zeros((1080, 1800, 3), dtype=numpy.uint8)
                
        else:
            print result

