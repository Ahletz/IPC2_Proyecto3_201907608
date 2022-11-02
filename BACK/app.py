
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

        head = ET.Element('Categorias') #etiqueta del xml PRINCIPAL CATEGORIAS

        categorias = root.find('listaCategorias')

        for j in categorias.findall('categoria'):

            id_categoria = j.attrib.get('id')
            Nombre_categoria = j.find('nombre').text
            Descripcion = j.find('descripcion').text
            CargaTrabajo = j.find('cargaTrabajo').text

            #SUBELEMENTOS DE CATETGORIAS

            Categoria = ET.SubElement(head, 'Categoria', id = id_categoria)

            ET.SubElement(Categoria, 'nombre').text = Nombre_categoria
            ET.SubElement(Categoria, 'descripcion').text = Descripcion
            ET.SubElement(Categoria, 'cargaTrabajo').text = CargaTrabajo

            ListaConfig = ET.SubElement(Categoria, 'listaConfiguraciones')

            ListaConfiguraciones = j.find('listaConfiguraciones')

            for k in ListaConfiguraciones.findall('configuracion'):

                id_configuracion = k.attrib.get('id')
                nombre_configuracion = k.find('nombre').text
                descripcion_configuracion = k.find('descripcion').text

                #SUBELEMNTOS DE CATEGORIA
                Config = ET.SubElement(ListaConfig, 'configuracion', id= id_configuracion)
                
                ET.SubElement(Config, 'nombre').text = nombre_configuracion
                ET.SubElement(Config, 'descripcion').text = descripcion_configuracion

                Recursos = ET.SubElement(Config, 'recursosConfiguracion')

                Recursos_configurasion = k.find('recursosConfiguracion')

                for l in Recursos_configurasion.findall('recurso'):

                    id_recurso_config = l.attrib.get('id')
                    nombre_recurso = l.text
                    ET.SubElement(Recursos, 'recurso', id= id_recurso_config).text = nombre_recurso
        
        create = ET.ElementTree(head)
        create.write('BD-Categorias.xml')


        #BD-XML CLIENTES

        clientes = root.find('listaClientes')

        head = ET.Element('listaClientes') #ETIQUETA INICIAL DEL DOCUMENTO


        for m in clientes.findall('cliente'):

            id_nit = m.attrib.get('nit')
            nombre_categoria = m.find('nombre').text
            usuario =  m.find('usuario').text
            clave =  m.find('clave').text
            direccion =  m.find('direccion').text
            correo =  m.find('correoElectronico').text

            listaInstancias = m.find('listaInstancias')

            #CREACION DE BS-XML 
            cliente = ET.SubElement(head, 'Cliente', nit = id_nit)

            ET.SubElement(cliente, 'nombre').text = nombre_categoria
            ET.SubElement(cliente, 'usuario').text = usuario
            ET.SubElement(cliente, 'clave').text = clave
            ET.SubElement(cliente, 'direccion').text = direccion
            ET.SubElement(cliente, 'correo').text = correo

            Instancias = ET.SubElement(cliente, 'listaInstancias')

            for n in listaInstancias.findall('instancia'):

                id_instancia = n.attrib.get('id')
                idConfiguracion = n.find('idConfiguracion').text
                nombre_instancia = n.find('nombre').text
                fechaInicio = n.find('fechaInicio').text
                estado = n.find('estado').text
                fechaFinal = n.find('fechaFinal').text


                Instancia = ET.SubElement(Instancias, 'Instancia', id= id_instancia)

                ET.SubElement(Instancia, 'nombre').text = nombre_categoria
                ET.SubElement(Instancia, 'idConfiguracion').text = idConfiguracion
                ET.SubElement(Instancia, 'nombre').text = nombre_instancia
                ET.SubElement(Instancia, 'fechaInicio').text = fechaInicio
                ET.SubElement(Instancia, 'estado').text = estado
                ET.SubElement(Instancia, 'fechaFinal').text = fechaFinal

        
        create = ET.ElementTree(head)
        create.write('BD-Clientes.xml')


        return jsonify({'mensaje': 'DATOS ALMACENADOS'}) #RETORNAR UN JSON CON MENSAJE DE DATOS CAPTURADOS

    except Exception as ex: #CAPTURA DE ERRORES ENVIANDO UN MENSAJE DE ERROR AL MOMENTO 

        return jsonify({'mensaje':'ERROR '}) #MENSAJE DE ERROR

if __name__ == '__main__':

    app.run(debug=True)




