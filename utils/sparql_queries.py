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

PREDICATES_QUERY = """SELECT DISTINCT ?p
WHERE
{{
      ?s <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <{}> .
      ?s ?p ?o
}}
"""

TYPES_QUERY = """
SELECT DISTINCT ?type
WHERE
{
      ?s <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> ?type
}
"""

SPARQL_QUERY = 'SELECT {} WHERE {{ {} }}'


def _property_table_query(properties, typ):
    subject = '?subject'
    variables = _get_variables(properties)
    triple_patterns = ['?subject <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <{}> .'.format(typ)]
    query_variables = '?subject {}'
    for prop_variable, prop in zip(variables, properties):
        triple_pattern = 'OPTIONAL {{ {} <{}> {} }}'.format(subject, prop, prop_variable)
        triple_patterns.append(triple_pattern)
        query_variables = query_variables.format('{} {}'.format(prop_variable, '{}'))
    triple_patterns = '\n'.join(triple_patterns)
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
        prop_label = prop.split(sep)[-1].replace('-', '_')
        variable = variable_pattern.format(prop_label)
        variables.append(variable)
    return variables


def _get_type_suffix(typ):
    if '#' in typ:
        return typ.split('#')[-1]
    else:
        return typ.split('/')[-1]


def _exec_query(query, dataset):
    qexec = autoclass('org.apache.jena.query.QueryExecutionFactory').create(query, dataset)
    results = qexec.execSelect()
    # qexec.close()
    return results


@fn_timer
def exec_types_query(dataset):
    results = _exec_query(TYPES_QUERY, dataset)
    formatter = autoclass('org.apache.jena.query.ResultSetFormatter')
    return formatter.toList(results).listIterator()


@fn_timer
def exec_predicates_query(dataset, typ):
    results = _exec_query(PREDICATES_QUERY.format(typ), dataset)
    formatter = autoclass('org.apache.jena.query.ResultSetFormatter')
    return formatter.toList(results).listIterator()


@fn_timer
def exec_property_table(properties, dataset, typ):
    results = _exec_query(_property_table_query(properties, typ), dataset)
    formatter = autoclass('org.apache.jena.query.ResultSetFormatter')
    File = autoclass('java.io.File')
    FileOutputStream = autoclass('java.io.FileOutputStream')
    f = File('results/{}.csv'.format(_get_type_suffix(typ)))
    fop = FileOutputStream(f)
    if not f.exists():
        f.createNewFile()
    formatter.outputAsCSV(fop, results)
    fop.flush()
    fop.close()


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
