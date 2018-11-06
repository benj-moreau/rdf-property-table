import argparse

from utils.sparql_queries import exec_predicates_query, exec_types_query, exec_property_table, load_dataset, clean_dataset


def get_types(dataset):
    results = exec_types_query(dataset)
    types = []
    while results.hasNext():
        next_result = results.next()
        typ = next_result.get('?type').toString()
        types.append(typ)
    return types


def get_predicates(dataset, typ):
    results = exec_predicates_query(dataset, typ)
    predicates = []
    while results.hasNext():
        next_result = results.next()
        predicate = next_result.get('?p').toString()
        if 'http://www.w3.org/1999/02/22-rdf-syntax-ns#type' not in predicate:
            predicates.append(predicate)
    return predicates


def get_property_table(properties, dataset, typ):
    exec_property_table(properties, dataset, typ)


def main():
    parser = argparse.ArgumentParser(prog='property-table', description='Transform a rdf graph into a property table')
    parser.add_argument('filepath', metavar='FP', type=str, nargs='+',
                        help='RDF file to transform')
    args = parser.parse_args()
    filepath = args.filepath[0]
    dataset = load_dataset(filepath)
    types = get_types(dataset)
    for typ in types:
        properties = get_predicates(dataset, typ)
        get_property_table(properties, dataset, typ)
    clean_dataset()


if __name__ == "__main__":
    main()
