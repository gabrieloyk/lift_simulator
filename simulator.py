from lift import Lift, Actions
from person import Person
from info import Info 
import argparse
import random

class Simulator:
    def __init__(self, nfloors):
        self.nfloors = nfloors
        self.up_pressed = set()
        self.down_pressed = set()
        self.lifts = [Lift(nfloors, 10, 0), Lift(nfloors, 10, 1)]
        self.waiting = [[] for f in range(nfloors+1)]
        self.lift_people = [[[] for f in range(nfloors+1)], [[] for f in range(nfloors+1)]]
        self.info = Info()
        self.requests = []
        self.exponential_dist = [1. / (f ** 2 + 1) for f in range(nfloors)]
        self.intervals = [int(random.expovariate(self.exponential_dist[f])) for f in range(self.nfloors)]
    
    def generate(self):
        '''
        Generates new persons that are waiting for the lift. 
        Using a countdown, people are generated at each floor.
        These intervals are sampled from a exponential distribution.
        When the timer runs out, a person will be generated.
        '''
        new_requests = []
        for floor in range(1, self.nfloors):
            if self.intervals[floor] == 0:
                new_person = Person(self.nfloors, floor)
                self.waiting[floor].append(new_person)
                if new_person.get_direction() == "up":
                    self.up_pressed.add(new_person.current_floor)
                elif new_person.get_direction() == "down":
                    self.down_pressed.add(new_person.current_floor)
                new_requests.append(floor)
                self.intervals[floor] = int(random.expovariate(self.exponential_dist[floor])) + 1
            else:
                self.intervals[floor] -= 0.25
        self.requests.extend(new_requests)
    
    def assign_request(self):
        '''
        Assigns which lift should service which particular floor.
        If it is on the way for the lift, it will pick up the person.
        '''
        for lift in self.lifts:
            if lift.is_available():
                if self.up_pressed:
                    lift.add_floors(next(iter(self.up_pressed)))
                    lift.to_do = "up"
                elif self.down_pressed:
                    lift.add_floors(next(iter(self.down_pressed)))
                    lift.to_do = "down"
            else:
                if (lift.current_floor in self.up_pressed):
                    if lift.direction == "down" and lift.to_do == "up":
                        self.up_pressed.remove(lift.current_floor)
                        lift.direction = "up"
                        self.update(lift.action(), lift)
                        print(" * Lift changes direction from down to up")
                        
                    elif lift.direction == "up":
                        self.up_pressed.remove(lift.current_floor)
                        self.update(lift.action(), lift)

                if (lift.current_floor in self.down_pressed):
                    if lift.direction == "up" and lift.to_do == "down":
                        self.down_pressed.remove(lift.current_floor)
                        lift.direction = "down"
                        self.update(lift.action(), lift)
                        print(" * Lift changes direction from up to down")
                        
                    elif lift.direction == "down":
                        self.down_pressed.remove(lift.current_floor)
                        self.update(lift.action(), lift)
  

    def update(self, action, lift):
        '''
        Updates the statistical information gathered.
        Shows opening and closing of lift to allow persons to enter and exit.
        '''
        floor = self.lifts[lift.id].current_floor
        self.info.update_floor(floor, lift.id)
        
        if action == Actions['open']:
            if len(self.lift_people[lift.id][floor]) > 0:
                print(" * Person arrives")
                self.info.completed += 1
                print(self.info.completed)
            for person in self.lift_people[lift.id][floor]:
                self.info.update_wait(person, lift.id)
                self.lift_people[lift.id][floor].remove(person)
            
            current_floor_requests = []
            leavers = []
            for person in self.waiting[floor]:
                if person.get_direction() == lift.direction:
                    print(" * Person enters Lift " + str(lift.id) + " presses floor " + str(person.target_floor))
                    current_floor_requests.append(person.target_floor)
                    self.lift_people[lift.id][person.target_floor].append(person)
                    leavers.append(person)
                    self.lifts[lift.id].add_floors(person.target_floor)
            
            for leaver in leavers:
                self.waiting[floor].remove(leaver)
                
        for floor in range(1, self.nfloors+1):
            for person in self.lift_people[lift.id][floor]:
                person.waiting("in_lift")
            for person in self.waiting[floor]:
                person.waiting("waiting")
            
    def run(self, time):
        '''
        The main system that runs the simulation. 
        At each time step, displays information of floors pressed, the current floor of the lift,
        and the overall statistics of the simulation.
        '''
        for i in range(time):
            print(" ------------------------------------- ")
            print("Time: " + str(i))
            self.generate()
            print("Floors Up Pressed: " + str(self.up_pressed))
            print("Floors Down Pressed: " + str(self.down_pressed))
            self.assign_request()
            for lift in self.lifts:
                print("Lift " + str(lift.id) + " Floor " + str(lift.current_floor) + " Status: " + str(lift.direction))
                print("  " + str(lift.next_floors))
                action = lift.action()
                self.update(action, lift)      
        self.info.get_info()
            
                
                
if __name__ == '__main__':
    s = Simulator(20)
    p = argparse.ArgumentParser()
    p.add_argument('--iterations', type=int, default=100, help='Number of iterations for simulation')
    args = p.parse_args()
    s.run(args.iterations)