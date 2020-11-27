import simpy
import random
from numpy.random import choice
import numpy as np

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
            c = self.client(env, 'Client%02d' % self.start, server, time_in_server=mu)
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
            tis = random.expovariate(time_in_server)
            self.server_times.append(tis)
            yield env.timeout(tis)
            #print("%s Finished %d" % (name, env.now))
            
            
class Server_FIFO(object):
    def __init__(self, env, lamb, mu, n_servers, n_clients):
        self.env = env
        # Start the run process everytime an instance is created.
        #Capacity is the amount of servers n, standard Queue is FIFO
        self.mu = mu
        self.lamb = lamb
        self.n_servers = n_servers
        self.n_clients = n_clients
        
        self.server = simpy.PriorityResource(env, capacity=n_servers)
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
            c = self.client(env, 'Client%02d' % self.start, server, time_in_server=mu)
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
        tis = random.expovariate(time_in_server)
        
        
        with server.request(priority = tis) as req:
            #the client got to the server
            yield req
            
            wait = env.now - arrive
            self.waiting_times.append(wait)
            
            #print("%s Waited %d" % (name, wait))
            
            #calculating the time the client spent in the server, is exponentially distributed with rate mu 

            self.server_times.append(tis)
            yield env.timeout(tis)
            #print("%s Finished %d" % (name, env.now))
            

class Server_Distr(object):
    def __init__(self, env, lamb, mu, n_servers, n_clients, distr):
        self.env = env
        # Start the run process everytime an instance is created.
        #Capacity is the amount of servers n, standard Queue is FIFO
        self.mu = mu
        self.lamb = lamb
        self.n_servers = n_servers
        self.n_clients = n_clients
        self.distr = distr
        
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
            c = self.client(env, 'Client%02d' % self.start, server, time_in_server=mu)
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
            
            
            if self.distr == 'M':
                tis = random.expovariate(time_in_server)
            elif self.distr == "D":
                tis = float(1/time_in_server)
            elif self.distr == "HE": #75% exponential 1, 25% exponential 5
            
                if random.random() <= 0.75:
                    tis = random.expovariate(20)
                else:
                    tis = random.expovariate(4)
            else:
             
                tis = random.lognormvariate(0,1)
                
            self.server_times.append(tis)
            yield env.timeout(tis)
            #print("%s Finished %d" % (name, env.now))
                        
    
        