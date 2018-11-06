# rdf-property-table
Transform a RDF file into property class tables.

See [A survey of RDF storage approaches](https://hal.inria.fr/hal-01299496/document) for more informations on property table.

# Installation

Assuming you already have `python 2.7`, `pip 9`, `java 8`,

Download [jena 3.9](https://jena.apache.org/download/index.cgi) and update classpath:

```bash
export CLASSPATH=${CLASSPATH}:YOUR-JENA-DIR-PATH/lib/*
```

Create a new virtualenv:

install Cython

```bash
python -m pip install --upgrade cython
```

Install dependencies with pip:

```bash
pip install -r requirements.txt
```

# Run it !

```bash
python property_table.py [filepath]
```

example for a turtle file in the current directory:

```bash
python property_table.py rdf_file.ttl
```
