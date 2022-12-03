from owlready2 import *
onto = get_ontology("5lab_2.owl")
onto.load()
with onto: sync_reasoner()

#3.1 Аналіз онтології:
#Пограмно, за допомогою обраного різонера, провести перевірку сумісності (consistency) онтології;
print("inconsistent_classes = ",list(onto.inconsistent_classes()))

#вирахувати кількість класів онтології;
print("count_classes = ", len(list(onto.classes())))

#вирахувати кількість екземплярів (Individuals) в онтології
print("count_individuals = ", len(list(onto.individuals())))

q1 = default_world.sparql("""SELECT DISTINCT ?x
                        { ?x a owl:Class .
                          ?y rdfs:domain ?x}""")

#знайти класи, що мають конкретну властивість 
print(f"Classes with propertys = {list(q1)}")

#Найти пару: (Вопрос - Принятый ответ)
q2 = default_world.sparql("""
                        Prefix lab: <http://www.semanticweb.org/home/ontologies/2021/11/untitled-ontology-5#>
                        SELECT ?x ?y
                        WHERE { ?x rdf:type lab:Question . 
                                ?x lab:Has_Answer ?y
                                ?y lab:Accepted 'true'}""")

print(list(q2))

with onto:
    #Добавить классы Company, Job
    class Company(onto.Resourse):
        pass

    class Job(onto.Resourse):
        pass
    
    #Добавить 2 ObjectProperty 
    #Добавить ограничение InverseFunctionalProperty
    class has_worker(ObjectProperty, InverseFunctionalProperty):
        domain = [Company]
        range = [onto.User]

    #Добавить ограничение FunctionalProperty
    class is_working_on(ObjectProperty, FunctionalProperty):
        domain = [onto.User]
        range = [Job]

    #Добавить 2 DataProperty
    class job_role(DataProperty):
        range = [str]

    class company_industry(DataProperty):
        industry = [str]

    AllDisjoint([Company, Job])

#Удалить 2 DataProperty
destroy_entity(onto["Answers"])
destroy_entity(onto["Questions"])

#Добавить два экземпляра
ancient_gaming = Company("ancient-gaming")
ancient_gaming.company_industry = ["Casino", "Gaming", "Shopping"]

senior_job_offer = Job("senior-full-stack-developer-fully-remote-ancient-gaming")
senior_job_offer.job_role = ["Full Stack Developer"]
#user "gumbo" is working on senior_job_offer
onto.gumbo.is_working_on = senior_job_offer

#Company ancient_gaming has worker gumbo
ancient_gaming.has_worker.append(onto.gumbo)

#Удалить 2 экземпляра
destroy_entity(onto["comment-000000"])
destroy_entity(onto["comment-88356146"])

#Удалить 2 ObjectProperty
destroy_entity(onto["Has_Member"])
destroy_entity(onto["Has_Comment"])

#Удалить 2 класса 
destroy_entity(onto["Collective"])
destroy_entity(onto["Revision"])

#Проверка на consistentsy
with onto: sync_reasoner()

onto.save("test.owl", format="rdfxml")