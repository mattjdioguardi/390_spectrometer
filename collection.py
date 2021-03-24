#!/usr/bin/env python

#importing all needed libraries
import Ebert
import u6
import numpy as np
import pandas as pd
import matplotlib.pylab as plt
from scipy.signal import find_peaks
from datetime import datetime
import time

#function that takes starting step number, ending step number, and a step size
#then sweeps through that range returning a list of positions and a list of
#voltages lined up by index of the two arrays
def sweep(start_in_steps, end_in_steps, step_size):
        spectrometer.moveTo(-start_in_steps)#move to staring pos

        #calulates the # of data points based on range and step size
        steps = int(np.ceil((end_in_steps - start_in_steps)/step_size))
        voltages = np.zeros(steps)#probably could just make 2d array but names are nice
        angles = np.zeros(steps)

        #moves the ebert and collects the voltage and position at each point
        #saving to the respective arrays
        for i in range(steps):
            spectrometer.moveLeft(step_size)
            time.sleep(0.06)
            voltages[i] = DAQ.getAIN(0)
            positions[i] = spectrometer.position()
            time.sleep(0.005)

        #returns the two arrays
        return positions, voltages


#given a list of positions and voltages finds all the peaks and then
#collets data in a small range around those peaks with a new step size
def refine(positions, voltages, step_size):
    peaks, _ = find_peaks(-voltages, height = .5)
    points = int(np.ceil(100/step_size))
    fine_peaks = np.zeros((len(peaks),2,points))
    all_angles = np.zeros(0)
    all_voltages = np.zeros(0)

    #for each peak collects data 50 steps on either side with a given step size
    #adds this data to both the 2d array seperated by peak and to one long list
    #for ease of plotting
    for i in range(len(peaks)):
        fine_peaks[i] = sweep(positions[peaks[i]]+50,positions[peaks[i]]-50,step_size)
        all_angles.concatenate((all_angles,fine_peaks[i][0]))
        all_voltages.concatenate((all_voltagesfine_peaks[i][1]))

    #returns all three arrays
    return all_angles, all_voltages, fine_peaks


if __name__ == '__main__':
    #ebert/ labjact setup
    spectrometer = Ebert.Ebert('COM3')
    DAQ = u6.U6()
    spectrometer.moveTo(0)

    #read in star/end/step size from the user
    start = int(input("starting angle:"))*25600
    end = int(input("end angle:"))*25600
    step = int(input("step size:"))

    #sweeps according to the input
    positions, voltages = sweep(start,end,step)
    #refines the data with a step size of 1
    fine_angles, fine_voltages, fine_data = refine(positions,voltages,1)

    #data frame of all refined data in a row
    df = pd.DataFrame()
    df["angles"] = fine_angles
    df["voltages"] = fine_voltages

    #data frame of each peaks data separated
    df1 = pd.DataFrame()
    for i in range(len(fine_data)):
        df1["peak " + str(i) + " step#"] = fine_data[i][0]
        df1["peak " + str(i) + " voltage"] = fine_data[i][1]


    #combines the two frames and saves them to a csv marked by the current
    #date and time
    df = pd.concat([df,df1], axis=1)
    time = datetime.now().strftime("%d-%m-%Y_%H:%M:%S")
    df.to_csv("Ebert_" + time + ".csv", index=False)











    e.moveTo(0)
    e.close()
