import argparse
import flightinfo

parser = argparse.ArgumentParser(description='Display info about flights and their relations with FIRs')
parser.add_argument('fnfir', metavar='FIR_JSON', help='FIR list, in geojson format')
parser.add_argument('fnflights', metavar='FLIGHTS_JSON', help='flight list, in geojson format')

args = parser.parse_args()
flightinfo.print_info(args.fnfir, args.fnflights)
