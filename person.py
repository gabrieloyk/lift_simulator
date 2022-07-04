import random

def sample_floor(nfloors):
    '''
    Assigns a greater chance that the person will want to go to floor 1.
    '''
    levels = range(1, nfloors)
    weights = [0.24]
    for x in range(2, nfloors):
        weights.append(0.04)
    return random.choices(levels, weights)[0]

class Person:
    def __init__(self, nfloors, floor):
        self.status = "waiting"
        self.waiting_time = 0
        self.transport_time = 0
        self.current_floor = floor
        self.target_floor = sample_floor(nfloors)
        while self.target_floor == floor:
            self.target_floor = sample_floor(nfloors)
            
    def waiting(self, status):
        if status == "in_lift":
            self.transport_time +=1
        elif status == "waiting":
            self.waiting_time += 1
    
    def get_direction(self):
        return "up" if self.target_floor > self.current_floor else "down"
        
        
    