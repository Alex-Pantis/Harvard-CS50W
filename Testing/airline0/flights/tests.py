from django.test import TestCase, Client # Client = fake browser, TestCase = test runner
from django.db.models import Max
from .models import Airport, Flight, Passenger

# Create a test class — all tests go inside this
class FlightTestCase(TestCase): # TestCase = Django's robot that runs tests and cleans up after

    # This function runs BEFORE every single test
    # Purpose: Create fake data that all tests can use
    def setUp(self): # This will not efect the database
        #create airports
        a1 = Airport.objects.create(code="AAA", city="City A")
        a2 = Airport.objects.create(code="BBB", city="City B")

        # Create three fake flights:
        # 1. Valid: AAA → BBB, duration 100
        Flight.objects.create(origin=a1, destination=a2, duration=100)
        # 2. Invalid: AAA → AAA (same airport)
        Flight.objects.create(origin=a1, destination=a1, duration=200)
        # 3. Invalid: negative duration
        Flight.objects.create(origin=a1, destination=a2, duration=-100)

    # Test 1: Check how many flights leave from airport AAA
    def test_departures_count(self):
        a = Airport.objects.get(code="AAA")
        self.assertEqual(a.departures.count(), 3) # Should be 3 (all flights leave from AAA)

    # Test 2: Check how many flights arrive at airport AAA    
    def test_arrivals_count(self):
        a = Airport.objects.get(code="AAA")
        self.assertEqual(a.arrivals.count(), 1) # Only one flight arrives at AAA (the invalid same-airport one)

    # Test 3: Check if a valid flight passes validation
    def test_valid_flight(self):
        a1 = Airport.objects.get(code="AAA") 
        a2 = Airport.objects.get(code="BBB")
        f = Flight.objects.get(origin=a1, destination=a2, duration=100)
        self.assertTrue(f.is_valid_flight()) 

    # Test 4: Check if same-airport flight fails validation
    def test_invalid_flight_destination(self):
        a1 = Airport.objects.get(code="AAA")
        f = Flight.objects.get(origin=a1, destination=a1)
        self.assertFalse(f.is_valid_flight())

    # Test 5: Check if negative duration fails validation
    def test_invalid_flight_duration(self):
        a1 = Airport.objects.get(code="AAA")
        a2 = Airport.objects.get(code="BBB")
        f = Flight.objects.get(origin=a1, destination=a2, duration=-100)
        self.assertFalse(f.is_valid_flight())

    # Test 6: Check if the main flights list page loads correctly
    def test_index(self):
        c = Client() #Fake browser
        response = c.get("/flights/")  # Visit the flights list page
        # Check if page loaded successfully
        self.assertEqual(response.status_code, 200)
        # Check if it shows all 3 flights
        self.assertEqual(response.context["flights"].count(), 3)

    # Test 7: Check if a real flight page loads
    def test_valid_flight_page(self):
        a1 = Airport.objects.get(code="AAA")
        # Get the invalid same-airport flight (it has an ID)
        f = Flight.objects.get(origin=a1, destination=a1)
        c = Client()
        response = c.get(f"/flights/{f.id}") # Visit its page
        self.assertEqual(response.status_code, 200) # Should load even if invalid

    # Test 8: Check if a fake flight ID gives 404 error
    def test_invalid_flight_page(self):
        # Get the highest flight ID in database
        max_id = Flight.objects.all().aggregate(Max("id"))["id__max"]
        c = Client()
        # Try to visit a flight that doesn't exist (max_id + 1)\
        response = c.get(f"/flights/{max_id + 1}")
        self.assertEqual(response.status_code, 404)  # Should be "Not Found"   


    # Test 9: Check if passenger shows on flight page
    def test_flight_page_passengers(self):
        f =  Flight.objects.get(pk=1)   # Get first flight (pk = primary key = id)
        p = Passenger.objects.create(first="Alice", last="Adams") # Create fake passenger
        f.passengers.add(p)  # Book them on the flight
        c = Client()
        response = c.get(f"/flights/{f.id}")
        self.assertEqual(response.status_code, 200)
        # Check if the passenger appears in context
        self.assertEqual(response.context["passengers"].count(), 1)

    # Test 10: Check if non-booked passenger shows in "available" list
    def test_flight_page_non_passengers(self):
        f = Flight.objects.get(pk=1)
        p = Passenger.objects.create(first="Alice", last="Adams")  # Not booked on flight
        c = Client()
        response = c.get(f"/flights/{f.id}")
        self.assertEqual(response.status_code, 200)
        # non_passengers = all passengers NOT on this flight
        self.assertEqual(response.context["non_passengers"].count(), 1)    
