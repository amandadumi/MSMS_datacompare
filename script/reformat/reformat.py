# a script to automatically format the comparison table for the MSMS data
#Amanda Dumi
#08/25/16

from pandas import DataFrame, read_csv
import numpy as np
import pandas as pd

df = pd.read_csv('myexample.csv' ,names=['data1','id1','data2','id2','data3','id3','data4','id4','data5','id5'])
crosslink_mass= 344.038556
ids = [df['id1'],df['id2'],df['id3'],df['id4'],df['id5']]
mass = [df['data1'],df['data2'],df['data3'],df['data4'],df['data5']]
bf = pd.DataFrame()
bf= df['id2']
print bf
