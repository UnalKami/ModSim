import numpy as np
import random as rd
import matplotlib.pyplot as plt

np.random.seed(1)

class MM1_Queue:
    def __init__(self, time_end):

        #Specify input parameters.
        self.mean_interarrival = 3.000
        #Parameters for clients delay where clientA represent those clients that don´t buy anything and clientB and clientC are clients that buy something.
        self.clientA_time = 1.500
        self.clientB_time = np.random.uniform(3.100, 3.800)
        self.clientC_time = 7.000

        self.clientB_profit = 2500
        self.clientC_profit = 4500
        
        self.totalA = 0
        self.totalB = 0
        self.totalC = 0
        self.time_end = time_end

        #Initialize state variables
        #For this problem we will consider the tender as a server
        self.server_status = 0 #0 is idle and 1 is busy
        self.num_in_q = 0
        self.time_arrival = [] #List for times of arrival of customers.
        self.time_last_event = 0.0

        #Initialize statistical couters-
        self.total_of_delays = 0
        self.area_num_in_q = 0.0
        self.area_server_status = 0.0

        self.day_profit = 0
        self.total_customers_per_day = 0
        self.new_client = ""

        #Initialize simulation clock
        self.sim_time = 0.0

        #Initialize event list
        self.time_next_event = [0,0,0] #The ecent list has tree entries, with the first not being used.
        self.time_next_event[1] = self.sim_time + self.expon(self.mean_interarrival)
        self.time_next_event[2] = float('inf')


        self.num_events = 2
         
    def timing(self):
        """Timing funtion."""

        #Initialize variables needed to search event list for minimum time.
        self.min_time_next_event = float('inf')
        self.next_event_type = 0

        #Determine the event type of the next event to occur.
        for i in range(1,self.num_events + 1): #Range considers i=1,2,...,num_events.
            if self.time_next_event[i] < self.min_time_next_event:
                self.min_time_next_event = self.time_next_event[i]
                self.next_event_type = i

        #Check to see whether all entries in the event list have infinite values.
        if self.next_event_type == 0:
            #Stop the simulation
            raise Exception("All entries in the event list have infinite values, so stop the simulation.")

        #The event list has an entry with a finite value, so advance the simulation clock
        self.sim_time = self.min_time_next_event

    def arrive(self):
        """Arrive event function"""

        #Schedule next arrival
        self.time_next_event[1] = self.sim_time + self.expon(self.mean_interarrival)

        #Check to see whether the server is busy.
        if self.server_status == 1:
            #Server is busy, so increment the number for customers un queue and store the time of arrival of the arriving customer at the end of the list self.time_arrival
            self.num_in_q += 1
            self.time_arrival.append(self.sim_time)
        else:
            #Server is idle, so arriving customer has a delay of zero. (The following two statements are for program clarity and do not affect the simulation result)
            self.delay = 0.0
            self.total_of_delays += self.delay

            #Increment the number of customers delayed and make server busy.
            self.server_status = 1
            self.total_customers_per_day += 1

            self.probabilistic_client = ["A","A","B","B","B","B","B","C","C","C"]

            self.new_client = rd.choices(self.probabilistic_client)
            #Increment the number of customers delayed and schedule a departure.
            if self.new_client == ["A"]:
                self.time_next_event[2] = self.sim_time + self.expon(self.clientA_time)
                self.totalA += 1
            elif self.new_client == ["B"]:
                self.day_profit += self.clientB_profit
                self.time_next_event[2] = self.sim_time + self.clientB_time
                self.totalB += 1
            elif self.new_client == ["C"]:
                self.day_profit += self.clientC_profit
                self.time_next_event[2] = self.sim_time + self.expon(self.clientC_time)
                self.totalC += 1

    def depart(self):
        """Depart event function"""
        #Check to see whether the queue is empty
        if self.num_in_q == 0:
            #The queue is empty, so make the server idle and eliminate the departure event front consideration.
            self.server_status = 0
            self.time_next_event[2] =float('inf')
        else:
            #The queue is nonempty, so decrement the number in queuq.
            self.num_in_q -= 1

            #Compute the delay of the customer who is beginning service and update the total delay accumulator.
            self.delay = self.sim_time - self.time_arrival[0] #The indez of the first location in a list is 0.
            self.total_of_delays += self.delay

            #Delete the customer who was first in queue.
            del self.time_arrival[0]
            
    def report(self):
        """Report generator function"""

        print("Store profits: {}".format(self.day_profit))
        print("Clients served: {}".format(self.total_customers_per_day))
        print("Average number in queue: {:.3f}".format(self.area_num_in_q/self.sim_time))
        print("Mean service time: {:.3f} minutes".format(self.total_of_delays/self.total_customers_per_day))
        print("Server utilization: {:.3f}".format(self.area_server_status/self.sim_time))
        print("Time simulation ended: {:.3f} minutes".format(self.sim_time))
        print("-"*55)

    def update_time_avg_stats(self):
        """Funtion to compute time-average statistics."""

        #Compute time since last event and update time-of-last-event marker.
        self.time_since_last_event = self.sim_time - self.time_last_event
        self.time_last_event = self.sim_time

        #Update area under number-in-queue variable.
        self.area_num_in_q += self.num_in_q * self.time_since_last_event

        #Update area under the server-busy indicator variable
        self.area_server_status += self.server_status * self.time_since_last_event

    def expon(self, mean):
        """Function to generate exponential random variates"""

        return -mean * np.log(np.random.uniform(0,1))

    def plot(self):
        labels = 'Clientes tipo A','Clientes tipo B', 'Clientes tipo C'
        sizes = [self.totalA,self.totalB,self.totalC]
        colors = ['pink', 'cadetblue','coral']
        plt.figure(figsize=(12, 6)) 
        plt.subplot(1, 2, 1)
        plt.pie(sizes, labels=labels, autopct='%1.1f%%', shadow=True, startangle=140, colors=colors)
        plt.title('Porcentaje tipos de clientes')

        plt.tight_layout()
        plt.show()

    def main(self):
        print("-"*55)
        print("Single-server queueing system with fixed run length")
        print("Mean interarrival time: {:.3f} minutes".format(self.mean_interarrival))
        print("Simulation run length: {} minutes".format(self.time_end))
        print("-"*55)

        #Run the simulation until the specified amount of time has been reached
        while self.time_end >= self.sim_time:

            #Determine the next event type.
            self.timing()

            #Update the time-average statistical counters.
            self.update_time_avg_stats()

            #Invoke the appropriate event function.
            if self.next_event_type == 1:
                self.arrive()
            elif self.next_event_type == 2:
                self.depart()
        
        while self.num_in_q != 0:
            self.depart()

        #Invoke the report generator
        self.report()



m = MM1_Queue(480)

m.main()
m.plot()
