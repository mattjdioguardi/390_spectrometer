import numpy as np
import matplotlib.pylab as pt
import scipy
from scipy.signal import find_peaks

input = np.genfromtxt('test.csv',delimiter=',',skip_header=1)

voltages = np.zeros(len(input))
angles = np.zeros(len(input))

for i in range(len(input)):
    angles[i] = input[i][0]
    voltages[i] = input[i][1]

peaks, _ = find_peaks(-voltages, height = .5)
peaks2 = [2*x for x in peaks if 2*x < len(angles)]


pt.plot(angles[peaks], voltages[peaks], "x")
pt.plot(angles[peaks2], voltages[peaks2], "o")



print()

pt.plot(angles, voltages)
pt.show()
