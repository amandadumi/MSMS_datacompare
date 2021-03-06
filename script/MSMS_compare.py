## TODO: input file option

from pandas import DataFrame, read_csv
import numpy as np
import pandas as pd
import argparse
from argparse import RawTextHelpFormatter

class MSMS:
    def __init__(self):
        #parse command line input
        self.parse_input()
        #set list of file names to analyze
        self.gen_file_list()

    def parse_input(self):
        version_msg = """
        MSMS data compare script
        version: 2.0
        authors: Amanda Dumi and Shiv Upadhyay
        """

        input_msg = """Required format of .csv file:
        a) collected data in column 1
        b) the masses to compare to in column 5
        c) the identity of the ion in collumn 6
        """
        parser = argparse.ArgumentParser(
            description='{}/n/n{}'.format(version_msg,input_msg))

        parser.add_argument('-mf', '-mult_file',
        action="store",
        dest="file_list",
        help="To analyze multiple files.\n Provide with text file that contains a list of all files to analyze.",
        default = 'none')

        parser.add_argument('-sf', '-single_file',
        action="store",
        dest="single_file",
        help="To analyze a single file. Provide with name of text file.",
        default = 'none')

        parser.add_argument('-ma', '-mass_accuracy',
        action="store",
        dest="mass_accuracy",
        help="mass accuracy in Daltons",
        default = 'no accuracy defined')

#TODO: add this to class variables¬ç
        parser.add_argument('-pid', '-protein_ID',
        action="store",
        dest="protein_id",
        help="protein id to be stored as note in output file",
        default = 'no accuracy defined')

#TODO: add this to class variables¬ç
        parser.add_argument('-notes', '-notes',
        action="store",
        dest="notes",
        help="a quoted statmenet to be placed in the output file",
        default = 'no accuracy defined')


        self.pars_res = parser.parse_args()
        self.file_list = self.pars_res.file_list
        self.single_file = self.pars_res.single_file
        self.mass_accuracy = float(self.pars_res.mass_accuracy)

    def gen_file_list(self):
        if self.file_list != 'none':
            with open(self.file_list, 'r') as f:
                self.file_names = f.readlines()
                for id,file in enumerate(self.file_names):
                    self.file_names[id] = file.replace('\n','')
        if self.single_file !='none':
            self.file_names = [self.single_file]

    def analyze(self):
        col_names = ['collected','retention time','','match?','mass','identity']
        for id,file in enumerate(self.file_names):
            print('beginning analysis of {}'.format(file))
            self.df = pd.read_csv('{}'.format(file), names=col_names)
            k=0
            self.df['match?'] = np.nan
            self.df[' '] = np.nan
            # self.df['retention time'] = np.nan
            self.df['extra_info'] = np.nan
            self.df['summary: mass'] = np.nan
            self.df['summary: match'] = np.nan
            self.df.iloc[0,7]= str('mass accuracy:')
            self.df.iloc[1,7]= self.mass_accuracy

            ##finds the length of masses to loop over
            stuff = len(self.df.iloc[self.df['mass'].fillna(0.0).nonzero()])
            c = []
            #looping over samples
            for i in range(len(self.df['collected'])):
                #occasional printing
                if i%50 == 0:
                    print('progress: {:5} of {:5}'.format(i, len(self.df['collected'])))
                for j in range(stuff):
                    error=np.abs((self.df.iloc[i,0])-self.df.iloc[j,4])
                    if error <= self.mass_accuracy:
                        #checking to see if sample has any previous matches
                        if self.df.iloc[i,3]!=np.nan:
                            #getting the sample identity
                            d=self.df.iloc[j,5]
                            # appending this to the sample list
                            c.append(d)
                            self.df.iloc[i,3] =  str(c).strip('[]')
                            self.df.iloc[k,8]= self.df.iloc[i,0]
                            self.df.iloc[k,9]= self.df.iloc[i,3]
                        # if no previous matches.
                        else:
                            d = str(self.df.iloc[j,5])
                            self.df.iloc[i,3]= self.df.iloc[k,9]= d
                            self.df.iloc[k,8]= self.df.iloc[i,0]
                            self.df.iloc[k,9]= self.df.iloc[i,3]
                            c.append(d)
                        k+=1
                            #resetting c vector for next sample
                            # placcing the mass into the summary collumn
                c=[]

            self.summary_df = self.df[['summary: mass','summary: match','extra_info']]
            self.write_output_file(file)

    def write_output_file(self,file):
        self.df.to_csv("{}_output.csv".format(file.replace('.csv',''),index=False))
        self.summary_df.to_csv("{}_summary.csv".format(file.replace('.csv',''),index=False))





if __name__ == "__main__":
    test = MSMS()
    print(test.file_names)
    test.analyze()
