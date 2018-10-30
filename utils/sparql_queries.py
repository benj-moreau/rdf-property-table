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


def spo_query():
    return SPO_QUERY


def predicates_query():
    return PREDICATES_QUERY


def property_table_query(properties):
    subject = '?subject'
    variables = _get_variables(properties)
    triple_patterns = '{}'
    query_variables = '?subject {}'
    for prop_variable, prop in zip(variables, properties):
        triple_pattern = '{} {} {}\n'.format(subject, prop, prop_variable)
        triple_patterns = triple_patterns.format('{} {}'.format(triple_pattern, '{}'))
        query_variables = query_variables.format('{} {}'.format(prop_variable, '{}'))
    triple_patterns = triple_patterns.replace('{}', '')
    query_variables = query_variables.replace('{}', '')
    print SPARQL_QUERY.format(query_variables, triple_patterns)
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
