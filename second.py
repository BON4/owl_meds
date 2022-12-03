from owlready2 import *
onto = get_ontology("drugs.owl")
onto.load()

#Пользователь вводит симптом - ему предлагает препарат
q1 = default_world.sparql(""" 
                        Prefix lab: <http://www.semanticweb.org/home/ontologies/2022/10/untitled-ontology-32#>
                        SELECT ?x ?name
                        WHERE {
                            ?x rdf:type lab:Препарат .
                            ?x lab:Показано ?y .
                            ?y lab:Name ?name . FILTER contains(?name, "%s")
                        }
""" % ("бол"))

print(list(q1))

#Пользователь вводит препарат - ему показывает его сведения
q2 =  default_world.sparql(""" 
                        Prefix lab: <http://www.semanticweb.org/home/ontologies/2022/10/untitled-ontology-32#>
                        SELECT ?prep_n ?heal_n ?danger_n ?sides_n ?use_n ?combine_n
                        WHERE {
                            ?prep rdf:type lab:Препарат .
                            ?prep lab:Name "%s" .
                            ?prep lab:Name ?prep_n .
                            
                            ?prep lab:Показано ?heal .
                            ?heal lab:Name ?heal_n .

                            ?prep lab:Противопоказано ?danger .
                            ?danger lab:Name ?danger_n .            

                            ?prep lab:Побочный_эффект ?sides .
                            ?sides lab:Name ?sides_n . 

                            ?prep lab:Введение ?use .
                            ?use lab:Name ?use_n . 

                            ?prep lab:Сочетается ?combine .
                            ?combine lab:Name ?combine_n .                 
                        }
""" % ("Трамадол"))

print(list(q2))