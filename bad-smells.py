import rdflib
import rdflib.plugins.sparql as sq

g = rdflib.Graph()
result = g.load("tree2.owl")

query1 = """SELECT ?mn ?cn (COUNT(*) AS ?tot) WHERE {
            ?c a tree:ClassDeclaration .
            ?c tree:jname ?cn .
            ?c tree:body ?m .
            ?m a tree:MethodDeclaration .
            ?m tree:jname ?mn .
        } GROUP BY ?m"""

query1 = """SELECT ?c WHERE {
      ?c a tree:ClassDeclaration .
      }
"""
q = sq.prepareQuery(
    query1,
    initNs={"tree": "http://usi.ch/giacomelli/Knowledge_Analysis_and_Management.owl#"})
print("All methods: ")

for row in g.query(q):
    print(row.c)
print()
