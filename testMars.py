import sys
import unittest
import MarsMain
import doctest

testObject = MarsMain.Rover(1, 1, 1, "E", False)
coordTest = MarsMain.CoordPlane(1, 7, 7)

class TestRover(unittest.TestCase):

    def test_constructor(self):
        assert type(MarsMain.Rover(2, 3, 4,  "N", False)) is type(testObject)
        """
        Test the constructor 
        """
    def test_processDirection(self):
        self.assertEquals("N",testObject.processDirection("L")[2])
        self.assertEquals(2, testObject.processDirection("M")[1])
        self.assertEquals("E", testObject.processDirection("R")[2])
        """
        Test the different type of instructions and the output
        """

class TestCoord(unittest.TestCase):

    def test_constructor(self):
        assert type(MarsMain.CoordPlane(1, 4, 4)) is type(coordTest)
        """
        Test the constructor 
        """

class FunctionTest(unittest.TestCase):

    def test_validatePlane(self):
        self.assertEquals(True, MarsMain.validatePlane((3, 4, "N"), 5, 5))
        """
        Test function validatePlane() outcome
        """

    def test_cordniateValue(self):
        self.assertTrue(MarsMain.cordniateValue(testObject.x_location, testObject.y_location, coordTest.x_max, coordTest.y_max))
        """
        Test function cordniateValue() outcome
        """



if __name__ == "__main__":

    unittest.main()
