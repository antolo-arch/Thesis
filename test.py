from templater3 import Templater
documents_to_learn = ['<b> spam and eggs </b>', '<b> ham and spam </b>',
                          '<b> white and black </b>'] # list of documents
template = Templater()
for document in documents_to_learn:
    template.learn(document)

print('Template created:', template._template)


document_to_parse = '<b> yellow and blue </b>'
print('Parsing other document:', template.parse(document_to_parse))

print('Filling the blanks:', template.join(['', 'red', 'orange', '']))