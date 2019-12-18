import rdflib
import rdflib.plugins.sparql as sq


def main():
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

    # TODO fix DataClass query

    q = sq.prepareQuery(
        query1,
        initNs={"tree": "http://usi.ch/giacomelli/Knowledge_Analysis_and_Management.owl#"})
    print("All methods: ")

    for row in g.query(q):
        print(row.c)
    print()


def queries():
    return {
        'LongMethod': """
    PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
    PREFIX owl: <http://www.w3.org/2002/07/owl#>
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
    PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
    PREFIX tree: <http://usi.ch/giacomelli/Knowledge_Analysis_and_Management.owl#>
    SELECT ?cn ?mn (COUNT(*) AS ?tot) WHERE {
                ?c a tree:ClassDeclaration .
                ?c tree:jname ?cn .
                ?c tree:body ?m .
                ?m a tree:MethodDeclaration .
                ?m tree:jname ?mn .
                ?m tree:body ?st .
                ?st a/rdfs:subClassOf* tree:Statement .
            }
    
    GROUP BY ?cn ?mn
    HAVING (?tot >= 20)
    ORDER BY DESC(?tot)
    """
        , 'LongConstructor': """
    PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
    PREFIX owl: <http://www.w3.org/2002/07/owl#>
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
    PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
    PREFIX tree: <http://usi.ch/giacomelli/Knowledge_Analysis_and_Management.owl#>
    SELECT ?cn ?mn (COUNT(*) AS ?tot) WHERE {
                ?c a tree:ClassDeclaration .
                ?c tree:jname ?cn .
                ?c tree:body ?m .
                ?m a tree:ConstructorDeclaration .
                ?m tree:jname ?mn .
                ?m tree:body ?st .
                ?st a/rdfs:subClassOf* tree:Statement .
            }
    
    GROUP BY ?cn ?mn
    HAVING (?tot >= 20)
    ORDER BY DESC(?tot)
    """
        , 'LargeClass': """
    PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
    PREFIX owl: <http://www.w3.org/2002/07/owl#>
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
    PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
    PREFIX tree: <http://usi.ch/giacomelli/Knowledge_Analysis_and_Management.owl#>
    SELECT ?cn (COUNT(*) AS ?tot) WHERE {
                ?c a tree:ClassDeclaration .
                ?c tree:jname ?cn .
                ?c tree:body ?m .
                ?m a tree:MethodDeclaration .
            }
    
    GROUP BY ?cn
    HAVING (?tot >= 10)
    ORDER BY DESC(?tot)
    """
        , 'MethodWithSwitch': """
    PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
    PREFIX owl: <http://www.w3.org/2002/07/owl#>
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
    PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
    PREFIX tree: <http://usi.ch/giacomelli/Knowledge_Analysis_and_Management.owl#>
    SELECT ?cn ?mn (COUNT(*) AS ?tot) WHERE {
                ?c a tree:ClassDeclaration .
                ?c tree:jname ?cn .
                ?c tree:body ?m .
                ?m a tree:MethodDeclaration .
                ?m tree:jname ?mn .
                ?m tree:body ?st .
                ?st a tree:SwitchStatement .
            }
    
    GROUP BY ?cn ?mn
    HAVING (?tot >= 1)
    ORDER BY DESC(?tot)
    """
        , 'ConstructorWithSwitch': """
    PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
    PREFIX owl: <http://www.w3.org/2002/07/owl#>
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
    PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
    PREFIX tree: <http://usi.ch/giacomelli/Knowledge_Analysis_and_Management.owl#>
    SELECT ?cn ?mn (COUNT(*) AS ?tot) WHERE {
                ?c a tree:ClassDeclaration .
                ?c tree:jname ?cn .
                ?c tree:body ?m .
                ?m a tree:ConstructorDeclaration .
                ?m tree:jname ?mn .
                ?m tree:body ?st .
                ?st a tree:SwitchStatement .
            }
    
    GROUP BY ?cn ?mn
    HAVING (?tot >= 1)
    ORDER BY DESC(?tot)
    """
        , 'MethodWithLongParameterList': """
    PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
    PREFIX owl: <http://www.w3.org/2002/07/owl#>
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
    PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
    PREFIX tree: <http://usi.ch/giacomelli/Knowledge_Analysis_and_Management.owl#>
    SELECT ?cn ?mn (COUNT(*) AS ?tot) WHERE {
                ?c a tree:ClassDeclaration .
                ?c tree:jname ?cn .
                ?c tree:body ?m .
                ?m a tree:MethodDeclaration .
                ?m tree:jname ?mn .
                ?m tree:parameters ?pa .
            }
    
    GROUP BY ?cn ?mn
    HAVING (?tot >= 5)
    ORDER BY DESC(?tot)
    """
        , 'ConstructorWithLongParameterList': """
    PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
    PREFIX owl: <http://www.w3.org/2002/07/owl#>
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
    PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
    PREFIX tree: <http://usi.ch/giacomelli/Knowledge_Analysis_and_Management.owl#>
    SELECT ?cn ?mn (COUNT(*) AS ?tot) WHERE {
                ?c a tree:ClassDeclaration .
                ?c tree:jname ?cn .
                ?c tree:body ?m .
                ?m a tree:ConstructorDeclaration .
                ?m tree:jname ?mn .
                ?m tree:parameters ?pa .
            }
    
    GROUP BY ?cn ?mn
    HAVING (?tot >= 5)
    ORDER BY DESC(?tot)
    """
        , 'DataClass': """
    """
    }


if __name__ == '__main__':
    main()
