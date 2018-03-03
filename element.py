# -*- coding: utf-8 -*-
import numpy as np
import itertools


class IntegralOnBorder():

    def __init__(self, electrode, R, gi, point, value):

        self.x1 = point[0][0]
        self.y1 = point[0][1]
        self.x2 = point[1][0]
        self.y2 = point[1][1]
        self.x3 = point[2][0]
        self.y3 = point[2][1]
        self.v1 = value[0]
        self.v2 = value[1]
        self.v3 = value[2]
        self.result = 0
        self.a = electrode[0]
        self.b = electrode[1]
        self.h = electrode[2]
        self.R = R
        self.gi = gi
        self.sigma_b = gi * 7
        self.K = gi / (2 * np.pi * self.sigma_b)

    def M(self, x1, y1, x2, y2, x3, y3, ksi, eta):

        # N1 = 1-ksi-eta
        # N2 = ksi
        # N3 = eta
        x_new = x1 * (1 - ksi - eta) + x2 * ksi + x3 * eta
        y_new = y1 * (1 - ksi - eta) + y2 * ksi + y3 * eta
        # print x_new, y_new, K*(3*((x_new-a)**2+(y_new-b)**2)/((x_new-a)**2+(y_new-b)**2+h**2)**2.5-2./((x_new-a)**2+(y_new-b)**2+h**2)**1.5)
        return (3 * ((x_new - self.a) ** 2 + (y_new - self.b) ** 2)
                         / ((x_new - self.a) ** 2 + (y_new - self.b) ** 2 + self.h ** 2) ** 2.5 - 2. / (
        (x_new - self.a) ** 2 + (y_new - self.b) ** 2 + self.h ** 2) ** 1.5)

    def V(self, v1, v2, v3, ksi, eta):
        return (1 - ksi - eta) * v1 + ksi * v2 + eta * v3

    def calc_volume(self):
        A_k = np.abs(self.x1 * (self.y2 - self.y3) + self.x2 * (self.y3 - self.y1) + self.x3 * (self.y1 - self.y2)) / 2.
        M_ = np.array([self.M(self.x1, self.y1, self.x2, self.y2, self.x3, self.y3, 1. / 3,
                             1. / 3)])  # np.array([M(x1, y1, x2, y2, x3, y3, 0, 0.5), M(x1, y1, x2, y2, x3, y3, 0.5, 0), M(x1, y1, x2, y2, x3, y3, 0.5, 0.5)])
        V_ = np.array([self.V(self.v1, self.v2, self.v3, 1. / 3,
                             1. / 3)])  # np.array([V(v1, v2, v3, 0, 0.5), V(v1, v2, v3, 0.5, 0), V(v1, v2, v3, 0.5, 0.5)]) #
            # print S/3*np.dot(M_, V_)
        self.result +=  0.5*self.K * A_k * np.dot(M_, V_)  # S/3*np.dot(M_, V_)
        return self.result


class IntegralOnLine():
    def __init__(self, electrode, R, gi, points, values, line):
        self.points = points
        self.values = values
        self.line = line
        self.result = 0
        self.a = electrode[0]
        self.b = electrode[1]
        self.h = electrode[2]
        self.R = R
        self.gi = gi
        self.sigma_b = gi * 7
        self.K = gi / (2 * np.pi * self.sigma_b)




    def integr_on_border(self, x1, y1, z1, x2, y2, z2, v1, v2):
        x_mid = (x1 + x2) / 2.
        y_mid = (y1 + y2) / 2.
        v_mid = (v1 + v2) / 2.
        # print x1, x2
        if np.abs(x1 - x2) < 0.0001:
            x_param = (x2 - x1) * (y_mid - y1) / (y2 - y1) + x1
            return (x_param * (x_param - self.a) + y_mid * (y_mid - self.b)) / ((x_param - self.a) ** 2 + (
            y_mid - self.b) ** 2 + self.h ** 2) ** 1.5 * (1 + ((x2 - x1) / (y2 - y1)) ** 2) ** 0.5 * np.abs(y2 - y1) * v_mid
        else:
            y_param = (y2 - y1) / (x2 - x1) * (x_mid - x1) + y1
            return (x_mid * (x_mid - self.a) + y_param * (y_param - self.b)) / ((x_mid - self.a) ** 2 + (
            y_param - self.b) ** 2 + self.h ** 2) ** 1.5 * (1 + ((y2 - y1) / (x2 - x1)) ** 2) ** 0.5 * np.abs(x2 - x1) * v_mid


    def calc_border(self):
            for j in xrange(len(self.line)):
                #print self.line[j]
                x1, y1, z1 = self.points[self.line[j][0]][0], self.points[self.line[j][0]][1], 0
                x2, y2, z2 = self.points[self.line[j][1]][0], self.points[self.line[j][1]][1], 0
                v1 = self.values[self.line[j][0]]
                v2 = self.values[self.line[j][1]]
                #print x1, y1, x2, y2, v1, v2
                # sum_ += ((x1+x2)/2.*((x1+x2)/2.-a)+(y1+y2)/2.*((y1+y2)/2.-b))*((x1-x2)**2.+(y1-y2)**2.)**0.5/((((x1+x2)/2.-a)**2
                # +((y1+y2)/2.-b)**2+h**2)**3./2)*(v1+v2)/2.
                self.result += self.integr_on_border(x1, y1, z1, x2, y2, z2, v1, v2)
                #print self.result


            self.result = self.K / self.R * self.result
            #self.result = self.K * self.result
            return  self.result
