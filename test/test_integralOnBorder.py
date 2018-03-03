# -*- coding: utf-8 -*-
import unittest
import numpy as np

from element import IntegralOnBorder
from element import IntegralOnLine

def calc_volume(electrode, points, tri, values):
    """
    Adapter for testing
    :param points: Points coordinates
    :param tri: Number of points in triangle
    :param values: Values
    :return:
    """
    pass

def calc_border(electrode, points, polyline, values):
    """
    Adapter for testing
    :param points: Points coordinates
    :param tri: Number of points in triangle
    :param values: Values
    :return:
    """
    pass

TOLERANCE = 0.001
class TestIntegralOnBorder(unittest.TestCase):

    def test_volumetric_tri_equal(self):

        points1 = [[-3,-4], [3, 7], [6, 4]]
        points2 = [[6, 4], [-3, -4], [3, 7]]
        points3 = [[3, 7], [6, 4], [-3, -4]]


        val_tri = [1, 1, 1]
        electrode = [10, 10, 1]
        R = 25
        gi = 0.5

        triangle1 = IntegralOnBorder(electrode, R, gi, points1, val_tri)
        triangle2 = IntegralOnBorder(electrode, R, gi, points2, val_tri)
        triangle3 = IntegralOnBorder(electrode, R, gi, points3, val_tri)
        result1 = triangle1.calc_volume()  # (electrode, R, gi, points, val_tri1)#coord_tri1, val_tri1)
        result2 = triangle2.calc_volume()
        result3 = triangle3.calc_volume()


        self.assertIsNotNone(result1)
        self.assertIsNotNone(result2)
        self.assertIsNotNone(result3)
        #проверка на независимость от порядка обхода по границе
        self.assertAlmostEqual(result1, result2, delta=TOLERANCE)
        self.assertAlmostEqual(result1, result3, delta=TOLERANCE)

        coord_border1 = [[0, 1], [1, 2], [2, 0]]
        coord_border2 = [[1, 2], [2, 0], [0, 1]]
        coord_border3 = [[2, 0], [0, 1], [1, 2]]

        line1 = IntegralOnLine(electrode, R, gi,  points1, val_tri, coord_border1)
        line2 = IntegralOnLine(electrode, R, gi,  points2, val_tri, coord_border2)
        line3 = IntegralOnLine(electrode, R, gi,  points3, val_tri, coord_border3)

        result1 = triangle1.calc_volume() + \
                  line1.calc_border()
        result2 = triangle2.calc_volume() + \
                  line2.calc_border()
        result3 = triangle3.calc_volume() + \
                  line3.calc_border()
        print "res", result1, result2, result3#triangle1.calc_volume()+line1.calc_border()##result1, result2, result3

        self.assertAlmostEqual(0., np.abs(result1), delta=TOLERANCE)
        self.assertAlmostEqual(0., np.abs(result2), delta=TOLERANCE)
        self.assertAlmostEqual(0., np.abs(result3), delta=TOLERANCE)

    def test_volumetric_tri_equal2(self):
        points1 = [[-3, -4], [3, 7], [6, 4]]
        points2 = [[6, 4], [-3, -4], [3, 7]]
        points3 = [[3, 7], [6, 4], [-3, -4]]

        val_tri1 = [1, -2, 3]
        val_tri2 = [-2, 3, 1]
        val_tri3 = [3, 1, -2]
        electrode = [10, 10, 1]
        R = 1
        gi = 0.5

        triangle1 = IntegralOnBorder(electrode, R, gi, points1, val_tri1)
        triangle2 = IntegralOnBorder(electrode, R, gi, points2, val_tri2)
        triangle3 = IntegralOnBorder(electrode, R, gi, points3, val_tri3)

        result1 = triangle1.calc_volume()#(electrode, R, gi, points, val_tri1)#coord_tri1, val_tri1)
        result2 = triangle2.calc_volume()
        result3 = triangle3.calc_volume()


        self.assertIsNotNone(result1)
        self.assertIsNotNone(result2)
        self.assertIsNotNone(result3)

        self.assertAlmostEqual(result1, result2, delta=TOLERANCE)
        self.assertAlmostEqual(result1, result3, delta=TOLERANCE)


    def test_square1(self):
        points1 = [[0, 0], [1, 0], [0, 1]]
        points2 = [[1, 0], [1, 1], [0, 1]]
        val_tri1 = [1, 1, 0]
        val_tri2 = [1, 0, 0]
        electrode1 = [1.5, 0.5, 1]
        electrode2 = [-0.5,0.5, 1]
        R = 1
        gi = 0.5
        coord_border1 = [[0, 1], [1, 2], [2, 0]]
        coord_border2 = [[0, 1], [1, 2], [2, 0]]

        triangle1 = IntegralOnBorder(electrode1, R, gi, points1, val_tri1)
        triangle2 = IntegralOnBorder(electrode1, R, gi, points2, val_tri2)
        line1 = IntegralOnLine(electrode1, R, gi, points1, val_tri1, coord_border1)
        line2 = IntegralOnLine(electrode1, R, gi, points2, val_tri2, coord_border2)
        result1 = triangle1.calc_volume() + \
                  line1.calc_border()+ triangle2.calc_volume() + \
                  line2.calc_border()

        triangle3 = IntegralOnBorder(electrode2, R, gi, points1, val_tri1)
        triangle4 = IntegralOnBorder(electrode2, R, gi, points2, val_tri2)
        line3 = IntegralOnLine(electrode2, R, gi, points1, val_tri1, coord_border1)
        line4 = IntegralOnLine(electrode2, R, gi, points2, val_tri2, coord_border2)
        result2 = triangle3.calc_volume() + \
                  line3.calc_border()+ triangle4.calc_volume() + \
                  line4.calc_border()
        print result1, result2, result1+result2
        self.assertAlmostEqual(result1, -result2, delta=TOLERANCE)



if __name__ == '__main__':
    unittest.main()
