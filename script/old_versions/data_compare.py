#######################
# Analysis of MSMS data
# Amanda and Shiv
#######################
from pandas import DataFrame, read_csv
import numpy as np
import pandas as pd

print('.csv file needs format of:')
print('a) your collected data in column 1')
print('b) the masses to compare to in column 4')
print('c) the identity of the ion in collumn 5')
name_of_file = str(input('Name of input CSV: '))
name_of_output =str(input('Name of output CSV: '))
error_criteria = str(input('Mass accuracy: '))
protein_ID = str(input('Protein ID: '))
amino_acid_sequence = str(input('Aminoa acid sequence: '))
error_criteria= float(error_criteria)

df = pd.read_csv( '{}.csv'.format(name_of_file),names = ['collected','','match?','mass','identity'])
k=0
df['match?'] = np.nan
df[' '] = np.nan
df['extra_info'] = np.nan
df.iloc[0,6]= str('Protein ID:')
df.iloc[1,6]= protein_ID
df.iloc[3,6]= str('Amino acid sequence:')
df.iloc[4,6]= amino_acid_sequence

stuff = df['mass'].isnull().sum()
stuff = len(df.iloc[df['mass'].fillna(0.0).nonzero()])
c = []
for i in range(len(df['collected'])):
    if i%50 == 0:
        print('progress:',i,'out of ', len(df['collected']))
    for j in range(stuff):
        error=(np.abs((df.iloc[i,0]-df.iloc[j,3])/df.iloc[j,3]))*100
        if error <= error_criteria:
            if df.iloc[i,2]!=0:
                d=df.iloc[j,4]
                c.append(d)
                df.iloc[i,2] =  str(c).strip('[]')
            else:
                df.iloc[i,2]= str(df.iloc[j,4])
    c=[]
df.to_csv("{}.csv".format(name_of_output,index=False))
