import yaml

from utils.sparql_queries import get_id_variable, get_uri_suffix, get_variables

SOURCE = '{dataset_id}.json~jsonpath'
ITERATOR = '$.[*].fields'


def get_rml(properties, typ, subject_prefix, filename, templates):
    rdf_mapping = {}
    rdf_mapping = _add_source(rdf_mapping, dataset_id=get_uri_suffix(typ))
    rdf_mapping['mappings'] = {}
    rdf_mapping = _add_class_map(rdf_mapping, typ, subject_prefix)
    variables = get_variables(properties)
    for variable, prop in zip(variables, properties):
        field = variable.replace('?', '')
        _add_predicate_map(rdf_mapping, prop, field, typ, templates)
    file = open('results/{}_{}.rml.yaml'.format(filename, get_uri_suffix(typ)), 'w')
    yaml.safe_dump(rdf_mapping, file)


def _add_source(rdf_mapping, dataset_id):
    rdf_mapping['sources'] = {'dataset-source': [SOURCE.format(dataset_id=dataset_id), ITERATOR]}
    return rdf_mapping


def _add_class_map(rdf_mapping, typ, subject_prefix):
    subject_id = get_uri_suffix(typ)
    template = "{}$({})".format(subject_prefix, get_id_variable(typ).replace('?', '').lower())
    class_map = {'source': 'dataset-source', 'subject': template, 'predicateobjects': []}
    class_map['predicateobjects'].append(['a', typ])
    rdf_mapping['mappings'][subject_id] = class_map
    return rdf_mapping


def _add_predicate_map(rdf_mapping, prop, field, typ, templates):
    subject_id = get_uri_suffix(typ)
    if templates.get(field):
        rdf_mapping['mappings'][subject_id]['predicateobjects'].append([prop, "{}$({})".format(templates[field], field.lower())])
    else:
        rdf_mapping['mappings'][subject_id]['predicateobjects'].append([prop, '$({})'.format(field.lower())])
    return rdf_mapping
