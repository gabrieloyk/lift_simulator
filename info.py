class Info:
    def __init__(self):
        self.completed = 0
        self.waiting_times = []
        self.logs = {0: {"transport_logs": [], "floor_logs": []}, 
                1: {"transport_logs": [], "floor_logs": []}}

    def update_wait(self, person, lift_id):
        self.waiting_times.append(person.waiting_time)
        self.logs[lift_id]['transport_logs'].append(person.transport_time)

    def update_floor(self, current_floor, lift_id):
        self.logs[lift_id]['floor_logs'].append(current_floor)

    def get_info(self):
        '''
        Return aggregated statistics on the simulation.
        '''
        waiting_time = sum(self.waiting_times)
        print(" ------------------------------------- ")
        print("Total floor waiting time  " + str(round(waiting_time/ len(self.waiting_times),2)))
        transport_time = sum(self.logs[0]["transport_logs"]) + sum(self.logs[1]["transport_logs"])
        print("Total transport time " + str(round(transport_time/ len(self.waiting_times),2)))
        total_time = waiting_time + transport_time
        print("Average total time taken: "+ str(round(total_time/len(self.waiting_times),2)))
        print("Number of completed trips: " + str(self.completed))
