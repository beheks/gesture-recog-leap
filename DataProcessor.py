import PoseData
import math
import lib.Leap.Leap as Leap

class_name = "default" 

class DataProcessor():
 
    def __init__(self):
        pass
     
    def get_features(self, frame):

        result = list()
                
        hand = frame.handList.rightmost
                
        # Radius of hand sphere Feature #0
        result.append(hand.sphereRadius)

        # Check if the hand has any fingers
        fingers = hand.fingersList

        # Number of fingers Feature #1
        result.append(len(fingers)) 

        #Angle between adjacent fingers Features #2, #3, #4 and #5
        for i in range(1, len(fingers)):                        
            a = fingers[i-1].tipPosition - hand.palmPosition
            b = fingers[i].tipPosition - hand.palmPosition
            angle = self.calculate_angle(a, b)
            result.append(angle)
        for i in range(len(fingers) - 1, 4):
            if i >= 0:
                result.append(0.0)

        #Distance between fingertip and hand center Features #6, #7, #8, #9 and #10
        for finger in fingers:
            dist = self.distance(finger.tipPosition, hand.palmPosition)
            result.append(dist)
        for i in range(0, 5-len(fingers)):
            result.append(0.0)

        #Angle between finger vector (hand center -> fingertip) and hand normal Features #11, #12, #13, #14 and #15 
        for finger in fingers:
            a = finger.tipPosition - hand.palmPosition
            b = hand.palmNormal - hand.palmPosition
            angle = self.calculate_angle(a, b)
            result.append(angle)
        for i in range(0, 5-len(fingers)):
                result.append(0.0)
                
        return result

    def distance(self, pos1, pos2):
        a = pos1 - pos2
        dist = math.sqrt(float(a.x*a.x+a.y*a.y+a.z*a.z))
        return dist

    def calculate_angle(self, a, b):
        div = (math.sqrt(float(a.x*a.x+a.y*a.y+a.z*a.z))*math.sqrt(float(b.x*b.x+b.y*b.y+b.z*b.z)))
        if a == None or b == None or abs(div - 0.0) <= 0.0001:
            return 0.0

        return float(a.x*b.x+ a.y*b.y+ a.z*b.z)/div
    
