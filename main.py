import rdflib
from rdflib import URIRef, Literal
from rdflib.namespace import RDF, XSD
from pyshacl import validate

# 1. BUILD THE GRAPH (In a real app, this data comes from an API or JSON payload)
g = rdflib.Graph()
ex = rdflib.Namespace("http://example.com/edu#")

courses = {
    "AIT626_NLP_Theory": {"credits": 3},
    "ECE554_Embedded_ML": {"credits": "Three"} # Error: Text instead of a number
}

for name, details in courses.items():
    uri = URIRef(ex + name)
    g.add((uri, RDF.type, ex.Course))
    
    if isinstance(details["credits"], int):
        g.add((uri, ex.credits, Literal(details["credits"], datatype=XSD.integer)))
    else:
        g.add((uri, ex.credits, Literal(details["credits"], datatype=XSD.string)))

# 2. LOAD THE EXTERNAL SHACL FILE
shapes_graph = rdflib.Graph().parse("rules.shacl", format="turtle")

# 3. PIPELINE GATE 1: VALIDATION
print("--- RUNNING PIPELINE GATE 1: SHACL AUDIT ---")
conforms, _, results_text = validate(g, shacl_graph=shapes_graph, inference='none')

if conforms:
    print("Audit Passed! Opening query file...\n")
    
    # 4. PIPELINE GATE 2: SPARQL EXTRACTION
    print("--- RUNNING PIPELINE GATE 2: SPARQL ---")
    with open("extract.rq", "r") as file:
        sparql_query = file.read()
        
    for row in g.query(sparql_query):
        print(f"Valid Record: {row.courseName} | Credits: {row.credits}")
        
else:
    # 5. HALT PIPELINE
    print("CRITICAL FAILURE: Pipeline Halted. Bad data prevented from reaching the query stage.\n")
    print(results_text)