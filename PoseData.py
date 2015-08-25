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
        self.handList = HandList(frame.hands)
        self.framerate = frame.current_frames_per_second
        
    def __repr__(self):
        return "%s(handList=%r, framerate=%r)" % (
            self.__class__.__name__, self.handList, self.framerate)

class HandList(yaml.YAMLObject):
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
        
        #direction from the palm position toward the fingers
        self.direction = Vector(hand.direction)
        
        #send the finger list to FingerList so it can structure the data
        self.fingersList = list()
        for finger in hand.fingers:
            self.fingersList.append(Finger(finger))
        
        #palm normal, position, velocity, width
        self.palmNormal = Vector(hand.palm_normal)
        self.palmPosition = Vector(hand.palm_position)
        self.palmVelocity = Vector(hand.palm_velocity)
        
        #center and radius of the sphere formed the hand curvature
        self.sphereCenter = Vector(hand.sphere_center)
        self.sphereRadius = hand.sphere_radius
        
        #stabilized position of the palm, considers previous frames
        self.stabilizedPalmPosition = Vector(hand.stabilized_palm_position)
        
        self.timeVisible = hand.time_visible

    def __repr__(self):

        return "%s(confidence=%r, direction=%r, fingerList=%r, grabStrenght=%r, isLeft=%r, isRight=%r, isValid=%r, palmNormal=%r, palmPosition=%r, palmVelocity=%r, palmWidth=%r, pinchStrength=%r, sphereCenter=%r, sphereRadius=%r, stabilizedPalmPosition=%r, timeVisible=%r)" % (
            self.__class__.__name__, self.confidence, self.direction, self.fingerList, self.grabStrenght, self.isLeft, self.isRight, self.isValid, self.palmNormal, self.palmPosition, self.palmVelocity, self.palmWidth, self.pinchStrength, self.sphereCenter, self.sphereRadius, self.stabilizedPalmPosition, self.timeVisible)

class Finger(yaml.YAMLObject):
    yaml_tag = u'!Finger'        
    def __init__(self, finger):

        if not finger.is_valid:
            raise ValueError

        self.tipPosition = Vector(finger.tip_position)

    def __repr__(self):
        return "%s(isExtended=%r, tipPosition=%r)" % (
            self.__class__.__name__, self.isExtended, self.tipPosition)

class Vector(yaml.YAMLObject):
    yaml_tag = u'!Vector'        
    def __init__(self, vector):

        if not vector.is_valid:
            raise ValueError

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

