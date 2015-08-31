try:
    from adxl345 import ADXL345
    adxl345 = ADXL345()
except:
    pass
import time
import os
import csv
import datetime
from collections import deque
from itertools import izip, imap, combinations
from util import rolling_window, smooth_3d_measurements
import glob
from knockclassifier import KnockClassifier
import numpy

def print_measurements(axes):
    print("ADXL345 on address 0x%x:" % (adxl345.address))
    print("\tx = %.3fG" % axes['x'])
    print("\ty = %.3fG" % axes['y'])
    print("\tz = %.3fG" % axes['z'])



def record():
    a0 = a1 = adxl345.getAxes(True)
    measurements = []
    distances = deque(maxlen=30)
    distances += [30]
    while True:
        time.sleep(.02)
        a0 = a1
        a1 = adxl345.getAxes(True)
        distance = euclidean_distance(a0, a1)
        distances.append(distance)
        print_measurements(a1)
        measurements.append(axes_dict_to_tuple(a1))
        if numpy.mean(distances) < .02:
            print("Done recording")
            return measurements

def save_measurements(X, Y, directory='./training_data'):
    # Make directory
    if not os.path.exists(directory):
        print('Making %s dir' % directory)
        os.makedirs(directory)

    # Make files
    fname = datetime.datetime.now().strftime("%y%m%d_%H%M%S.csv")
    full_path = os.path.join(directory, fname)
    f = csv.writer(open(full_path, "w"))
    f.writerows(izip(X, Y))

def load_measurements(directory='./training_data'):
    X, Y = [], []
    for fname in glob.glob(os.path.join(directory, '*.csv')):
        for x, y in csv.reader(open(fname)):
            X.append(eval(x))
            Y.append(eval(y))
    return X, Y

def train(directory='./training_data'):
    X, Y = load_measurements(directory)
    classifier = KnockClassifier()
    for x, y in izip(X, Y):
        classifier.addData(max_distance(smooth_3d_measurements(x)), y)
    classifier.fit()
    return classifier

import matplotlib as mpl
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import matplotlib.pyplot as plt
def plot(measurements, label='movement'):
    mpl.rcParams['legend.fontsize'] = 10
    
    smoothed = smooth_3d_measurements(measurements, 10)
    X, Y, Z = [], [], []
    for x, y, z in smoothed:
        X += [x]
        Y += [y]
        Z += [z]

    fig = plt.figure()
    ax = fig.gca(projection='3d')
    ax.plot(X, Y, Z, label=label)
    ax.set_xlabel('X axis')
    ax.set_ylabel('Y axis')
    ax.set_zlabel('Z axis')
    ax.legend()
    plt.show()

if __name__ == "__main__":
    X, Y = [], []
    while True:
        x = record()
        val = raw_input('Valid Bump?: ')
        if val in ('q', 'Q'):
            save_measurements(X, Y)
            break
        X.append(x)
        if val in (1, 'y', 'Y'):
            Y.append(1)
        elif val in (0, 'n', 'N'):
            Y.append(0)
        else:
            print('Pass')
