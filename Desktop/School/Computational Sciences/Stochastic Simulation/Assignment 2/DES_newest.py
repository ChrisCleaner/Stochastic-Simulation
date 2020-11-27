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


sys.path.append(r'C:\Users\Gebruiker\OneDrive\Computational_Science\Year1_Semester1_Block2\Stochastic_Simulations\Assignment2')

from DES_simulation2 import Server, Server_FIFO, Server_Distr


import pandas as pd
import xlsxwriter


N = 100
mu = 10

#n_clients = 10000


def main():
    question1and2()
    question3()

    
    
def question1and2():    
    location = (r'C:\Users\Gebruiker\OneDrive\Computational_Science\Year1_Semester1_Block2\Stochastic_Simulations\Assignment2\Results2\DES_results_1.csv')

    #run with 1 server with lambda = 10
    lambd = 9
    dataframes = pd.DataFrame(columns= ['times', 'n_clients','lambda', 'servers'])
    dataframes2 = pd.DataFrame(columns= ['times', 'n_clients', 'lambda', 'servers'])
    
    for lambd in [5, 8, 9, 9.5, 9.9]:
        for n_clients in [100, 1000, 5000, 10000, 25000, 50000, 100000, 200000, 300000]:
            n_servers = 1
            print('Run with %i server(s) with lambda = %i' % (n_servers, lambd))
            wait_times1 = multiple_simulations( lambd, n_servers, n_clients, 1)
        
            wait_times1_2  = multiple_simulations( lambd, n_servers, n_clients, 2)
    
            lambd2 = lambd*2

            n_servers = 2
            print('Run with %i server(s) with lambda = %i' % (n_servers, lambd2))
            wait_times2  = multiple_simulations(lambd, n_servers,n_clients,  1)
    
            lambd3 = lambd*4

            n_servers = 4
            print('Run with %i server(s) with lambda = %i' % (n_servers, lambd3))
            wait_times3  = multiple_simulations(lambd, n_servers, n_clients, 1)
    
    
    
            df1 = pd.DataFrame({'times': wait_times1, 'n_clients': n_clients,  'lambda': [lambd for i in range(len(wait_times1))], 'servers': [1 for i in range(len(wait_times1))]})
            df2 = pd.DataFrame({'times': wait_times2, 'n_clients': n_clients,'lambda': [lambd for i in range(len(wait_times2))], 'servers': [2 for i in range(len(wait_times2))]})
            df4 = pd.DataFrame({'times': wait_times3, 'n_clients': n_clients, 'lambda': [lambd for i in range(len(wait_times3))], 'servers': [4 for i in range(len(wait_times3))]})
    
            df = df1.append(df2)
            df = df.append(df4)
        
            df1_2 = pd.DataFrame({'times': wait_times1_2, 'n_clients': n_clients,  'lambda': [lambd for i in range(len(wait_times1_2))], 'servers': [1 for i in range(len(wait_times1_2))]})
        
            dataframes = dataframes.append(df)
            dataframes2 = dataframes2.append(df1_2)
        
    write_to_csv(dataframes, location)    

    location = (r'C:\Users\Gebruiker\OneDrive\Computational_Science\Year1_Semester1_Block2\Stochastic_Simulations\Assignment2\Results2\DES_results_2.csv')
    write_to_csv(dataframes2, location)

def question3():
    location = (r'C:\Users\Gebruiker\OneDrive\Computational_Science\Year1_Semester1_Block2\Stochastic_Simulations\Assignment2\Results2\DES_results_3.csv')
    dataframes = pd.DataFrame(columns= ['times', 'n_clients', 'distr', 'servers'])
    for lambd in [5, 8, 9, 9.5, 9.9]:
        for n_clients in [100, 1000, 5000, 10000, 25000, 50000, 100000, 200000, 300000]:
            for serv in [3, 4]:
                n_servers = 1
                print('Run with %i server(s) with lambda = %i' % (n_servers, lambd))
                wait_times1= multiple_simulations( lambd, n_servers, n_clients, serv)
        
     
                lambd2 = lambd*2
            
                n_servers = 2
                print('Run with %i server(s) with lambda = %i' % (n_servers, lambd2))
                wait_times2 = multiple_simulations(lambd, n_servers,n_clients,  serv)
    
                lambd3 = lambd*4

                n_servers = 4
                print('Run with %i server(s) with lambda = %i' % (n_servers, lambd3))
                wait_times3  = multiple_simulations(lambd, n_servers, n_clients, serv)
    
    
                df1 = pd.DataFrame({'times': wait_times1, 'n_clients': n_clients,  'distr': [serv for i in range(len(wait_times1))], 'servers': [1 for i in range(len(wait_times1))]})
                df2 = pd.DataFrame({'times': wait_times2, 'n_clients': n_clients,'distr': [serv for i in range(len(wait_times2))], 'servers': [2 for i in range(len(wait_times2))]})
                df4 = pd.DataFrame({'times': wait_times3, 'n_clients': n_clients, 'distr': [serv for i in range(len(wait_times3))], 'servers': [4 for i in range(len(wait_times3))]})
    
                df = df1.append(df2)
                df = df.append(df4)
        
    
                dataframes = dataframes.append(df)
    
   
    write_to_csv(dataframes, location)    


    

def multiple_simulations(lambd, n_servers, n_clients, serv):
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
        if serv == 1: 
            processing = Server(env, lambd, mu, n_servers, n_clients)
        elif serv == 2:
            processing = Server_FIFO(env, lambd, mu, n_servers, n_clients)
        elif serv == 3:
            processing = Server_Distr(env, lambd, mu, n_servers, n_clients, 'D')
        else:
            processing = Server_Distr(env, lambd, mu, n_servers, n_clients, 'HE')
           
        env.run()
        #print('clients helped', processing.start)
        
        times.append(np.mean(processing.waiting_times))
       
        if i/N*100 % 1 == 0:
            print(int(i/N*100 + 1), '%')
         
    return times



def write_to_csv(data, location):
   
    data.to_csv(location, index = False)
    

    
    
if __name__ == '__main__':
    main()