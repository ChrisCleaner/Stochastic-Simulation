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
from statsmodels.graphics.gofplots import qqplot


location = r'C:\Users\Gebruiker\OneDrive\Computational_Science\Year1_Semester1_Block2\Stochastic_Simulations\Assignment2\Results1\DES_results_1.csv'
location2 =  r'C:\Users\Gebruiker\OneDrive\Computational_Science\Year1_Semester1_Block2\Stochastic_Simulations\Assignment2\Results1\DES_results_2.csv'
location3 =  r'C:\Users\Gebruiker\OneDrive\Computational_Science\Year1_Semester1_Block2\Stochastic_Simulations\Assignment2\Results1\DES_results_3.csv'



def main():
    df = pd.read_csv(location)
    df2 = pd.read_csv(location2)
    df3 = pd.read_csv(location3)
    
    read(df)
    
    df.loc[df['servers'] == 1][df['lambda'] == 9.1]
    
def read(df):
    dfs = {}
    for lambd in [9.1, 9.3, 9.5, 9.7, 9.9, 9.99]:
        for serv in [1,2,4]:
            df1 = df.loc[df['servers'] == serv][df['lambda'] == lambd]
            dfs['{}+{}'.format(lambd, serv)] = df1
            
            
    print(len(dfs['9.3+2']))
      
    dfs['9.1+4']
    
    
    
    
    
    
def extra(df):
    
    
    fig, (ax1, ax2, ax3) = plt.subplots(1,3, figsize=(14,5))
    
    #plt.yscale('log')
    g1 = sns.boxplot(x="lambda", y="times", data=df.loc[df['servers'] == 1], ax = ax1)
    g2 = sns.boxplot(x="lambda", y="times", data=df.loc[df['servers'] == 2], ax = ax2)
    g3 = sns.boxplot(x="lambda", y="times", data=df.loc[df['servers'] == 4], ax = ax3)
    

    g2.set(ylabel=None)
    g3.set(ylabel=None)
    
    plt.show()
        
        
        
        
    
    df1 = df.loc[df['servers'] == 1]
    df2 = df.loc[df['servers'] == 2]
    df3 = df.loc[df['servers'] == 4]
    
    
    df4 = df1 - df2
    
    sns.displot(df, x = 'times', hue = 'servers')
    plt.show()
    
    plt.hist(df1['times'], bins = 60)
    
    sns.displot(df1, x="times", element="step")
    plt.show()
    sns.displot(df2, x="times", element="step")
    plt.show()
    sns.displot(df3, x="times", element="step")
    
    print("levene test")
    print("Comparing all")
    print( stats.levene(df1['times'], df2['times'],df3['times']))
    print()
    ('Comparing 1 server to:')
    print('2', stats.levene(df1['times'], df2['times']))
    
    print('shapiro-wilk tests')
    
    print('1:', stats.shapiro(df1['times']))
    print('2', stats.shapiro(df2['times']))
    print('4', stats.shapiro(df3['times']))
    

    print()
    
    print("welch tests, of 1 and")
    print('2', stats.ttest_ind(df1['times'], df2['times'], equal_var = False))
    print('4', stats.ttest_ind(df1['times'], df3['times'], equal_var = False))
    print('3 2 and 4', stats.ttest_ind(df2['times'], df3['times'], equal_var = False))
    


    print(stats.normaltest(df1['times']))
    print(stats.normaltest(df2['times']))
    print(stats.normaltest(df3['times']))
    
    