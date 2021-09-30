import time

class Timer:
    def start_timer(self, minutes):
        for i in range(minutes):
            time.sleep(1)
            print(i)

        return True

    def __init__(self, work_minutes, break_minutes):
        self.work_minutes = work_minutes
        self.break_minutes = break_minutes

    def __init__(self):
        self.work_minutes = 25
        self.break_minutes = 5
        