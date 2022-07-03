from collections import deque
Actions = {'up':1, 'down': -1, 'open': 0}
class Lift: 
    def __init__(self, nfloors, floor, lift_id):
        self.id = lift_id
        self.next_floors = deque()
        self.pressed = set()
        self.nfloors = nfloors
        self.initial_floor = floor
        self.current_floor = floor
        self.direction = 'down'
        self.to_do = ''
    
    def is_available(self):
        return len(self.next_floors) == 0
    
    def add_floors(self, floor):
        """
        Adds instructions to where the lift should go next.
        """
        if floor not in self.pressed:
            if len(self.pressed) == 0:
                self.next_floors.append(floor)
                self.pressed.add(floor)
            elif floor > max(self.pressed):
                self.next_floors.append(floor)
                self.pressed.add(floor)
            elif floor < min(self.pressed):
                self.next_floors.appendleft(floor)
                self.pressed.add(floor)
            

    def action(self):
        """
        Performs necessary action. Open doors if there are people who need to get off or on. 
        Else, move to the next floor. When the lift has nothing to do it will return to the middle floor.
        Returns movement of lift.
        """
        move = 0
        if len(self.next_floors) == 0:
            if self.current_floor != self.initial_floor:
                move = Actions['up'] if self.current_floor < (self.nfloors / 2) else Actions['down']
        elif self.current_floor == self.next_floors[0]:
            print("* Lift " + str(self.id) + " Doors Opening... Floor " + str(self.current_floor) )
            self.next_floors.remove(self.current_floor)
            if self.to_do != self.direction:
                self.direction = self.to_do
            if self.pressed and (self.current_floor in self.pressed):
                self.pressed.remove(self.current_floor)
            move = Actions['open']
        else:
            move = Actions['up'] if self.current_floor < self.next_floors[0] else Actions['down']

        self.current_floor += move
        
        if move > 0:
            self.direction = "up"
        if move < 0:
            self.direction = "down"
            
        return move
 