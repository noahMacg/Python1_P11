# MacGillivray_P11
# # Programmer: Noah MacGillivray
# EMail: nmacgillivray@cnm.edu
# Purpose: Extends from P10 and practices GUI
# This program creates a list of geo points from file read in, asks the user
# for a location and finds the closest location from the data read in.

from GeoPoint import GeoPoint
import textwrap

user_continue = True  # Condition to continue program loop

f = open("coordinates.txt")
# List to hold the imported geo points
geo_points = []
# Import data
for line in f:
    data = line.strip().split(",")
    lat = float(data[0])
    long = float(data[1])
    description = data[2]
    obj = GeoPoint(lat, long, description)
    geo_points.append(obj)
f.close()


# Header function
def header():
    text = (
        "This program finds the distance between a list of predetermined locations"
        " read in from a file and the location you provide. It then calculates which location"
        " you are closer to."
    )
    wrapped_string = textwrap.fill(text, width=80)
    print(wrapped_string)
    print()


# Imported list header
def list_header():
    print(
        "\nThe following are the locations for comparison and their associated coordinates:\n"
    )
    print(f"{'Latitude':<14} {'Longitude':<14} {'Location':<14}")
    print(f"{'-'*38}")


# Asks user for location; converts the input from string to float and stores in a tuple
def get_location():
    while True:
        user_input = input(
            "Enter your latitude and longitude (in decimal degrees) separated by a space: "
        )
        try:
            lat_long = user_input.split()

            if len(lat_long) != 2:
                raise ValueError(
                    "Please enter exactly two values only separated by a space."
                )

            lat_long = tuple(map(float, lat_long))

            return lat_long
        except ValueError:
            print(
                "Invalid input; please enter two separate coordinates separated by a space."
            )


# Asks user for location name.
def get_location_name():

    while True:
        user_input = input("Enter the location name:")

        if user_input:
            return user_input
        print("Nothing was entered; please provide a name.")


# Calculates the closest distance from user input and imported list
def calc_closest_distance(user_input, other_points):

    closest_distance = float("inf")
    closest_point = None

    for i in other_points:
        distance = GeoPoint.calc_distance(user_input.point, i.point)

        if distance < closest_distance:
            closest_distance = distance
            closest_point = i.description

    return (closest_distance, closest_point)


# Program loop that uses other functions to get locations,
# calculate distance, print the results and ask user to continue.
try:
    while user_continue == True:
        header()
        # GPS and locations name variables
        user_lat, user_long = get_location()
        user_location_name = get_location_name()
        user_input = GeoPoint(user_lat, user_long, user_location_name)

        closest_point = calc_closest_distance(user_input, geo_points)
        list_header()
        for point in geo_points:
            print(point)

        print()
        print(
            f"{user_location_name.capitalize()} is closer to{closest_point[1]} with "
            f"a distance of {closest_point[0]:.2f} km\n"
        )

        compute_another = (
            input("Would you like to compute another? Enter yes or no: ")
            .strip()
            .lower()
        )
        if compute_another == "yes":
            continue
        else:
            print()
            print("Thanks for using the program, have a nice day!")
            user_continue = False
except Exception as e:
    print("Something went wrong: ", e)

    compute_another = (
        input("Would you like to compute another? Enter yes or no: ").strip().lower()
    )
    if compute_another == "yes":
        compute_another = True
    else:
        print()
        print("Thanks for using the program, have a nice day!")
        user_continue = False
