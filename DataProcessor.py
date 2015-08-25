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
        if hand == None or hand.isLeft:
            return None

        #features #0, #1, #2, #3, #4 and #5 related to the hand
        result.append(hand.sphereRadius)
        result.append(hand.pinchStrength)
        result.append(hand.grabStrenght)
        
        numberFingers = len(hand.getFingersList())
        numberExtendedFingers = len(hand.getExtendedFingersList())
        
        result.append(numberFingers)
        result.append(numberExtendedFingers)
        result.append(numberFingers - numberExtendedFingers)

        fingers = hand.getFingersList()
        fingers_vectors = list()
        
        #fingers characteristics, if it is extended and length [#6.. #15]
        for finger in fingers:
            if finger.isExtended:
                result.append(1)
            else:
                result.append(0)
            result.append(self.distance(finger.distal.nextJoint, hand.palmPosition))
            fingers_vectors.append(self.subtract(finger.distal.nextJoint, hand.palmPosition))

        #angle between adjacent fingers features #16, #17, #18 and #19
        result += self.get_angle_adjacent(fingers_vectors)

        #angle between finger vector (hand center -> fingertip) and hand normal features #20, #21, #22, #23 and #24
        normal = self.subtract(hand.palmNormal, hand.palmPosition)
        result += self.get_angle_fingers_normal(fingers_vectors, normal)

        for finger in fingers:
            bones = finger.getBones()
            result += self.get_angle_adjacent_bones(bones)
            for bone in bones:
                result.append(bone.length)                
                result.append(bone.width)
                #usa direction tambem? igual ao vetor do dedo?
                
        return result

    def subtract(self, pos1, pos2):
        return PoseData.Vector(Leap.Vector(pos1.x - pos2.x, pos1.y - pos2.y, pos1.z - pos2.z))
        

    def distance(self, pos1, pos2):
        a = self.subtract(pos1, pos2)
        dist = math.sqrt(float(a.x*a.x+a.y*a.y+a.z*a.z))
        return dist

    def get_angle_adjacent_bones(self, vectors):
        angles = list()
        prev = self.subtract(vectors[0].prevJoint, vectors[0].nextJoint)
        for v in vectors[1:len(vectors)]:
            next = self.subtract(v.nextJoint, v.prevJoint)           
            angles.append(self.calculate_angle(prev, next))
            prev = self.subtract(v.prevJoint, v.nextJoint)
        return angles

    def get_angle_adjacent(self, vectors):
        angles = list()
        prev = vectors[0]
        for v in vectors[1:len(vectors)]:
            angles.append(self.calculate_angle(prev, v))
            prev = v
        return angles

    def get_angle_fingers_normal(self, vectors, n):
        angles = list()
        for v in vectors:
            angles.append(self.calculate_angle(v, n))
        return angles

    def calculate_angle(self, a, b):
        div = (math.sqrt(float(a.x*a.x+a.y*a.y+a.z*a.z))*math.sqrt(float(b.x*b.x+b.y*b.y+b.z*b.z)))
        if a == None or b == None or abs(div - 0.0) <= 0.0001:
            return 0.0

        return float(a.x*b.x+ a.y*b.y+ a.z*b.z)/div
    
