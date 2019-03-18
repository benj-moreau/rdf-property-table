import argparse
import codecs
import csv

from utils.sparql_queries import exec_predicates_query, exec_types_query, exec_subject_query, exec_property_table
from utils.sparql_queries import load_dataset, clean_dataset, get_uri_prefix
from utils.yarrrml_serializer import get_rml
from utils.sparql_queries import get_uri_suffix, get_id_variable, get_variables
from utils.TimerDecorator import fn_timer

CSV_DELIMITER = '|'
REPLACE_DELIMITER = ' '


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

@fn_timer
def get_property_table(properties, dataset, typ, subject_prefix, filename):
    results = exec_property_table(properties, dataset, typ, subject_prefix, filename)
    filename = 'results/{}_{}.csv'.format(filename, get_uri_suffix(typ))
    templates = {}
    id_variable = get_id_variable(typ)
    header = [id_variable.replace('?', '')]
    variables = get_variables(properties)
    properties = []
    for var in variables:
        prop = var.replace('?', '')
        properties.append(prop)
        header.append(prop)
    with codecs.open(filename, "w") as fp:
        writer = csv.writer(fp, delimiter=CSV_DELIMITER)
        writer.writerow(header)
        while results.hasNext():
            next_result = results.next()
            row = [next_result.get(id_variable).toString().replace(CSV_DELIMITER, REPLACE_DELIMITER)]
            for field, var in zip(properties, variables):
                value = next_result.get(var)
                if value:
                    value = value.toString()
                    if is_uri(value):
                        if not templates.get(field):
                            templates[field] = get_uri_prefix(value)
                        value = get_uri_suffix(value)
                    value = value.replace(CSV_DELIMITER, REPLACE_DELIMITER)
                row.append(value)
            writer.writerow(row)
    return templates


def get_subject_prefix(dataset, typ):
    results = exec_subject_query(dataset, typ)
    while results.hasNext():
        next_result = results.next()
        return get_uri_prefix(next_result.get('?s').toString())
    return None


def get_filename(filepath):
    # remove path
    filename = filepath.rsplit('/', 1)[-1]
    # remove extension
    filename = filename.rsplit('.', 1)[0]
    return filename


def is_uri(value):
    if 'http' in value and '://' in value:
        return True
    return False


def main():
    parser = argparse.ArgumentParser(prog='property-table', description='Transform a rdf graph into a property table')
    parser.add_argument('filepath', nargs='+', help='RDF file to transform', type=str)
    args = parser.parse_args()
    clean_dataset()
    for filepath in args.filepath:
        filename = get_filename(filepath)
        dataset = load_dataset(filepath)
        types = get_types(dataset)
        for typ in types:
            subject_prefix = get_subject_prefix(dataset, typ)
            properties = get_predicates(dataset, typ)
            templates = get_property_table(properties, dataset, typ, subject_prefix, filename)
            get_rml(properties, typ, subject_prefix, filename, templates)
        clean_dataset()


if __name__ == "__main__":
    main()
