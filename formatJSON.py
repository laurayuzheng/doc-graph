filename = 'data2.json'

text = open(filename,'r').read()

text = text.replace('\"nodes\"','nodes')
text = text.replace('\"edges\"','edges')
text = text.replace('\"id\"','id')
text = text.replace('\"name\"','name')
text = text.replace('\"name\"','name')
text = text.replace('\"cluster\"','cluster')
text = text.replace('\"source\"','source')
text = text.replace('\"target\"','target')

with open(filename, 'w') as filetowrite:
    filetowrite.write(text)
    filetowrite.close()
