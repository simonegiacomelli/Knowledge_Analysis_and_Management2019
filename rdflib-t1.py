import rdflib

g = rdflib.Graph()
result = g.load("tree2.owl")

print("graph has %s statements." % len(g))
# prints graph has 79 statements.

for subj, pred, obj in g:
    if (subj, pred, obj) not in g:
        raise Exception("It better be!")

s = g.serialize(format='n3')
