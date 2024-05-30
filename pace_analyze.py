"""
pip install xmltodict
"""
import sys
import xmltodict
import numpy as np
import xml.etree.ElementTree as ET

from utils import open3dUtils, readCSV, pltUtils

data_dir = '../lvPace_2024_04_23_16_17_12/'

contact_model_file = 'Contact_Mapping_Model.xml'
map_point_localtion_file = 'Contact_Mapping/MapPointLocations.csv'
ecg_file = 'ECG_Waveforms_Filtered.csv'
catheter_file = 'EP_Catheter_Bipolar_Waveforms_Filtered.csv'

def plot_contact_mapping_model():
    tree = ET.parse(data_dir + contact_model_file)
    Contact_Mapping_Model_str = xmltodict.parse(ET.tostring(tree.getroot()))
    vertices_str = Contact_Mapping_Model_str['DIF']['DIFBody']['Volumes']['Volume']['Vertices']['#text']
    vertices_color = Contact_Mapping_Model_str['DIF']['DIFBody']['Volumes']['Volume']['Map_color']['#text']
    vertices = np.fromstring(sep=' ', string=vertices_str).reshape(-1, 3)
    vertices_color = np.fromstring(sep=' ', string=vertices_color)

    o3dutils = open3dUtils()
    pcd = o3dutils.draw_point_cloud(vertices, vertices_color)


def save_ECG_as_npz():
    print('Saving ECG as npz file')
    lines = readCSV(data_dir + ecg_file, delimiter=',', skiprows=84)
    line = lines[0]
    titles = ['timestamp'] + [line[ind] for ind in range(4, len(line)-1, 3)]
    data = []
    for line in lines[1:-1]:
        time_stamp = [float(line[1] + '.' + f"{int(line[2]):06}")]
        phases = [float(line[ind]) for ind in range(4, len(line)-1, 3)]
        data.append(np.array(time_stamp + phases))
    data = np.array(data)
    np.savez(data_dir + 'ECG_Waveforms_Filtered.npz', titles=titles, data=data) # save as npz file
    return data

def save_Catheter_Bipolar_Waveforms_as_npz():
    print('Saving Catheter_Bipolar_Waveforms as npz file')
    lines = readCSV(data_dir + catheter_file, delimiter=',', skiprows=145)
    line = lines[0]
    titles = ['timestamp'] + [line[ind] for ind in range(4, len(line)-1, 3)]
    data = []
    for line in lines[1:-1]:
        time_stamp = [float(line[1] + '.' + f"{int(line[2]):06}")]
        phases = [float(line[ind]) for ind in range(4, len(line)-1, 3)]
        data.append(np.array(time_stamp + phases))
    data = np.array(data)
    np.savez(data_dir + 'Catheter_Bipolar_Waveforms.npz', titles=titles, data=data) # save as npz file
    return data

def plot_ECG(localtion_ind=0):
    load_file = np.load(data_dir + 'ECG_Waveforms_Filtered.npz')
    titles = load_file['titles']
    data = load_file['data']
    map_point_localtion_lines = readCSV(data_dir + map_point_localtion_file, delimiter=',', skiprows=59)
    time_stamp = map_point_localtion_lines[localtion_ind][3]
    
    plot_length = int(1/0.0005)
    ecg_ind = np.argmin(np.abs(data[:, 0] - float(time_stamp)))
    plt_utils = pltUtils()
    axs = plt_utils.get_fig(grid=[3, 4])
    for ind in range(1, 13):
        axs[ind-1].plot(np.arange(plot_length), data[ecg_ind:ecg_ind+plot_length, ind])
        axs[ind-1].set_title(titles[ind])
    plt_utils.title('ECG')
    plt_utils.show()

def plot_bipolar(localtion_ind=0):
    load_file = np.load(data_dir + 'Catheter_Bipolar_Waveforms.npz')
    titles = load_file['titles']
    data = load_file['data']
    map_point_localtion_lines = readCSV(data_dir + map_point_localtion_file, delimiter=',', skiprows=59)
    time_stamp = map_point_localtion_lines[localtion_ind][3]
    
    plot_length = int(1/0.0005)
    start_ind = np.argmin(np.abs(data[:, 0] - float(time_stamp)))
    plt_utils = pltUtils()
    axs = plt_utils.get_fig(grid=[3, 3])
    for ind in range(1, 10):
        axs[ind-1].plot(np.arange(plot_length), data[start_ind:start_ind+plot_length, ind])
        axs[ind-1].set_title(titles[ind])
    plt_utils.title('Catheter_Bipolar_Waveforms')
    plt_utils.show()

# plot_contact_mapping_model()

# save_ECG_as_npz()
# save_Catheter_Bipolar_Waveforms_as_npz()

plot_ECG()
plot_bipolar()