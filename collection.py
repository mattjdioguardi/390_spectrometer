#!/usr/bin/env python

import Ebert
import u6
import numpy as np
import pandas as pd
import matplotlib.pylab as plt
import scipy
from scipy.signal import find_peaks
import time


def sweep(start_in_steps, end_in_steps, step_size):
        spectrometer.moveTo(-start_in_steps)

        steps = int(np.ceil((end_in_steps - start_in_steps)/step_size))
        voltages = np.zeros(steps)
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
    points = int(np.ceil(100/step_size))
    fine_peaks = np.zeros((len(peaks),2,points))
    all_angles = np.zeros(0)
    all_voltages = np.zeros(0)


    for i in range(len(peaks)):
        fine_peaks[i] = sweep(positions[peaks[i]]+50,positions[peaks[i]]-50,step_size)
        all_angles.concatenate((all_angles,fine_peaks[i][0]))
        all_voltages.concatenate((all_voltagesfine_peaks[i][1]))

    return all_angles, all_voltages, fine_peaks





if __name__ == '__main__':
    spectrometer = Ebert.Ebert('COM3')
    DAQ = u6.U6()
    spectrometer.moveTo(0)

    start = int(input("starting angle:"))*25600
    end = int(input("end angle:"))*25600
    step = int(input("step size:"))
    positions, voltages = sweep(start,end,step)
    fine_angles, fine_voltages, fine_data = refine(positions,voltages,1)

    df = pd.DataFrame()
    df["angles"] = fine_angles
    df["voltages"] = fine_voltages

    df1 = pd.DataFrame()
    for i in range(len(fine_data)):
        df1["peak " + str(i) + " step#"] = fine_data[i][0]
        df1["peak " + str(i) + " voltage"] = fine_data[i][1]

    df = pd.concat([df,df1], axis=1)
    time = datetime.now().strftime("%d-%m-%Y_%H:%M:%S")
    df.to_csv("Ebert_" + time + ".csv", index=False)











    e.moveTo(0)
    e.close()