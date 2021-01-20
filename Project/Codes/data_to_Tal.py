import numpy as np
from os import listdir
from os.path import isfile, join
import pandas as pd
import matplotlib.pyplot as plt
from FFClust import IOFibers
import os

def get_list_of_files(directory):
    files = [f for f in listdir(directory) if isfile(join(directory, f))]
    dirs = [f for f in listdir(directory) if not isfile(join(directory, f))]
    return files, dirs

# directory = '/home/cocobio/Documents/ARCHI_Database/'
directory = 'D:/Codes/UDEC/Database/2020/ARCHI/'
fiber_dir = '/OverSampledFibers/'
transform_dir_file = '/TransformMatrices/T2_to_Tal_tr_tmp.trm'

files, subjects = get_list_of_files(directory)
subjects.sort()
fiber_data = []
distance = []
n_fibers = []

for subject in subjects:
    print('Processing', subject)
    subject_fibers_path = directory + subject + fiber_dir
    subject_fibers_talairach_matrix = directory + subject + transform_dir_file

    fibers, tmp = get_list_of_files(subject_fibers_path)
    del tmp
    
    fibers = [f for f in fibers if f.endswith('.bundles') and f.find("_centroids") != -1]

    for f_path in fibers:
        f = subject_fibers_path + f_path
        f_tal = f[:f.rindex('/')+1]+'Final/'+f[f.rindex('/')+1:f.find('.bundles')]+"_Tal"+f[f.find('.bundles'):]

        if not os.path.exists(f_tal[:f_tal.rindex('/')]):
            os.makedirs(f_tal[:f_tal.rindex('/')])

        # print("python talairach/talairach.py "+f+" "+f_tal+" "+subject_fibers_talairach_matrix)
        os.system("python talairach/talairach.py "+f+" "+f_tal+" "+subject_fibers_talairach_matrix)

    #     break
    # break