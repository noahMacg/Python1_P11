import math


# Class to define GPS objects and calculate distance.
class GeoPoint:
    def __init__(self, lat=0, long=0, description="TBD"):
        self.lat = lat
        self.long = long
        self._description = description

    def SetPoint(self, coordinates):
        self.lat, self.long = coordinates

    def GetPoint(self):
        return (self.lat, self.long)

    def SetDescription(self, description):
        self._description = description

    def GetDescription(self):
        return self._description

    point = property(GetPoint, SetPoint)

    description = property(GetDescription, SetDescription)

    # Haversine formula to calculate the distance in km
    def calc_distance(point1, point2):
        lat1, long1 = map(math.radians, point1)
        lat2, long2 = map(math.radians, point2)
        radius = 6371

        a = math.sin((lat1 - lat2) / 2) ** 2 + (
            math.cos(lat1) * math.cos(lat2) * (math.sin((long1 - long2) / 2) ** 2)
        )
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

        return radius * c

    # Print method
    def __str__(self):
        return f"{self.lat:>8.2f} {self.long:>13.2f} {' '*4} {self.description}"
