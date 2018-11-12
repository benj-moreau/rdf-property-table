import argparse

from utils.sparql_queries import exec_predicates_query, exec_types_query, exec_subject_query, exec_property_table
from utils.sparql_queries import load_dataset, clean_dataset, get_uri_prefix
from utils.rml_serializer import get_rml_graph


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


def get_property_table(properties, dataset, typ, subject_prefix):
    exec_property_table(properties, dataset, typ, subject_prefix)


def get_subject_prefix(dataset, typ):
    results = exec_subject_query(dataset, typ)
    while results.hasNext():
        next_result = results.next()
        return get_uri_prefix(next_result.get('?s').toString())
    return None


def main():
    parser = argparse.ArgumentParser(prog='property-table', description='Transform a rdf graph into a property table')
    parser.add_argument('filepath', metavar='FP', type=str, nargs='+',
                        help='RDF file to transform')
    args = parser.parse_args()
    filepath = args.filepath[0]
    clean_dataset()
    dataset = load_dataset(filepath)
    types = get_types(dataset)
    for typ in types:
        subject_prefix = get_subject_prefix(dataset, typ)
        properties = get_predicates(dataset, typ)
        get_property_table(properties, dataset, typ, subject_prefix)
        get_rml_graph(properties, typ, subject_prefix)
    clean_dataset()


if __name__ == "__main__":
    main()
