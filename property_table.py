from jnius import autoclass, cast
import argparse
import csv


def main():
    parser = argparse.ArgumentParser(prog='property-table', description='Transform a rdf graph into a property table')
    parser.add_argument('filepath', metavar='FP', type=str, nargs='+',
                        help='RDF file to transform')
    args = parser.parse_args()
    filepath = args.filepath[0]
    DBConnection = autoclass('org.apache.jena.query.Query')
    System = autoclass('java.lang.System')
    System.out.println(filepath)


if __name__ == "__main__":
    main()
