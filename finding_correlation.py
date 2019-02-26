import pandas as pd
from pandas.plotting import scatter_matrix

import os
from argparse import ArgumentParser
import matplotlib.pyplot as plt

from matplotlib import rcParams
rcParams.update({'figure.autolayout': True})

import seaborn as sns


parser = ArgumentParser()
parser.add_argument("-f", "--file_name", required=True,
                    help="file name ")
parser.add_argument("-p", "--path", required=True,
                    help="the input path to data folder")


args = parser.parse_args()

# Paths to store the data
"""daily path :/home/ojas/Documents/independent_study_harry_perros/extracted_data/daily"""
"""daily path :/home/ojas/Documents/independent_study_harry_perros/extracted_data/weekly"""
"""daily path :/home/ojas/Documents/independent_study_harry_perros/extracted_data/monthly"""

os.chdir(args.path)

dataframe = pd.read_csv(args.file_name)


corr = dataframe.corr()
print(corr)

#plt.gcf().subplots_adjust(bottom=0.15)

sns.heatmap(corr,annot=True,
            xticklabels=corr.columns.values,
            yticklabels=corr.columns.values)

plt.show()

scatter_matrix(dataframe)

plt.xticks(rotation=90)
plt.yticks(rotation=90)

plt.show()
