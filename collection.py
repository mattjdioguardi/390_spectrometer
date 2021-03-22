# -*- coding: utf-8 -*-
"""
Created on Tue Mar 16 15:58:29 2021

@author: pguest
"""




import Ebert
import u6
import numpy as np
import pandas as pd
import matplotlib.pylab as plt
import scipy
from scipy.signal import find_peaks
import time


def sweep(start_pos, end_pos, step_size):
        start_in_steps = start_pos
        end_in_steps = end_pos
        spectrometer.moveTo(start_in_steps)

        steps = int(np.ceil((end_in_steps - start_in_steps)/step_size))
        voltages = np.zeros(steps)
        voltages[:]=np.nan
        angles = np.zeros(steps)

        for i in range(steps):
            spectrometer.moveLeft(step_size)
            time.sleep(0.06)
            voltages[i] = DAQ.getAIN(0)
            positions[i] = spectrometer.position()
            time.sleep(0.005)

        return positions, voltages
        # plt.plot(angles, voltages)
        # plt.show()
        #
        # df = pd.DataFrame({"angles": angles, "voltage" : voltages})
        # df.to_csv("test.csv", index=False)

def refine(positions, voltages, step_size):
    peaks, _ = find_peaks(-voltages, height = .5)
    fine_data = np.zeros((len(peaks),2))

    for i in range(len(peaks)):
        fine_data[i] = sweep(positions[peaks[i]]+50,positions[peaks[i]]-50,step_size)





if __name__ == '__main__':
    spectrometer = Ebert.Ebert('COM3')
    DAQ = u6.U6()
    spectrometer.moveTo(0)

    start = int(input("starting angle:"))*25600
    end = int(input("end angle:"))*25600
    step = int(input("step size:"))
    positions, voltages = sweep(start,end,step)

    refine(positions,voltages,1)





    e.moveTo(0)
    e.close()