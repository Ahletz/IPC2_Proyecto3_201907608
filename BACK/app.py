
from flask import Flask, request, jsonify
import xml.etree.ElementTree as ET

app = Flask(__name__)

@app.route('/Principal', methods = ["POST"])

def Archivo_principal():

    try:

        #OBTENCION DEL CONTENIDO DEL MENSAJE ENVIADO POR MEDIO DEL POST
        contenido = request.data.decode(encoding='utf-8')
        Datos = open('BD-PRINCIPAL.xml', 'w')
        Datos.write(contenido)
        Datos.close()

        tree = ET.parse('BD-PRINCIPAL.xml') #abrir xml

        root = tree.getroot() #obtener xml

        #CREACION DE BD-XML PARA LOS DATOS 

        #BD-XML RECURSOS

        recursos = root.find('listaRecursos')

        head = ET.Element("Recursos")

        for i in recursos.findall('recurso'):


            id_recurso = i.attrib.get('id') #ID
            Nombre = i.find('nombre').text #NOMBRE 
            Abreviatura = i.find('abreviatura').text #ABREVIATRUA 
            Metrica = i.find('metrica').text #METRICA
            Tipo = i.find('tipo').text #TEXT            
            ValorxHora = i.find('valorXhora').text #VALOR POR HORA

            #CREACION DEL CONTENIDO DEL XML

            Recurso = ET.SubElement(head, 'Recurso', id = id_recurso) 

            ET.SubElement(Recurso, 'nombre').text = Nombre
            ET.SubElement(Recurso, 'abreviatura').text = Abreviatura
            ET.SubElement(Recurso, 'metrica').text = Metrica
            ET.SubElement(Recurso, 'tipo').text = Tipo
            ET.SubElement(Recurso, 'valorXhora').text = ValorxHora

        #CREACION DEL ARCHIVO XML CON EL CONTENIDO     
        create = ET.ElementTree(head)
        create.write('BD-Recursos.xml')


        #BD-XML CATEGORIAS 

        head = ET.Element('Categorias') #etiqueta del xml

        categorias = root.find('listaCategorias')

        for j in categorias.findall('categoria'):

            id_categoria = j.attrib.get('id')
            Nombre_categoria = j.find('nombre').text
            Descripcion = j.find('descripcion').text
            CargaTrabajo = j.find('cargaTrabajo').text

            Categoria = ET.SubElement(categorias, 'Categoria', id = id_categoria)

            ET.SubElement(Categoria, 'nombre').text = Nombre_categoria
            ET.SubElement(Categoria, 'descripcion').text = Descripcion
            ET.SubElement(Categoria, 'cargaTrabajo').text = CargaTrabajo

            ListaConfiguraciones = j.find('listaConfiguraciones')

            for k in ListaConfiguraciones.findall('configuracion'):

                id_configuracion = k.attrib.get('id')
                nombre_configuracion = k.find('nombre').text
                descripcion_configuracion = k.find('descripcion').text

                ListaConfig = ET.SubElement(categorias, 'listaConfiguraciones')

                Config = ET.SubElement(ListaConfig, 'configuracion', id= id_configuracion)
                ET.SubElement(Config, 'nombre').text = nombre_configuracion
                ET.SubElement(Config, 'descripcion').text = descripcion_configuracion

                Recursos_configurasion = k.find('recursosConfiguracion')

                for l in Recursos_configurasion.findall('recurso'):

                    id_recurso_config = l.attrib.get('id')
                    nombre_recurso = l.find('recurso').text


                    Recursos = ET.SubElement(Config, 'recursosConfiguracion')

                    ET.SubElement(Recursos, 'recurso', id= id_recurso_config).text = nombre_recurso
        
        create = ET.ElementTree(head)
        create.write('BD-Categorias.xml')



        return jsonify({'mensaje': 'DATOS ALMACENADOS'}) #RETORNAR UN JSON CON MENSAJE DE DATOS CAPTURADOS

    except Exception as ex: #CAPTURA DE ERRORES ENVIANDO UN MENSAJE DE ERROR AL MOMENTO 

        return jsonify({'mensaje':'ERROR '}) #MENSAJE DE ERROR

if __name__ == '__main__':

    app.run(debug=True)




