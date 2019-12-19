import rdflib
import rdflib.plugins.sparql as sq

g = rdflib.Graph()
g.load("tree2.owl")


def rdfquery(query):
    namespace = "http://usi.ch/giacomelli/Knowledge_Analysis_and_Management.owl#"
    q = sq.prepareQuery(query, initNs={"tree": namespace})
    return g.query(q)


def get(dictionary, fieldname):
    if fieldname in dictionary.labels:
        return dictionary[fieldname]
    return ''


def query_to_set(query):
    return {r.cn for r in rdfquery(query)}


def main():
    with open('log.txt', 'w') as f:
        def log(*args):
            print(*args)
            f.write(' '.join(args) + '\n')

        # DataClass bad smell is a special case
        log('DataClass:')
        yes_setget, no_setget = data_class_queries()
        for cn in query_to_set(yes_setget) - query_to_set(no_setget):
            log(f"  {cn} :: ()")
        log()

        # the rest of the bad smells
        for name, query in queries().items():
            log(name + ':')
            for r in rdfquery(query):
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

    }


def data_class_queries():
    return ["""
    PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
    PREFIX owl: <http://www.w3.org/2002/07/owl#>
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
    PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
    PREFIX tree: <http://usi.ch/giacomelli/Knowledge_Analysis_and_Management.owl#>
    SELECT distinct ?cn WHERE {
                ?c a tree:ClassDeclaration .
                ?c tree:jname ?cn .
                ?c tree:body ?m .
                ?m a tree:MethodDeclaration .
                ?m tree:jname ?mn .
                FILTER regex(?mn, "^get.*|^set.*")
            }
    """, """
        PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
        PREFIX owl: <http://www.w3.org/2002/07/owl#>
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
        PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
        PREFIX tree: <http://usi.ch/giacomelli/Knowledge_Analysis_and_Management.owl#>
        SELECT distinct ?cn WHERE {
                    ?c a tree:ClassDeclaration .
                    ?c tree:jname ?cn .
                    ?c tree:body ?m .
                    ?m a tree:MethodDeclaration .
                    ?m tree:jname ?mn .
                    FILTER ( !EXISTS {
                        FILTER regex(?mn, "^get.*|^set.*")
                    } )
                }
    """]


if __name__ == '__main__':
    main()
