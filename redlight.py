import json
import re

jsonPath = "Red_Light_Camera_Violations_2023.json"

with open(jsonPath, "r") as jsonFile:
    data = json.load(jsonFile)

lstIntersections = [feature['properties']['INTERSECTION'] for feature in data['features']]

lstStreetNames = [name.strip().capitalize() for intersection in lstIntersections for name in re.split('@', intersection)]
lstStreetNames = sorted(list(set(lstStreetNames)))

lstToSanitize = [name for name in lstStreetNames if '/' in name]

lst1 = sorted(list(set(lstStreetNames).symmetric_difference(lstToSanitize)))

listOfStreets = []
for name in lstToSanitize:
    streets = [street.strip().capitalize() for street in re.split(r'\s*/\s*', name)]
    listOfStreets.extend(streets)
lst1.extend(listOfStreets)
listOfStreets = sorted(list(set(lst1)))

while True:
    streetName = input("Please enter the name of the street (x to exit)? ").strip().capitalize()

    if streetName == 'X':
        print("Good bye!")
        break

    if streetName in listOfStreets:
        foundStreet = None
        for feature in data['features']:
            intersection = feature['properties']['INTERSECTION']
            if any(streetName.lower() in street.lower() for street in re.split('@|/', intersection)):
                foundStreet = feature
                break

        if foundStreet:
            print(f"\nAll Red Light Violations on {streetName} Street/Road:")
            totalViolations = 0
            for month in ['JANUARY', 'FEBRUARY', 'MARCH', 'APRIL', 'MAY', 'JUNE', 'JULY', 'AUGUST', 'SEPTEMBER', 'OCTOBER', 'NOVEMBER', 'DECEMBER']:
                if foundStreet['properties'][month] != 'TBD':
                    print(f"{month}: {foundStreet['properties'][month]}")
                    totalViolations += int(foundStreet['properties'][month])
                else:
                    print(f"{month}: TBD")

            print(f"\nTotal violations: {totalViolations}\n")
    else:
        print("Street not found\n")
