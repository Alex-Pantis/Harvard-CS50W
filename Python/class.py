class point():
    def __init__(self, input1, input2):
        self.x = input1
        self.y = input2
p  = point(2,3)
print(p.x)
print(p.y)
class Flight():
    def __init__(self, capacity ):
        self.capacity = capacity
        self.passengers = []
    def add_pasengers(self, nume):
        #if self.open_seats == 0:
        if not self.open_seats:
            return False
        self.passengers.append(nume)
        return True
    def open_seats(self):
        return self.capacity - len(self.passengers)    

flight = Flight(3)
people = ["Harry", "Mike", "Bob", "jhon"]
for person in people:
    #success = flight.add_pasengers(person)
    #if success:
    if flight.add_pasengers(person):
        print(f"Added {person} in the list")
    else:
        print(f"No available seats for {person}")    