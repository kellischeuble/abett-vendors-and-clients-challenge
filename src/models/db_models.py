class Vendor:

    def __init__(self, name, direction, schedule):
        self.name = name
        self.direction = direction
        self.schedule = schedule

class Customer:

    def __init__(self, name, employee_count):
        self.name = name
        self.employee_count = employee_count