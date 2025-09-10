import math

def haversine(lat1, lon1, lat2, lon2):
    """
    Calculate the great circle distance between two points
    on the earth (specified in decimal degrees) using the Haversine formula.
    """
    # Convert decimal degrees to radians
    lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])

    # Haversine formula
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = math.sin(dlat / 2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    r = 6371  # Radius of Earth in kilometers. Use 3956 for miles. Determines return value units.

    return c * r

# Example usage
if __name__ == "__main__":
    # Coordinates for New York City
    new_york = (40.7128, -74.0060)

    # Coordinates for London
    london = (51.5074, -0.1278)

    # Calculate the distance
    distance = haversine(new_york[0], new_york[1], london[0], london[1])

    print(f"The distance between New York and London is approximately {distance:.2f} kilometers.")
