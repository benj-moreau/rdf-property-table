import argparse

from utils.sparql_queries import exec_predicates_query, exec_property_table, load_dataset, clean_dataset


def get_predicates(dataset):
    results = exec_predicates_query(dataset)
    predicates = []
    while results.hasNext():
        next_result = results.next()
        predicate = next_result.get('?p').toString()
        predicates.append(predicate)
    return predicates


def get_property_table(properties, dataset):
    exec_property_table(properties, dataset)


def main():
    parser = argparse.ArgumentParser(prog='property-table', description='Transform a rdf graph into a property table')
    parser.add_argument('filepath', metavar='FP', type=str, nargs='+',
                        help='RDF file to transform')
    args = parser.parse_args()
    filepath = args.filepath[0]
    dataset = load_dataset(filepath)
    properties = get_predicates(dataset)
    get_property_table(properties, dataset)
    clean_dataset()


if __name__ == "__main__":
    main()
