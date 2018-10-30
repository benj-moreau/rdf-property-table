from jnius import autoclass
import argparse

from utils.sparql_queries import predicates_query, property_table_query


def get_predicates(dataset):
    qexec = autoclass('org.apache.jena.query.QueryExecutionFactory').create(predicates_query(), dataset)
    formatter = autoclass('org.apache.jena.query.ResultSetFormatter')
    results = qexec.execSelect()
    results = formatter.toList(results).listIterator()
    predicates = []
    while results.hasNext():
        next_result = results.next()
        predicate = next_result.get('?p').toString()
        predicates.append(predicate)
    qexec.close()
    return predicates


def get_property_table(dataset, properties):
    print property_table_query(properties)
    qexec = autoclass('org.apache.jena.query.QueryExecutionFactory').create(property_table_query(properties), dataset)
    formatter = autoclass('org.apache.jena.query.ResultSetFormatter')
    results = qexec.execSelect()
    formatter.outputAsCSV(results)


def main():
    parser = argparse.ArgumentParser(prog='property-table', description='Transform a rdf graph into a property table')
    parser.add_argument('filepath', metavar='FP', type=str, nargs='+',
                        help='RDF file to transform')
    args = parser.parse_args()
    filepath = args.filepath[0]
    dataset = autoclass('org.apache.jena.riot.RDFDataMgr').loadDataset(filepath)
    # formater.outputAsCSV(results)
    properties = get_predicates(dataset)
    get_property_table(dataset, properties)


if __name__ == "__main__":
    main()
