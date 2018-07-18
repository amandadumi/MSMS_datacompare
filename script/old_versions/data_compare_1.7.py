#######################
# Analysis of MSMS data
# Amanda and Shiv
#1.7: summary of matches
#######################
from pandas import DataFrame, read_csv
import numpy as np
import pandas as pd

print('.csv file needs format of:')
print('a) your collected data in column 1')
print('b) the masses to compare to in column 4')
print('c) the identity of the ion in collumn 5')
print('')
name_of_file = str(input('Name of input CSV: '))
name_of_output =str(input('Name of output CSV: '))
error_criteria = str(input('Mass accuracy (in Daltons): '))
protein_ID = str(input('Protein ID: '))
amino_acid_sequence = str(input('Amino acid sequence: '))
error_criteria= float(error_criteria)

df = pd.read_csv( '{}.csv'.format(name_of_file),names = ['collected','','retention time','match?','mass','identity'])
k=0
df['match?'] = np.nan
df[' '] = np.nan
df['retention time']= np.nan
df['extra_info'] = np.nan
df['summary: mass'] = np.nan
df['summary: match'] = np.nan
df.iloc[0,7]= str('mass accuracy:')
df.iloc[1,7]= error_criteria
df.iloc[2,7]= str('Protein ID:')
df.iloc[3,7]= protein_ID
df.iloc[4,7]= str('Amino acid sequence:')
df.iloc[5,7]= amino_acid_sequence

stuff = df['mass'].isnull().sum()
stuff = len(df.iloc[df['mass'].fillna(0.0).nonzero()])
c = []
for i in range(len(df['collected'])):
    if i%50 == 0:
        print('progress:',i,'out of ', len(df['collected']))
    for j in range(stuff):
        error=(np.abs((df.iloc[i,0]-df.iloc[j,4])/df.iloc[j,4]))*100
        if error <= error_criteria:
            k+=1
            if df.iloc[i,3]!=0:
                d=df.iloc[j,5]
                c.append(d)
                df.iloc[i,3] =  str(c).strip('[]')
                df.iloc[k,8]= df.iloc[i,0]
                df.iloc[k,9]= df.iloc[i,3]
            else:
                df.iloc[i,3]= str(df.iloc[j,5])
                df.iloc[k,8]= df.iloc[i,0]
                df.iloc[k,9]= df.iloc[i,3]
            
    c=[]    

# test to see if summary is working
stuff2 = len(df.iloc[df['match?'].fillna(0.0).nonzero()])
stuff3 = len(df.iloc[df['summary: mass'].fillna(0.0).nonzero()])
print(stuff2)
print(stuff3)
df.to_csv("{}.csv".format(name_of_output,index=False))
