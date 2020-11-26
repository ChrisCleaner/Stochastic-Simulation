# -*- coding: utf-8 -*-
"""
Created on Mon Nov 23 22:13:30 2020

@author: Gebruiker
"""
import simpy
import random
from numpy.random import choice
import numpy as np


class Server(object):
    def __init__(self, env, lamb, mu, n_servers, n_clients, sorting = "FIFO", distribution_input = "M", distribution_time_in_server = "M"):
        self.env = env
        # Start the run process everytime an instance is created.
        #Capacity is the amount of servers n, standard Queue is FIFO
        self.mu = mu
        self.lamb = lamb
        self.n_servers = n_servers
        self.n_clients = n_clients
        self.distribution_input = distribution_input
        self.distribution_time_in_server = distribution_time_in_server
        self.sorting = sorting
        if sorting == "FIFO":
            self.server = simpy.Resource(env, capacity=n_servers)
        else: self.server = simpy.PriorityResource(env, capacity=n_servers)
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
            
            #decide which distribution is chosen and set time in server
            if self.distribution_time_in_server == "M":
                time_in_server = random.expovariate(self.mu)
            elif self.distribution_time_in_server[0] == "D":
                time_in_server = float(self.distribution_time_in_server[1:])
            elif self.distribution_time_in_server == "Assigned": #75% exponential 1, 25% exponential 5
                if random.random() < 0.75:
                    time_in_server = random.expovariate(10)
                else:
                    time_in_server = random.expovariate(2)
            else:
                time_in_server = random.lognormvariate(0,1)
                    
                    
#                
            c = self.client(env, 'Client%02d' % self.start, server, time_in_server)
            env.process(c)
            
            #the time at which a client arrives is exponentially distributed with Lambda
            if self.distribution_input == "M":
                t = random.expovariate(self.lamb)
            elif self.distribution_input[0] == "D": 
                t = float(self.distribution_input[1:])
            elif self.distribution_input == "Assigned":
                if random.random() < 0.75:
                    t = random.expovariate(1)
                else:
                    t = random.expovariate(1/5)
                
            else:
                t = random.lognormvariate(0,1)
                
                
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
        
        if self.sorting == "FIFO":
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
        else:
            with server.request(priority = time_in_server) as req:
                yield req
                
                wait = env.now - arrive
                self.waiting_times.append(wait)
                
                #print("%s Waited %d" % (name, wait))
                
                #calculating the time the client spent in the server, is exponentially distributed with rate mu 
                self.server_times.append(time_in_server)
                yield env.timeout(time_in_server)
                #print("%s Finished %d" % (name, env.now))
            
            
    
        