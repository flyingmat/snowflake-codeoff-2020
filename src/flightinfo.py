import json
from shapely.geometry import Point
from shapely.geometry.linestring import LineString
from shapely.geometry.polygon import Polygon

# Flight class representing a flight
class Flight:
    def __init__(self, flight_json):
        self.flight_json = flight_json
        self.id = flight_json['id']
        self.properties = flight_json['properties']
        self.line = LineString(flight_json['geometry']['coordinates'])

    # return true if the flight starts inside the specified FIR
    def starts_in_fir(self, fir):
        return fir.polygon.contains(Point(self.line.coords[0]))

    # return true if the flight ends inside the specified FIR
    def ends_in_fir(self, fir):
        return fir.polygon.contains(Point(self.line.coords[-1]))

    # return true if the flight crosses the specified FIR at least once
    def crosses_fir(self, fir):
        return self.line.intersects(fir.polygon)

    # return the amount of times the flight crosses the specified FIR
    def times_crosses_fir(self, fir):
        ntimes = 0
        isinside = False
        for coord in self.line.coords:
            if fir.polygon.contains(Point(coord)):
                if not isinside:
                    ntimes += 1
                    isinside = True
            else:
                isinside = False
        return ntimes

    # return true if the flight is domestic given the roi as fir
    def is_domestic(self, fir):
        return self.starts_in_fir(fir) and self.ends_in_fir(fir)

    # return true if the flight is a fly-through given the roi as fir
    def is_flythrough(self, fir):
        return (not self.starts_in_fir(fir) and not self.ends_in_fir(fir))

# FIR class representing a Flight Information Region
class FIR:
    def __init__(self, fir_json):
        self.fir_json = fir_json
        self.properties = fir_json['properties']
        self.polygon = Polygon(fir_json['geometry']['coordinates'][0])

    # return the charge factor for a flight given the roi as fir
    # the charge factor is 2 for fly-through flights, 1 for flights that either
    # start or end in the fir, 0 for domestic flights or flights that do not cross
    # the fir
    def charge_factor(self, flight):
        cf = 0
        if flight.crosses_fir(self):
            if not flight.is_domestic(self):
                if flight.is_flythrough(self):
                    cf = 2
                else:
                    cf = 1
        return cf

def flight_fir_info(flight, fir):
    cf = fir.charge_factor(flight)
    return "Flight {}: charge {}!\n    {}\n    {}\n    {}\n".format(
            flight.properties['flight_number'],
            "no fee" if not cf else "standard" if cf == 1 else "double",

            "{} {}".format(
                    "crosses" if flight.crosses_fir(fir) else "does not cross",
                    fir.properties['ICAOCODE']
                ),
            "is {}domestic".format("" if flight.is_domestic(fir) else "not "),
            "is {}fly-through".format("" if flight.is_flythrough(fir) else "not ")
        )

def parse(fnfir, fnflights):
    with open(fnfir, 'r') as infir:
        fir = json.load(infir)
    with open(fnflights, 'r') as inflights:
        flights = json.load(inflights)
    return fir, flights

def main():
    fir, flights = parse('single_fir.geojson', 'flights.geojson')
    # for flight in flights['features']:
    #     test_flight(flight)
    # test_flight(Flight(flights['features'][0]))
    roi = FIR(fir)
    for jf in flights['features']:
        flight = Flight(jf)
        # print(flight_fir_info(flight, roi))
        flight_fir_info(flight, roi)

if __name__ == '__main__':
    main()
