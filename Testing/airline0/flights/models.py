from django.db import models
class Airport(models.Model):
    code = models.CharField(max_length=3)
    city = models.CharField(max_length=64)

    def __str__(self):
        return f"{self.city} ({self.code})"
    
class Flight(models.Model):
    #origin = models.CharField(max_length=64)
    origin = models.ForeignKey(Airport, on_delete=models.CASCADE, related_name="departures")
    destination = models.ForeignKey(Airport, on_delete=models.CASCADE, related_name="arrivals")
    duration = models.IntegerField()

    def __str__(self):
        return f"{self.id}: {self.origin} to {self.destination}"
    
    # Validation method — checks if flight makes sense
    def is_valid_flight(self):
        # 1. origin != destination (can't fly from NYC to NYC)
        # 2. duration >= 0 (can't have negative time)
        return self.origin != self.destination or self.duration >= 0
    
class Passenger(models.Model):
    first = models.CharField(max_length=64)    
    last = models.CharField(max_length=64)    
    flights = models.ManyToManyField(Flight, blank=True, related_name="passengers")

    def __str__(self):
        return f"{self.first} {self.last}"


"""
Django Model Concepts Explained:

- class Name(models.Model): → creates a database table
- field = models.CharField(...) → creates a column for text
- ForeignKey → links to one object in another table (one-to-many)
- ManyToManyField → links many-to-many (both sides can have many)
- related_name="..." → name to use when going backwards (airport.departures.all())
- blank=True → field can be empty in forms
- on_delete=models.CASCADE → if linked object deleted → delete this too
- def __str__(self): → how to show this object as text (used in admin, etc.)
"""