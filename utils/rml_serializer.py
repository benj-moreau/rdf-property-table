from rdflib import Graph, Namespace, Literal, URIRef, BNode

from utils.sparql_queries import get_id_variable, get_uri_suffix, get_variables

rr = Namespace("http://www.w3.org/ns/r2rml#")
rml = Namespace("http://semweb.mmlab.be/ns/rml#")
ql = Namespace('http://semweb.mmlab.be/ns/ql#')


def get_rml_graph(properties, typ, subject_prefix):
    rdf_mapping = Graph()
    rdf_mapping.bind("ql", ql)
    rdf_mapping.bind("rr", rr)
    rdf_mapping.bind("rml", rml)
    add_class_map(rdf_mapping, typ, subject_prefix)
    variables = get_variables(properties)
    for variable, prop in zip(variables, properties):
        field = variable.replace('?', '')
        add_predicate_map(rdf_mapping, prop, field, typ)
    rdf_mapping.serialize(format='ttl', destination='results/{}.rml.ttl'.format(get_uri_suffix(typ)))


def add_class_map(rdf_mapping, typ, subject_prefix):
    subject_id = URIRef("#{}".format(get_uri_suffix(typ)))
    subject_template = "{}{{{}}}".format(subject_prefix, get_id_variable(typ).replace('?', ''))
    logical_source = rml['logicalSource']
    logical_source_node = BNode()
    rdf_mapping.add((subject_id, logical_source, logical_source_node))
    rdf_mapping.add((logical_source_node, rml['source'], Literal(get_uri_suffix(typ))))
    rdf_mapping.add((logical_source_node, rml['referenceFormulation'], ql['JSONPath']))
    rdf_mapping.add((logical_source_node, rml['iterator'], Literal("$.[*].fields")))
    # Adding resource subject and type
    subject_map_node = BNode()
    subject_map = rr['subjectMap']
    rdf_mapping.add((subject_id, subject_map, subject_map_node))
    rdf_mapping.add((subject_map_node, rr['template'], Literal(subject_template)))
    rdf_mapping.add((subject_map_node, rr['class'], URIRef(typ)))


def add_predicate_map(rdf_mapping, prop, field, typ):
    subject_id = URIRef("#{}".format(get_uri_suffix(typ)))
    predicate_map = rr['predicateObjectMap']
    node = BNode()
    rdf_mapping.add((subject_id, predicate_map, node))
    rdf_mapping.add((node, rr['predicate'], URIRef(prop)))
    object_node = BNode()
    rdf_mapping.add((node, rr['objectMap'], object_node))
    # Target of the predicate is a field value (Term)
    rdf_mapping.add((object_node, rml['reference'], Literal("$.{}".format(field))))
    # rdf_mapping.add((object_node, rr['datatype'], xsd:field_type))
