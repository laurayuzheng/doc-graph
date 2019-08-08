''' Formats JSON data (data.json in this case) to copy and paste into html file using Alchemy.
This is purely for application with AlchemyJS, since the library cannot read directly from a JSON file locally.
'''

#filename = 'data.json'

def format(filename):
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
