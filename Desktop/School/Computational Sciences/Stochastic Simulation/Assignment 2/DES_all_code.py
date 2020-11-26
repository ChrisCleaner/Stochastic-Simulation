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



#sys.path.append(r'C:\Users\Gebruiker\OneDrive\Computational_Science\Year1_Semester1_Block2\Stochastic_Simulations\Assignment2')

#from DES_simulation2 import Server

location = os.getcwd().replace("\\","/") + "/results2.csv" #(r'C:\Users\Gebruiker\OneDrive\Computational_Science\Year1_Semester1_Block2\Stochastic_Simulations\Assignment2\DES_results2.csv')

import pandas as pd
import xlsxwriter


N = 1
mu = 10

n_clients = 20


def main():
  
    #run with 1 server with lambda = 10
    lambd = 9.9
    n_servers = 1
    print('Run with %i server(s) with lambda = %i' % (n_servers, lambd))
    wait_times1 = multiple_simulations( lambd, n_servers)
    
    lambd = 19.8
    n_servers = 2
    print('Run with %i server(s) with lambda = %i' % (n_servers, lambd))
    wait_times2 = multiple_simulations(lambd, n_servers)
    
    lambd = 39.6
    n_servers = 4
    print('Run with %i server(s) with lambda = %i' % (n_servers, lambd))
    wait_times3 = multiple_simulations(lambd, n_servers)
    
    
    
    df1 = pd.DataFrame({'times': wait_times1, 'servers': [1 for i in range(len(wait_times1))]})
    df2 = pd.DataFrame({'times': wait_times2, 'servers': [2 for i in range(len(wait_times2))]})
    df4 = pd.DataFrame({'times': wait_times3, 'servers': [4 for i in range(len(wait_times3))]})
    
    df = df1.append(df2)
    df = df.append(df4)
    
    write_to_csv( df)
    

def multiple_simulations(lambd, n_servers):
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
        processing = Server(env, lambd, mu, n_servers, n_clients)
        env.run()
        #print('clients helped', processing.start)
        times.append(np.mean(processing.waiting_times[int(0):]))
        print(processing.server_times)
    return times



def write_to_csv(data):
   
    data.to_csv(location, index = False)
    
    
class Server(object):
    def __init__(self, env, lamb, mu, n_servers, n_clients):
        self.env = env
        # Start the run process everytime an instance is created.
        #Capacity is the amount of servers n, standard Queue is FIFO
        self.mu = mu
        self.lamb = lamb
        self.n_servers = n_servers
        self.n_clients = n_clients
        
        self.server = simpy.Resource(env, capacity=n_servers)
        self.action = env.process(self.arriving(env, lamb, mu, self.server))
        self.waiting_times = []
        self.server_times = []

   
    
    
    def arriving(self, env, lamb, mu, server):
        """
        simulates the event that a client comes to the server with rate lambda, and is being handles with rate mu   
        env = Simpy envorinment
        lamb = lambda rate at which clietns arrive
        Mu = capacity of each server, rate at which clients are handled
        server = instance of Simpy Resource representing the servers 
        """
        self.start = 1
        #print('lambd', lamb)
        for i in range(self.n_clients):
            #mu is 1/(handle duration) = 1/5 , the amount of time it takes a server to handle one load
            time_in_server = random.expovariate(mu)
            c = self.client(env, 'Client%02d' % self.start, server, time_in_server)
            env.process(c)
            
            #the time at which a client arrives is exponentially distributed with Lambda
            t = random.expovariate(lamb)
            yield env.timeout(t)
            self.start += 1 
        
    
    def client(self, env, name, server, time_in_server):
        """
        simulates the event that a client comes to the server and has to wait if it iss full, server.request 
        is a build in function of Simpy that looks if the Server is free and it lets the client wait until 
        the server is free
        name = name of client
        server = server instance
        time_in_server = mu the rate in which the clients are handled
        """
        arrive = env.now
        #print(" %s arrives at %d" % (name, arrive))
    
        with server.request() as req:
            #the client got to the server
            yield req
            
            wait = env.now - arrive
            self.waiting_times.append(wait)
            
            #print("%s Waited %d" % (name, wait))
            
            #calculating the time the client spent in the server, is exponentially distributed with rate mu 
            tis = time_in_server
            self.server_times.append(tis)
            yield env.timeout(tis)
            #print("%s Finished %d" % (name, env.now))
            
            
    

    
    
if __name__ == '__main__':
    main()