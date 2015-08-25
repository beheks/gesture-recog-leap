import lib.yaml as yaml
import lib.Leap.Leap as Leap

class User(yaml.YAMLObject):
    yaml_tag = u'!User'
    def __init__(self, name = ""):
        self.name = name

    def __repr__(self):
        return "%s(name=%r)" % (
            self.__class__.__name__, self.name)

class Pose(yaml.YAMLObject):
    yaml_tag = u'!Pose'
    def __init__(self, name = ""):
        self.name = name

    def __repr__(self):
        return "%s(name=%r)" % (
            self.__class__.__name__, self.name)

class Frame(yaml.YAMLObject):
    yaml_tag = u'!Frame'
    def __init__(self, user, pose, framedata):
        self.user = user
        self.pose = pose
        self.frameData = framedata
    def __repr__(self):
        return "%s(user=%r, pose=%r, framedata=%r)" % (
            self.__class__.__name__, self.user, self.pose, self.framedata)

class FrameData(yaml.YAMLObject):
    yaml_tag = u'!FrameData'        
    def __init__(self, frame):
        
        #send the hands data to handList for it to structure
        self.handList = handList(frame.hands)
        self.framerate = frame.current_frames_per_second
        
    def __repr__(self):
        return "%s(handList=%r, framerate=%r)" % (
            self.__class__.__name__, self.handList, self.framerate)

class handList(yaml.YAMLObject):
    yaml_tag = u'!handList'
    def __init__(self, hands):
        self.leftmost = Hand(hands.leftmost)
        self.rightmost = Hand(hands.rightmost)
        
    def __repr__(self):
        return "%s(leftmost=%r, rightmost=%r)" % (
            self.__class__.__name__, self.leftmost, self.rightmost)

class Hand(yaml.YAMLObject):
    yaml_tag = u'!Hand'        
    def __init__(self, hand):

        if not hand.is_valid:
            raise ValueError

        #Confidence the sensor has in its data
        self.confidence = hand.confidence
        
        #direction from the palm position toward the fingers
        self.direction = Vector(hand.direction)
        
        #send the finger list to FingerList so it can structure the data
        self.fingersList = FingersList(hand.fingers)
        
        self.grabStrenght = hand.grab_strength
        
        #if the hand in question if valid, and if its either the left or the right hand
        self.isLeft = hand.is_left
        self.isRight = hand.is_right
        self.isValid = hand.is_valid
        
        #palm normal, position, velocity, width
        self.palmNormal = Vector(hand.palm_normal)
        self.palmPosition = Vector(hand.palm_position)
        self.palmVelocity = Vector(hand.palm_velocity)
        self.palmWidth = hand.palm_width
        
        #pinch strength, inversely proportional to the distance between index and thumb
        self.pinchStrength = hand.pinch_strength
        
        #center and radius of the sphere formed the hand curvature
        self.sphereCenter = Vector(hand.sphere_center)
        self.sphereRadius = hand.sphere_radius
        
        #stabilized position of the palm, considers previous frames
        self.stabilizedPalmPosition = Vector(hand.stabilized_palm_position)
        
        self.timeVisible = hand.time_visible

    def __repr__(self):

        return "%s(confidence=%r, direction=%r, fingerList=%r, grabStrenght=%r, isLeft=%r, isRight=%r, isValid=%r, palmNormal=%r, palmPosition=%r, palmVelocity=%r, palmWidth=%r, pinchStrength=%r, sphereCenter=%r, sphereRadius=%r, stabilizedPalmPosition=%r, timeVisible=%r)" % (
            self.__class__.__name__, self.confidence, self.direction, self.fingerList, self.grabStrenght, self.isLeft, self.isRight, self.isValid, self.palmNormal, self.palmPosition, self.palmVelocity, self.palmWidth, self.pinchStrength, self.sphereCenter, self.sphereRadius, self.stabilizedPalmPosition, self.timeVisible)
            
    def getFingersList(self):
        return self.fingersList.getFingersList()
    
    def getExtendedFingersList(self):
        return self.fingersList.getExtendedFingersList()

class FingersList(yaml.YAMLObject):
    yaml_tag = u'!FingerList'        

    def __init__(self, fingers):

        for f in fingers:
            if f.type() == Leap.Finger.TYPE_THUMB:
                self.thumb = Finger(f, False)
            if f.type() == Leap.Finger.TYPE_INDEX:
                self.index = Finger(f, False)
            if f.type() == Leap.Finger.TYPE_MIDDLE:
                self.middle = Finger(f, False)
            if f.type() == Leap.Finger.TYPE_RING:
                self.ring = Finger(f, False)
            if f.type() == Leap.Finger.TYPE_PINKY:
                self.pinky = Finger(f, False)

        for f in fingers.extended():
            if f.type() == Leap.Finger.TYPE_THUMB:
                self.thumb.isExtended = True
            elif f.type() == Leap.Finger.TYPE_INDEX:
                self.index.isExtended = True
            elif f.type() == Leap.Finger.TYPE_MIDDLE:
                self.middle.isExtended = True
            elif f.type() == Leap.Finger.TYPE_RING:
                self.ring.isExtended = True
            elif f.type() == Leap.Finger.TYPE_PINKY:
                self.pinky.isExtended = True

    def __repr__(self):
        return "%s(thumb=%r, index=%r, middle=%r, ring=%r, pinky=%r)" % (
            self.__class__.__name__, self.thumb, self.index, self.middle, self.ring, self.pinky)
            
    def getFingersList(self):
        fingers = list()
        fingers.append(self.thumb)
        fingers.append(self.index)
        fingers.append(self.middle)
        fingers.append(self.ring)
        fingers.append(self.pinky)
        return fingers
        
    def getExtendedFingersList(self):
        fingers = list()
        
        if self.thumb.isExtended:
            fingers.append(self.thumb)
            
        if self.index.isExtended:
            fingers.append(self.index)
            
        if self.middle.isExtended:
            fingers.append(self.middle)
        
        if self.ring.isExtended:
            fingers.append(self.ring)
        
        if self.pinky.isExtended:
            fingers.append(self.pinky)
            
        return fingers

class Finger(yaml.YAMLObject):
    yaml_tag = u'!Finger'        
    def __init__(self, finger, is_extended):

        if not finger.is_valid:
            raise ValueError

        self.isExtended = is_extended
        self.metacarpal = Bone(finger.bone(Leap.Bone.TYPE_METACARPAL))
        self.proximal = Bone(finger.bone(Leap.Bone.TYPE_METACARPAL))
        self.intermediate = Bone(finger.bone(Leap.Bone.TYPE_INTERMEDIATE))
        self.distal = Bone(finger.bone(Leap.Bone.TYPE_DISTAL))
        self.tipPosition = Vector(finger.tip_position)

    def __repr__(self):
        return "%s(isExtended=%r, metacarpal=%r, proximal=%r, intermediate=%r, distal=%r)" % (
            self.__class__.__name__, self.isExtended, self.metacarpal, self.proximal, self.intermediate, self.distal)
    
    def getBones(self):
        bones = list()
        
        bones.append(self.metacarpal)
        bones.append(self.proximal)
        bones.append(self.intermediate)
        bones.append(self.distal)
        
        return bones


class Bone(yaml.YAMLObject):
    yaml_tag = u'!Bone'        
    def __init__(self, bone):

        if not bone.is_valid:
            raise ValueError

        self.direction = Vector(bone.direction)
        self.length = bone.length
        self.nextJoint = Vector(bone.next_joint)
        self.prevJoint = Vector(bone.prev_joint)
        self.width = bone.width

    def __repr__(self):
        return "%s(direction=%r, length=%r, nextJoint=%r, prevJoint=%r, width=%r)" % (
            self.__class__.__name__, self.direction, self.length, self.nextJoint, self.prevJoint, self.width)

class Vector(yaml.YAMLObject):
    yaml_tag = u'!Vector'        
    def __init__(self, vector):

        if not vector.is_valid:
            raise ValueError
            #TODO: Should it be return None?

        self.x = vector.x
        self.y = vector.y
        self.z = vector.z
        self.pitch = vector.pitch
        self.yaw = vector.yaw
        self.roll = vector.roll

    def __repr__(self):
        return "%s(x=%r, y=%r, z=%r, pitch=%r, yaw=%r, roll=%r)" % (
            self.__class__.__name__, self.x, self.y, self.z, self.pitch, self.yaw, self.roll)
            
    def __sub__(self, other):
        vec = Leap.Vector(self.x - other.x, self.y - other.y, self.z - other.z)
        vec.pitch = self.pitch - other.pitch
        vec.roll = self.roll - other.roll
        vec.yaw = self.yaw - other.yaw
        return Vector(vec)

