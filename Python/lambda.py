people =[
    {"name": "Bob", "house": "Hdis"},
    {"name": "Trex", "house": "Hdis1"},
    {"name": "Alex2", "house": "Hdis2"}
]

#def f(person):
#    return person["name"]

#people.sort(key=f)
people.sort(key = lambda person: person["name"] )
print(people)