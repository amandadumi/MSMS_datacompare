#######################
# Analysis of MSMS data
# Amanda and Shiv
# analyze a list of files
#######################
from pandas import DataFrame, read_csv
import numpy as np
import pandas as pd

print('Required format of .csv file:')
print('a) collected data in column 1')
print('b) the masses to compare to in column 5')
print('c) the identity of the ion in collumn 6')
print('  ')
filetype= str(input('do you have more than one file to analyze(y/n): '))

def manyfiles():
    print('\n Ensure you have created a .txt file listing all files to analyze called \'allfiles.txt\' \n')
    error_criteria = str(input('Mass accuracy (in Daltons): '))
    error_criteria= float(error_criteria)
    a = np.loadtxt('allfiles.txt',dtype=bytes,delimiter='\n').astype(str)
    for m in range(len(a)-3):
        print('Beginning analysis of', a[m])
        #    name_of_file = str(input('Name of input CSV: '))
        #    name_of_output =str(input('Name of output CSV: '))
        #    error_criteria = str(input('Mass accuracy (in Daltons): '))
        #    protein_ID = str(input('Protein ID: '))
        #    amino_acid_sequence = str(input('Amino acid sequence: '))
        df = pd.read_csv('{}'.format(a[m]), names = ['collected','','retention time','match?','mass','identity'])
        k=0
        df['match?'] = np.nan
        df[' '] = np.nan
        df['retention time'] = np.nan
        df['extra_info'] = np.nan
        df['summary: mass'] = np.nan
        df['summary: match'] = np.nan
        df.iloc[0,7]= str('mass accuracy:')
        df.iloc[1,7]= error_criteria
        #df.iloc[2,7]= str('Protein ID:')
        #df.iloc[3,7]= protein_ID
        #df.iloc[4,7]= str('Amino acid sequence:')
        #df.iloc[5,7]= amino_acid_sequence
        stuff = df['mass'].isnull().sum()
        stuff = len(df.iloc[df['mass'].fillna(0.0).nonzero()])
        c = []
        for i in range(len(df['collected'])):
            if i%50 == 0:
                print('progress:',i,'out of ', len(df['collected']))
            for j in range(stuff):
                error=(np.abs((df.iloc[i,0])-df.iloc[j,4])/df.iloc[j,4])*100
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
        df2 = df[['summary: mass','summary: match','extra_info']]
        df.to_csv("{}_output.csv".format(a[m].replace('.csv',''),index=False))
        df2.to_csv("{}_summary.csv".format(a[m].replace('.csv',''),index=False))

def onefile():
    name_of_file = str(input('Name of input CSV: '))
    error_criteria = str(input('Mass accuracy (in Daltons): '))
    error_criteria= float(error_criteria)
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
            error=(np.abs((df.iloc[i,0])-df.iloc[j,4])/df.iloc[j,4])*100
            if error <= error_criteria:
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
                k+=1
        c=[]
    df2 = df[['summary: mass','summary: match','extra_info']]
    df.to_csv("{}_output.csv".format(name_of_file,index=False))
    df2.to_csv("{}_summary.csv".format(name_of_file,columns=[8,9],index=False))
    stuff2 = len(df.iloc[df['match?'].fillna(0.0).nonzero()])
    stuff3 = len(df.iloc[df['summary: mass'].fillna(0.0).nonzero()])

good_input = False
while good_input == False:
    if filetype =='y':
        manyfiles()
        good_input = True
    elif filetype =='n':
        onefile()
        good_input = True
    else:
        filetype= str(input('do you have more than one file to analyze(y/n): '))
