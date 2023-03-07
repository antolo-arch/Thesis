from templater3 import Templater
import re 
from wikimapper import WikiMapper
from titlecase import titlecase
from SPARQLWrapper import SPARQLWrapper, JSON

user_agent = "ThesisDataExtractor @github antolo-arch"
sparql = SPARQLWrapper("https://query.wikidata.org/sparql", agent=user_agent)

class WikiList:

    def __init__(self, tab_list: list) -> None:
        file_name, word_list = tab_list.split('\t')
        self.file_name: str = file_name
        self.word_list: list = word_list.strip().split('\\n')
        self.entities_word_list: list = self.create_entity_word_list()
        self.entities_id_list: list = self.create_entity_id_list()

    def create_template(self):
        template = Templater()
        for word in self.word_list:
            print(word)
            template.learn(word)
        self.template = template
        return self.template._template

    def try_template(self):
        word_to_parse = self.word_list[0]
        print(word_to_parse, self.template._template, self.template.parse(word_to_parse))

    def create_entity_word_list(self) -> list:
        entity_word_list = []
        for word in self.word_list:
            entity_word_list.append(re.findall(r'\[\[(.+?)\]\]',word))
        return entity_word_list

    def preprocess_entity(self, entity: str) -> str:
        if entity.find("|"):
            entity = entity.split("|")
            entity = entity[0]
        entity = entity.replace('wikt:',"")

        title_case_entity = titlecase(entity).replace(' ', '_')

        joined = entity.replace(' ', '_')

        capitalized_entity = entity.replace(' ', '_').capitalize()
        
        return title_case_entity, capitalized_entity, joined

    def create_entity_id_list(self) -> list:
        results = []
        for entities in self.entities_word_list:
            one_list = []
            for entity in entities:
                title_case, capitalized, joined = self.preprocess_entity(entity)
                id = mapper.title_to_id(title_case)
                if id is None:
                    id = mapper.title_to_id(capitalized)
                    if id is None:
                        id = mapper.title_to_id(joined)
                if id is not None:
                    one_list.append(id)
                else:
                    one_list.append("")
            results.append(one_list)
        return results

    def get_instance_of(self, entity: str) -> 'list[str]':
        instance_of = []
        query = '''SELECT ?classLabel WHERE {{
        wd:{entity} wdt:P31 ?class.
            SERVICE wikibase:label {{
            bd:serviceParam wikibase:language "en" .
            }}
        }}'''.format(entity=entity)
        sparql.setQuery(query)

        sparql.setReturnFormat(JSON)
        results = sparql.query().convert()
        for result in results['results']['bindings']:
            instance_of.append(result['classLabel']['value'])
        return instance_of

    def create_instance_counter(self):
        instance_counter = {}
        for entities in self.entities_id_list:
            for entity in entities:
                instances = self.get_instance_of(entity)
                for instance in instances:
                    if instance in instance_counter:
                        instance_counter[instance]+=1
                    else:
                        instance_counter[instance]=1
        return instance_counter
    
    def create_replaced_entities_with_id_list(self):
        pass
    #replace entities with the first instance, and then use templater
    

mapper = WikiMapper("index_enwiki-latest.db")
lines = open('simplewiki-20211120-lists-1k.tsv').readlines()
for line in lines[:1]:
    one_list = WikiList(line)
    word_list = one_list.word_list
    entity_id_list = one_list.entities_id_list
    entity_word_list = one_list.entities_word_list
    for x, row in enumerate(word_list):
        for i, word in enumerate(entity_word_list[x]):
            if entity_id_list[x][i] == "":
                #if id is unrecognizable, delete the row
                pass
            row = row.replace(f'[[{word}]]',entity_id_list[x][i])
        print(row)
    print(one_list.get_instance_of("Q2532"))
            
    