# Author : Qasim Wani
# License : MIT
# Date Written : 31st December, 2019
# Topic : Building a Predictive Arithemtic Calculator using BCI by clenching jaws to inducing absolute changes in electric potential of neural activity
# Objective : Calculates the number of Clenches in individual .csv file of EEG data caused by fluctuations in Electric Potential.
import numpy as np
import matplotlib.pyplot as plt
from scipy import fft, arange, signal
import pandas as pd
import os
import csv
#----------------------

EEG_FOLDER = "../../data/Clench/Official_Tests" #Test Folder
def find_files(PATH, ext):
    """
    Finds all the files in a particular directory. Return only .csv files.
    """
    files = []
    for r, d, f in os.walk(PATH):
        for file in f:
            if ext in file:
                files.append(os.path.join(r, file).replace("\\","/"))
    return files

files = find_files(EEG_FOLDER, ".csv") #List of all .csv files in the desired folder
def remove_meta_data(PATH):
    """
    Return:
    1. Changes in Electric potential based on Unix timestamp from
        the 5 channels of the Emotiv headset. 2 channels from the Frontal Lobe, 
        1 channel from the parietal lobe, and 2 from temporal lobe.
    2. Pandas Dataframe of the data reflected from (1).
    """
    reader = csv.reader(open(PATH, "rt"), delimiter='\t')
    i = 0
    one_file_data = []
    for line in reader:
        if(i > 0):
            one_file_data.append(line)
        i += 1
    one_file_data = np.array(one_file_data)
    columns = one_file_data[0][0].split(",")[3:8]
    row_data = []
    for rows in one_file_data[1:]:
        dtx = rows[0].split(",")[3:8]
        cont = []
        for x in dtx:
            cont.append(float(x))
        row_data.append(cont)
    dataframe = pd.DataFrame(row_data, columns=columns)
    return np.array(row_data), dataframe

def data_DF_dir(list_PATH):
    """
    Returns all the data from a given set of path files and its associated pandas dataframe object.
    """
    raw_data = []
    dataframes = []
    for file in list_PATH:
        rd, dfob = remove_meta_data(file)
        raw_data.append(rd)
        dataframes.append(dfob)
    return raw_data, dataframes

bci_data, bci_df = data_DF_dir(files)
friendly_name = [x.split("/")[-1].split("_")[0] for x in files]

def count_peaks_validation(peaks, x, threshold_vertical):
    count = 0
    for states in peaks:
        if(states > threshold_vertical):
            count += 1
    plt.plot(x)
    plt.xlabel("Time (sample_rate (128) per second expansion)")
    plt.ylabel("Amplitude")
    plt.title("Time Domain Chart of Peak count (One-Sided f(x))", y=1.08)
    return count

def ease(index, distance, start_index, threshold_vertical, height, width):
    dataCV = []
    for i in range(0, 5):
        x = bci_data[index].T[i][start_index:]
        x = abs(x - np.average(x))  # biasing.
        peaks, props = signal.find_peaks(x, distance=distance, height=height, width=width)
        count = count_peaks_validation(peaks, x, threshold_vertical)
        dataCV.append(count)
    count = round(np.array(dataCV).mean())
    return int(friendly_name[index]), count

def decode_brain_wave():
    count = []
    for i in range(len(friendly_name)):
        p,t = ease(i, 249, 309, 50, 200, 1)
        count.append(t)
    opA = ''
    opB = ''
    operation = ['+','-','*','/']
    result = 0

    check = False
    for x in count:
        x = int(x)
        if(x < 10):
            if(check == True):
                opB += str(x)
            else:
                opA += str(x)
        else:
            operation = operation[int(x%10)]
            check = True
    opA = int(opA)
    opB = int(opB)

    result = opA / opB
    if(operation == '+'):
        result = opA + opB
    elif(operation == '-'):
        result = opA - opB
    elif(operation == '*'):
        result = opA * opB
    print("Calculating Result :\n")
    print("Operand A : ", opA)
    print("\nOperan B : ", opB)
    print("\nOperation : ", operation)
    print("\n", opA, operation, opB, " = ", result)
    
    return result

if __name__ == "__main__":
    result = decode_brain_wave()