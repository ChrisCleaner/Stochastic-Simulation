# -*- coding: utf-8 -*-
"""
Created on Tue Nov 24 11:18:22 2020

@author: Gebruiker
"""

import numpy as np
import xlrd

import matplotlib.pyplot as plt
import seaborn as sns

import pandas as pd

import scipy.stats as stats
import os


location = os.getcwd().replace("\\","/") + "/results0.7579544029403025.csv"

def main():
    df = pd.read_csv(location)
    
    
    
    
    df1 = df.loc[df['servers'] == 1].drop("servers", axis =1)
    df2 = df.loc[df['servers'] == 2].drop("servers", axis = 1).reset_index()
    df3 = df.loc[df['servers'] == 4].drop("servers", axis = 1).reset_index()
    plot_df = pd.DataFrame()
    plot_df["1 Server"] = df1["times"]
    plot_df["2 Servers"] = df2["times"]
    plot_df["4 Servers"] = df3["times"]


    sns.relplot(data = plot_df)
    plt.show()
    
    print("levene test")
    print("Comparing all")
    print( stats.levene(df1['times'], df2['times'],df3['times']))
    print()
    ('Comparing 1 server to:')
    print('2', stats.levene(df1['times'], df2['times']))
    
    print('shapiro-wilk tests')
    
    print('1:', stats.shapiro(df1['times']))
    print('2', stats.shapiro(df2['times']))
    print('4', stats.shapiro(df2['times']))

    print()
    
    print("welch tests, of 1 and")
    print('2', stats.ttest_ind(df1['times'], df2['times'], equal_var = False))
    print('4', stats.ttest_ind(df1['times'], df3['times'], equal_var = False))
    


    print(stats.normaltest(df1['times']))
    print(stats.normaltest(df2['times']))
    print(stats.normaltest(df3['times']))
    
    
    

    

if __name__ == '__main__':
    main()