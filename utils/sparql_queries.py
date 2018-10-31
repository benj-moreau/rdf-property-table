from jnius import autoclass
import shutil

from utils.TimerDecorator import fn_timer

STORE_PATH = 'rdf_store/tdb_dataset'

SPO_QUERY = """
SELECT ?s ?p ?o
WHERE
{
      ?s ?p ?o
}
"""

PREDICATES_QUERY = """
SELECT DISTINCT ?p
WHERE
{
      ?s ?p ?o
}
"""

SPARQL_QUERY = 'SELECT {} WHERE {{ {} }}'


def _property_table_query(properties):
    subject = '?subject'
    variables = _get_variables(properties)
    triple_patterns = '{}'
    query_variables = '?subject {}'
    for prop_variable, prop in zip(variables, properties):
        triple_pattern = '{} <{}> {} .\n'.format(subject, prop, prop_variable)
        triple_patterns = triple_patterns.format('{} {}'.format(triple_pattern, '{}'))
        query_variables = query_variables.format('{} {}'.format(prop_variable, '{}'))
    triple_patterns = triple_patterns.replace('{}', '')
    query_variables = query_variables.replace('{}', '')
    return SPARQL_QUERY.format(query_variables, '{}'.format(triple_patterns))


def _get_variables(properties):
    variables = []
    variable_pattern = '?{}'
    for prop in properties:
        if '#' in prop:
            sep = '#'
        else:
            sep = '/'
        prop_label = prop.split(sep)[-1]
        variable = variable_pattern.format(prop_label)
        variables.append(variable)
    return variables


def _exec_query(query, dataset):
    qexec = autoclass('org.apache.jena.query.QueryExecutionFactory').create(query, dataset)
    results = qexec.execSelect()
    # qexec.close()
    return results


@fn_timer
def exec_predicates_query(dataset):
    results = _exec_query(PREDICATES_QUERY, dataset)
    formatter = autoclass('org.apache.jena.query.ResultSetFormatter')
    return formatter.toList(results).listIterator()


@fn_timer
def exec_property_table(properties, dataset):
    results = _exec_query(_property_table_query(properties), dataset)
    formatter = autoclass('org.apache.jena.query.ResultSetFormatter')
    formatter.outputAsCSV(results)


@fn_timer
def load_dataset(filepath):
    dataset = autoclass('org.apache.jena.tdb.TDBFactory').createDataset(STORE_PATH)
    model = dataset.getDefaultModel()
    autoclass('org.apache.jena.tdb.TDBLoader').loadModel(model, filepath)
    return dataset


@fn_timer
def clean_dataset():
    try:
        shutil.rmtree(STORE_PATH)
    except OSError as e:
        print ("Error: %s - %s." % (e.filename, e.strerror))
