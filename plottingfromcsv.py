import csv
import matplotlib.pyplot as plt
import numpy as np

def read_csv(filename):
    with open(filename, 'r') as csvfile:
        reader = csv.reader(csvfile)
        data = list(reader)
    return data

# 
# For my own reference:
# Real triggers start at around column 3029 (10.0567s) and end at 129703 (432.3033s)

# Colomn 0 : Time
# Colomn 1 : LE
LE = 1
# Colomn 2 : Fz
FZ = 2
# Colomn 3 : Pz
PZ = 3
# Colomn 4 : P3
P3 = 4
# Colomn 5 : P08
P08 = 5
# Colomn 6: P07
PO7 = 6
# Colomn 7 : Oz
OZ = 7
# Colomn 8: P4
P4 = 8
# Colomn 9 : Trigger

#

def create_electrode_data(data, oddball_array, i_start, i_end, t_duration, sampling_frequency, col_number):

    frames_to_capture = t_duration * sampling_frequency

    trigger_data = []
    oddball_data = []

    i = i_start
    odd_iterator = 0

    while i < i_end: #just to check the data
        row = data[int(i)]
        if row[9] == '1': 
            data_block = []
            for j in range(int(frames_to_capture)):
                j_row = data[int(i+j)]
                j_current_time = round ( float(j_row[0]) - float(row[0]), 5)
                data_block.append([j_current_time, float(j_row[col_number])])
            
            if oddball_array[odd_iterator] == 1:
                oddball_data.append(data_block)
            else:    
                trigger_data.append(data_block)

            odd_iterator += 1
            i += frames_to_capture
        else:
            i += 1

    return trigger_data, oddball_data

#averaging and plotting

def plot_average(data, subtraction=0):
    avg_values = np.zeros(len(data[0]))
    sum_times, _ = zip(*data[0])

    for block in data:
        _, values = zip(*block)
        avg_values += np.array(values)

    avg_values /= len(data)
    avg_values -= subtraction

    plt.plot(sum_times, avg_values)



def plot_overlapping(data):
    for block in data:
        times, values = zip(*block)
        plt.plot(times, values)


if __name__ == '__main__':
    i_start = 3029 #when the experiment actually starts.
    i_end = 85088
    t_duration = 0.7
    sampling_frequency = 3/0.01 # rows/second
    col_number = P3
    oddball_array = [1, 0, 0, 0, 0,
                    0, 0, 0, 1, 0,
                    0, 0, 0, 0, 1,
                    0, 1, 0, 0, 0,
                    0, 0, 0, 1, 0,
                    1, 0, 0, 0, 0,
                    1, 0, 0, 0, 0,
                    0, 0, 0, 1, 0,
                    0, 0, 0, 1, 0,
                    0, 0, 0, 0, 1,
                    1, 0, 0, 0, 0,
                    1, 0, 0, 0, 0,
                    0, 1, 0, 0, 0,
                    0, 1, 0, 0, 0,
                    0, 0, 1, 0, 0,
                    0, 0, 0, 0, 1,
                    0, 0, 0, 0, 1,
                    0, 0, 0, 1, 0,
                    0, 0, 0, 0, 1,
                    0, 0, 0, 0, 1,
                    0, 1, 0, 0, 0,
                    0, 0, 0, 1, 0,
                    0, 1, 0, 0, 0,
                    0, 0, 1, 0, 0,
                    0, 1, 0, 0, 0,
                    0, 1, 0, 0, 0,
                    0, 1, 0, 0, 0,
                    0, 0, 0, 0, 1,
                    0, 0, 1, 0, 0,
                    0, 0, 1, 0, 0,
                    0, 0, 0, 1, 0,
                    0, 0, 1, 0, 0,
                    0, 0, 0, 0, 1,
                    0, 0, 1, 0, 0,
                    0, 0, 0, 1, 0,
                    1, 0, 0, 0, 0,
                    0, 0, 1, 0, 0,
                    0, 1, 0, 0, 0,
                    0, 0, 1, 0, 0,
                    0, 0, 0, 0, 1]
    
    filename = r'full_12_oddball_ak_raw.csv' 
    data = read_csv(filename)   

    pz_data, pz_oddball_data = create_electrode_data(data, oddball_array, i_start, i_end, t_duration, sampling_frequency, col_number)
    plot_average(pz_data)
    plot_average(pz_oddball_data)

    print(len(pz_data), len(pz_oddball_data), len(pz_data)+len(pz_oddball_data), len(oddball_array))
    
    plt.show()