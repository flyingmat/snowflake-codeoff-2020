import argparse
import flightinfo

parser = argparse.ArgumentParser(description='Display info about flights and their relations with FIRs')
parser.add_argument('fnfir', metavar='FIR_JSON', help='FIR list, in geojson format')
parser.add_argument('fnflights', metavar='FLIGHTS_JSON', help='flight list, in geojson format')
parser.add_argument('--csv', dest='csv', action='store_const', const=True, default=False, help='use csv format')
parser.add_argument('-o', dest='output', type=str, default=None, help='store output in a file');

args = parser.parse_args()
flightinfo.run(args.fnfir, args.fnflights, args.csv, args.output)
