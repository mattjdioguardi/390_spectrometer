#!/usr/bin/env python

import numpy as np
import pandas as pd
from datetime import datetime

fine_peaks = np.zeros((60,2,5))

for i in range(len(fine_peaks)):
    fine_peaks[i][0] = [i]

all_angles = np.zeros(0)
all_voltages = np.zeros(0)




for i in range(len(fine_peaks)):
    all_angles =  np.concatenate((all_angles, fine_peaks[i][0]))
    all_voltages = np.concatenate((all_voltages, fine_peaks[i][1]))

df = pd.DataFrame()
df["angles"] = all_angles
df["voltages"] = all_voltages

df1 = pd.DataFrame()

for i in range(len(fine_peaks)):
    df1["peak " + str(i) + " step#"] = fine_peaks[i][0]
    df1["peak " + str(i) + " voltage"] = fine_peaks[i][1]

df = pd.concat([df,df1], axis=1)

time = datetime.now().strftime("%d-%m-%Y_%H:%M:%S")
df.to_csv("yee_" + time + ".csv", index=False)



print(datetime.now())
dt_string = datetime.now().strftime("%d/%m/%Y %H:%M:%S")

#


#print(fine_peaks)