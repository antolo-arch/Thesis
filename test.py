from templater3 import Templater
import re 
# documents_to_learn = ['<b> spam and eggs </b>', '<b> ham and spam </b>',
#                           '<b> white and black </b>'] # list of documents
# template = Templater()
# for document in documents_to_learn:
#     template.learn(document)

# print('Template created:', template._template)


# document_to_parse = '<b> yellow and blue </b>'
# print('Parsing other document:', template.parse(document_to_parse))

# print('Filling the blanks:', template.join(['', 'red', 'orange', '']))

class WikiList:

    def __init__(self, tab_list: list) -> None:
        file_name, word_list = tab_list.split('\t')
        self.file_name: str = file_name
        self.word_list: list = word_list.strip().split('\\n')
        self.template: Templater = None
        self.entities_word_list: list = self.create_entity_word_list()

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

    def create_entity_word_list(self):
        entity_word_list = []
        for word in self.word_list:
            entity_word_list.append(str(re.findall(r'\[\[(.+?)\]\]',word)))
        return entity_word_list


# Test templater 
lines = open('simplewiki-20211120-lists-1k.tsv').readlines()
for line in lines[100:101]:
    one_list = WikiList(line)
    print(one_list.entities_word_list)
    print(one_list.word_list)
    # word_list = word_list.split('\\n')
    # print(word_list)
