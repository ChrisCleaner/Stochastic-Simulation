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


import pandas as pd
import xlsxwriter


N = 2
mu = 10
lambd = 8

n_clients = 200
sorting_method = "FIFO"
in_distribution = "Assigned"
serv_distribution = "Assigned"
       

def main():
    
    for lambd in [9, 9.5, 9.9, 9.99999]:
        for sort_method in ["FIFO", "Priority"]:
            for serv_distribution in ["M", "D0.1", "Assigned", "Else"]:
                        #run with 1 server with lambda = 10
                    new_lambd = lambd
                    location = (os.getcwd().replace("\\","/") + f"/Result Folder/results {lambd, sort_method, serv_distribution}.csv")
                    n_servers = 1
                    print('Run with %i server(s) with lambda = %i' % (n_servers, new_lambd))
                    wait_times1 = multiple_simulations( new_lambd, n_servers, sorting_method)
                    print(wait_times1)
                    new_lambd = lambd*2
                    n_servers = 2
                    print('Run with %i server(s) with lambda = %i' % (n_servers, new_lambd))
                    wait_times2 = multiple_simulations(new_lambd, n_servers, sorting_method)
                    
                    new_lambd = new_lambd*2
                    n_servers = 4
                    print('Run with %i server(s) with lambda = %i' % (n_servers, new_lambd))
                    wait_times3 = multiple_simulations(new_lambd, n_servers, sorting_method)
                    
                    
                    
                    df1 = pd.DataFrame({'times': wait_times1, 'servers': [1 for i in range(len(wait_times1))]})
                    df2 = pd.DataFrame({'times': wait_times2, 'servers': [2 for i in range(len(wait_times2))]})
                    df4 = pd.DataFrame({'times': wait_times3, 'servers': [4 for i in range(len(wait_times3))]})
                    
                    df = df1.append(df2)
                    df = df.append(df4)
                    
             
                    write_to_csv(df,location)
    

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
        processing = Server(env, lambd, mu, n_servers, n_clients, sorting_method, in_distribution, serv_distribution)
        env.run()
        #print('clients helped', processing.start)
        times.append(np.mean(processing.waiting_times[int(500):]))
    return times



def write_to_csv(data,location):
   
    data.to_csv(location, index = False)
    

    
    
if __name__ == '__main__':
    main()