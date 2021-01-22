import sys
import os
import json
'''
MarsMain.py
By: Derek Hernandez
Mars Rover Challenge Problem
########################################################
Goals:
    -Take a .txt file as input
    -.txt file contains a specific format that will set up plateau and rover
    
            5 5
            1 2 N
            LMLMLMLMM
    -Parse .txt file and return the final location of the rover in a specific format 
            1 3 N 
            5 1 E
Summery: 
    After reading and rereading the instruction for this project, I felt the best way conquer this task is by slowly parsing 
    data line by line; feeding that data into an algorithm; the algorithm will feed in through specific filters; after filter
    data then modify and store into Object Arrays.
Running:
    MarsMain.py
    python MarsMain..py input.txt -a,d,j
    
    -a: Standard output, coordinates and direction
    -d: debugging, will display all coordinates of each rover
    -j: will display a standard output and will serialize all coordinates to a json file 
    
    testMars.py
    python testMars.py -v
    
    will display all tests
'''

RoverArray = []
coordArray = []
countRover = 0
countPlane = 0
ROTATE_RIGHT = {"N":"E", "E":"S", "S":"W", "W":"N"}
ROTATE_LEFT = {"N":"W", "W":"S", "S":"E", "E":"N"}

'''
Attributes: 
    "RoverArray": An array where Rover Objects are stored   (array)
    "coordArray": An array where plateau's/Coordinate Plane's are stored    (array)
    "countRover": A counter for Rover Numbers, only incremented when a new instruction with a direction is parsed   (int)
    "countPlane": A counter for plateau's, only incremented when a new instruction with no direction is parsed     (int)
    "ROTATE_RIGHT": A Dictionary where if its deemed to rotate "R" (right), we feed the current direction as a key and get the 
    new updated direction value
    "ROTATE_LEFT": A Dictionary where if its deemed to rotate "L" (left), we feed the current direction as a key and get the 
    new updated direction value
'''

class Rover(object):
    '''
    class Rover()

    Creates a new Rover Object where it can store current number, direction, and location.
    '''
    roverNum = 0
    x_location = 0
    y_location = 0
    faceDirection = ""
    fellOff = False

    '''
    Attributes:
        "roverNum": Number Rover deployed   (int)
        "x_location": current x-axis location   (int)
        "y_location": current y-axis location   (int)
        "faceDirection": current cardinal direction    (str)
        "fellOff": Used to know if rover went out of bounds    (bool)
    '''

    def __init__(self, roverNum, x_location, y_location, faceDirection, fellOff):
        '''
        def __init__()
        A constructor of new Rover Objects

        -:parameter:
        "roverNum": Rover Number (int)
        "x_location": inital x-axis location (int)
        "y_location": inital y-axis location (int)
        "faceDirection": Inital direction (str)

        :return: A new defined Rover Object
        '''
        self.roverNum = roverNum
        self.x_location = x_location
        self.y_location = y_location
        self.faceDirection = faceDirection
        self.fellOff = fellOff

    def processDirection(self, instruction):
        '''
        processDirection()
        A primitive handeler. This function will get the pared instruction and direct it to the proper updating function

        -:parameter:
            "instruction": a single string that was parsed and will be used to update either direction or location (str)

        :return: updated (int x, int y, "Direction")
        '''
        # print self.__dict__
        # Left direction shift
        if(instruction.upper() == "L"):
            self.implementMoveLeft()
            return self.x_location, self.y_location, self.faceDirection
        #Right direction shift
        elif(instruction.upper() == "R"):
            self.implementMoveRight()
            return self.x_location, self.y_location, self.faceDirection
        #Movement
        elif(instruction.upper() == "M"):
            self.movementDirect()
            return self.x_location, self.y_location, self.faceDirection
        #else is important, it tells you when you've reached the end of the line or if there was an invalid
        else:
            return "Done"


    def implementMoveLeft(self):
        '''
        implementMoveLeft()
        Will update the Rover's current direction based on instruction "L", using pre-defined dictionary
        :return: rover.facedirection
        '''
        self.faceDirection = ROTATE_LEFT[self.faceDirection]


    def implementMoveRight(self):
        '''
        implementMoveRight()
        Will update the Rover's current direction based on instruction "R", using pre-defined dictionary
        :return: rover.facedirection
        '''
        self.faceDirection = ROTATE_RIGHT[self.faceDirection]

    def movementDirect(self):
        '''
        movementDirect()
        Will update the Rover's current direction based on instruction "M", will increment +-1 depending on direction

        :return: rover.x (int), rover.y (int)
        '''
        if (self.faceDirection == 'N'):
            self.NorthMove()
        elif (self.faceDirection == 'E'):
            self.EastMove()
        elif (self.faceDirection == 'S'):
            self.SouthMove()
        elif (self.faceDirection == 'W'):
            self.WestMove()
        return self.x_location, self.y_location


    def NorthMove(self):
        '''
        NorthMove()
        Will increment the location by +1, North is up
        :return: rover.y_location
        '''
        self.y_location += 1

    def SouthMove(self):
        '''
        SouthMove()
        Will decrement the location by -1, South is down
        :return: rover.y_location
        '''
        self.y_location -= 1

    def EastMove(self):
        '''
        EastMove()
        Will increment the location by +1, East is right
        :return: rover.x_location
        '''
        self.x_location += 1

    def WestMove(self):
        '''
        SouthMove()
        Will decrement the location by -1, West is left
        :return: rover.x_location
        '''
        self.x_location -= 1




class CoordPlane(object):
    '''
    CoordPlane()
    Creates a plane/plateau object that will keep track of all rover points and directions

    '''
    Plane = 0
    x_max = 0
    y_max = 0
    RoverLocation = []
    '''
       Attributes 
           "Plane": holds the current number of rovers in the plateau   (int)
           "x_max": x-axis max distance, defined in txt file    (int)
           "y_max": y-axis max distance, defined in txt file    (int)
           "RoverLocation": current location of rover   (array)
    '''

    def __init__(self, Rover, x_max, y_max):
        '''
        def __init__()
        A constructor of new Coordinate Plane Object

         -:parameter:
        "Rover": Rover Number (int)
        "x_max": max x-axis  (int)
        "y_max": max y-axis  (int)

        :return: defined CoordPlane()
        '''
        self.Plane = Rover
        self.RoverLocation = []
        self.x_max = x_max
        self.y_max = y_max

def validatePlane(temp,max_x, max_y):
    '''
    def validatePlane()
    Function that validate the rovers new location, making sure that it is within the limits defined

     -:parameter:
    "temp": Holds new location and direction of object Rover     (Rover)
    "max_x": Max range of x-axis defined by CoordPlane    (int)
    "max_y": Max range of y-axis defined by CoordPlane   (int)
    :return: True if new location is in valid range and digit (bool)
    '''
    if not(temp == "Done"):
        if (cordniateValue(temp[0], temp[1], max_x, max_y)):
            return 1
        else:
            return 0
    else:
        return -1

def cordniateValue(x, y, max_x,max_y ):
    '''
    def cordniateValue()
    Function that validate the rovers new location, making sure that it is within the limits defined

     -:parameter:
    "x": Holds new location of object Rover     (int)
    "y": Holds new location of object Rover     (int)
    "max_x": Max range of x-axis defined by CoordPlane    (int)
    "max_y": Max range of y-axis defined by CoordPlane   (int)
    :return: returns True if new location is confined by range  (bool)
    '''
    if ((0 <= x <= max_x)&(0 <= y <= max_y)):
        return True
    else:
        return False


def printFinal():
    '''
    def printFinal()
    Function that directs the user's choice in output.
        -a: Normal, expected output coordinates and direction
        -d: debug, all coordinates of each rover
        -j: Normal output, but with a json file

    :return: desired output
    '''
    if (sys.argv[2] == "-a"):
        printUI(RoverArray)
    elif(sys.argv[2] == "-d"):
        printDebug(coordArray, RoverArray)
    elif(sys.argv[2] == "-j"):
        printAPI(RoverArray, coordArray)
    else:
        print "Invalid argument"

def printUI(roverArray):
    '''
    def printUI()
    Function that prints user interface

    :return: desired print
    '''
    if not(type(roverArray) == None):
        print "Rover Output:\n", "#" * 15
        for a in roverArray:
            print " ", a.x_location, a.y_location, "",a.faceDirection

def printDebug(coordArray, roverArray):
    '''
    def printDebug()
    Function that prints debug, all rover coordinates

    :return: debugging print
    '''
    if not(type(coordArray) == None):
        for a in coordArray:
            print a.Plane, ":", a.RoverLocation
        for b in roverArray:
            print b.__dict__
def printAPI(roverArray, coordArray):
    '''
    def printAPI()
    Function that prints standard UI, but also exports all coordinates to a json file

    :return: Standard UI and json file
    '''
    printUI(roverArray)

    with open("sample.json", "w+") as outfile:
        for a in coordArray:
            json_object = json.dumps(a.__dict__, indent=3)
            outfile.write(json_object)

    outfile.close()

def main():
    '''
    main()
    Will run file by importing text file and parsing data through classes and functions

    :return: hopefully a working and correct output
    '''
    countRover = 0
    countPlane = 0
    fileName = sys.argv[1]

    #Open and read text file line by line
    with open(fileName, 'r') as f:
        for line in f:
            # Instruction starts with a position
            if (line[0].isdigit()):
                # Line in file is less than 5 instructions, making it the plane descriptor
                if (len(line.rstrip('\n')) < 5):
                    countPlane += 1
                    coordArray.append(CoordPlane(countPlane, int(line[0]), int(line[2])))

                #If its more than length of 5, its a new rover location
                else:
                    countRover += 1
                    RoverArray.append(Rover(countRover, int(line[0]), int(line[2]), line[4].upper(), False))
            # argument starts with a change in direction or movement
            elif(line[0].isalpha()):
                tempPair = [(0,0)]
                #Will parse through line character by character and process if its L, R, M
                for char in line.rstrip():
                    #Will process the instruction and update the Rover location and direction
                    #return the new updated location and direction
                    temp = RoverArray[countRover-1].processDirection(str(char))
                    #Will process updated rover into the plane
                    if (validatePlane(temp, coordArray[countPlane - 1].x_max, coordArray[countPlane - 1].y_max)):
                        #true if the new location is in bounds
                        tempPair.append((temp[0], temp[1]))
                    else:
                        #Fasle if it is out of bounds hence it Fell Off
                        RoverArray[countRover-1].fellOff = True
                #Will append the entire locations to the CoordPlane Object
                coordArray[countPlane - 1].RoverLocation.append(tempPair)

            else:
                #Place holder for a invaild material, "\n"
                placeHolder = 1
    f.close()
    printFinal()


if __name__ == "__main__":
    main()

