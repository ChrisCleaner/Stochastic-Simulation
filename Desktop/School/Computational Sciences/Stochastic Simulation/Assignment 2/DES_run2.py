# -*- coding: utf-8 -*-
"""
Created on Mon Nov 23 22:17:35 2020

@author: Gebruiker
"""
import simpy
import random
from numpy.random import choice
import numpy as np
import sys 
from scipy import stats
import os
import random



sys.path.append(os.getcwd().replace("\\","/"))

from DES_simulation2 import Server

location = (os.getcwd().replace("\\","/") + f"/results{random.random()}.csv")
import pandas as pd
import xlsxwriter


N = 100
mu = 10

n_clients = 2000
sorting_method = "Priority"


def main():
  
    #run with 1 server with lambda = 10
    lambd = 8
    n_servers = 1
    print('Run with %i server(s) with lambda = %i' % (n_servers, lambd))
    wait_times1 = multiple_simulations( lambd, n_servers, sorting_method)
    
    lambd = 16
    n_servers = 2
    print('Run with %i server(s) with lambda = %i' % (n_servers, lambd))
    wait_times2 = multiple_simulations(lambd, n_servers, sorting_method)
    
    lambd = 24
    n_servers = 4
    print('Run with %i server(s) with lambda = %i' % (n_servers, lambd))
    wait_times3 = multiple_simulations(lambd, n_servers, sorting_method)
    
    
    
    df1 = pd.DataFrame({'times': wait_times1, 'servers': [1 for i in range(len(wait_times1))]})
    df2 = pd.DataFrame({'times': wait_times2, 'servers': [2 for i in range(len(wait_times2))]})
    df4 = pd.DataFrame({'times': wait_times3, 'servers': [4 for i in range(len(wait_times3))]})
    
    df = df1.append(df2)
    df = df.append(df4)
    
    write_to_csv( df)
    

def multiple_simulations(lambd, n_servers, sorting_method):
    """
    Runs N DES  of class Server with the Simpy environment and takes as input:
    lambd = lambda, rate at which clietns arrive
    mu = the load of the server, i.e. handling time
    n_servers = the amount of servers, note here if we double the amount of servers we also double arrival rate lambda
    stop_time = length of time to run 
    seed = random seed
    
    returns list with waiting time of each client
    """ 
    times = []
    print('%done')
    
    for i in range(N):
        random.seed(i)
        #initialise environment
        env = simpy.Environment()
        #start processing
        processing = Server(env, lambd, mu, n_servers, n_clients, sorting_method)
        env.run()
        #print('clients helped', processing.start)
        times.append(np.mean(processing.waiting_times[int(500):]))
    return times



def write_to_csv(data):
   
    data.to_csv(location, index = False)
    

    
    
if __name__ == '__main__':
    main()