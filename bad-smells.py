import rdflib
import rdflib.plugins.sparql as sq

g = rdflib.Graph()
g.load("tree2.owl")


def rdfquery(query):
    namespace = "http://usi.ch/giacomelli/Knowledge_Analysis_and_Management.owl#"
    q = sq.prepareQuery(query, initNs={"tree": namespace})
    return g.query(q)


def get(d, name):
    if name in d.labels:
        return d[name]
    return ''


def main():
    with open('log.txt', 'w') as f:
        def log(*args):
            print(*args)
            f.write(' '.join(args) + '\n')

        items = queries().items()
        for idx, (name, query) in enumerate(items):
            if name != 'DataClass':
                continue

            log(name + ':')

            result = rdfquery(query)
            for r in result:
                log(f"  {get(r, 'cn')} :: {get(r, 'mn')} ({get(r, 'tot')})")
            log()


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
    HAVING (COUNT(*) >= 20)
    ORDER BY DESC(COUNT(*))
    """
        , 'LongConstructor': """
    PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
    PREFIX owl: <http://www.w3.org/2002/07/owl#>
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
    PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
    PREFIX tree: <http://usi.ch/giacomelli/Knowledge_Analysis_and_Management.owl#>
    SELECT ?cn ?mn (COUNT(?st) AS ?tot) WHERE {
                ?c a tree:ClassDeclaration .
                ?c tree:jname ?cn .
                ?c tree:body ?m .
                ?m a tree:ConstructorDeclaration .
                ?m tree:jname ?mn .
                ?m tree:body ?st .
                ?st a/rdfs:subClassOf* tree:Statement .
            }
    
    GROUP BY ?cn ?mn
    HAVING (COUNT(?st) >= 20)
    ORDER BY DESC(COUNT(*))
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
    HAVING (COUNT(*)  >= 10)
    ORDER BY DESC(COUNT(*))
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
    HAVING (COUNT(*) >= 1)
    ORDER BY DESC(COUNT(*))
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
    HAVING (COUNT(*) >= 1)
    ORDER BY DESC(COUNT(*))
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
    HAVING (COUNT(*) >= 5)
    ORDER BY DESC(COUNT(*))
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
    HAVING (COUNT(*) >= 5)
    ORDER BY DESC(COUNT(*))
    """
        , 'DataClass': """
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
                ?m tree:jname ?mn .
                FILTER regex(?mn, "^get.*|^set.*")
            }
    
    GROUP BY ?cn
    HAVING (COUNT(*)  > 0)
    ORDER BY DESC(COUNT(*))
        """
    }


if __name__ == '__main__':
    main()
