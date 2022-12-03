from owlready2 import *
import itertools

onto = get_ontology("drugs.owl")
onto.load()

def checkio(data):
    for index in range(len(data) - 1, -1, -1):
        if data.count(data[index]) == 1:
            del data[index]
    return data

def join(qs):
    if len(qs) == 1:
        return qs[0]

    qs = list(itertools.chain(*qs))
    qs = checkio(qs)
    qs = set(qs)

    return list(qs)

# Пользователь ввобдит противопоказание - ему выдает препарат
def create_q(danger_list):
    qs = []
    for danger in danger_list:
        q = default_world.sparql(""" 
                        Prefix lab: <http://www.semanticweb.org/home/ontologies/2022/10/untitled-ontology-32#>
                        SELECT ?prep_n
                        WHERE { 
                            ?prep rdf:type lab:Препарат .
                            ?prep lab:Name ?prep_n .
                            FILTER NOT EXISTS {  
                                ?prep lab:Противопоказано ?y .
                                ?y lab:Name "%s" .
                            }
                        }
                    """ % (danger))
        q = list(itertools.chain(*q))
        qs.append(list(q))
    return qs

qs = create_q(["назальный полип", "травма головы"])

print(join(qs))