
from flask import Flask, request, jsonify
import xml.etree.ElementTree as ET
from datetime import datetime

app = Flask(__name__)

def Fecha(fecha):

        fecha = fecha

        tiempo = 0

        fecha_correcta = ''

        for i in fecha:

            if i.isdigit() or i == '/':

                fecha_correcta +=i



        dia = int(fecha_correcta[0] + fecha_correcta[1])
        mes = int(fecha_correcta[3] + fecha_correcta[4])
        año = int(fecha_correcta[6] + fecha_correcta[7] + fecha_correcta[8] + fecha_correcta[9])

        now = datetime.now()

        now_año = int(now.year)
        now_month = int(now.month)
        now_day = int(now.day)

        temp = año - now_año

        if temp > 0:

            tiempo += temp * 8760

        if mes > now_month:

            mes = mes *730

            tiempo += mes 

        elif mes<now_month: 

            tiempo += (now_month - mes )*730


        if dia > now_day:

            dia = dia *24

            tiempo += dia 

        elif dia<now_day: 

            tiempo += (now_day - dia )*24


        return tiempo


def Mensaje_confirmacion(nit, id_estancia, fecha):
        
        contenido = f'<consumo nitCliente="{nit}" idInstancia="{id_estancia}"> <fechaHora> {fecha} H </fechaHora> </consumo>'

        return contenido

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

        #CREACION DE MENSAJE DE RECIBIDO

        comienzo = '<?xml version="1.0"?> <listadoConsumos>'

        for r in clientes.findall('cliente'):

            id_nit = r.attrib.get('nit')

            listaInstancias = r.find('listaInstancias')

            for p in listaInstancias.findall('instancia'):

                id_instancia = p.attrib.get('id')

                tiempo = Fecha(p.find('fechaInicio').text)

                contenido = Mensaje_confirmacion(id_nit, id_instancia, tiempo)

                comienzo += contenido

        final = ' </listadoConsumos>'

        comienzo += final


        return comienzo #RETORNAR UN JSON CON MENSAJE DE DATOS CAPTURADOS

    except Exception as ex: #CAPTURA DE ERRORES ENVIANDO UN MENSAJE DE ERROR AL MOMENTO 

        return jsonify({'mensaje':'ERROR '}) #MENSAJE DE ERROR


@app.route('/Consultar-Recurso/<idRecurso>', methods = ["GET"])
    
def Consultar_Recurso(idRecurso):

    #try: 

        id_recurso = idRecurso

        tree = ET.parse('BD-Recursos.xml') #abrir xml

        root = tree.getroot() #obtener xml

        

        for i in root.findall('Recurso'):

            if i.attrib.get('id') == id_recurso:

                nombre = i.find('nombre').text
                abreviatura = i.find('abreviatura').text
                metrica = i.find('metrica').text
                tipo = i.find('tipo').text
                valorXhora = i.find('valorXhora').text

                contenido = jsonify({'nombre': nombre , 'abreviatura': abreviatura, 'metrica': metrica , 'tipo':tipo, 'valorXhora':valorXhora})

        return contenido

"""except Exception as ex:

        return jsonify({'mensaje':'ERROR '}) #MENSAJE DE ERROR"""

@app.route('/Consultar-Categorias/<idCategorias>', methods = ["GET"])

def Consultar_Categorias(idCategorias):

    id_Categoria = idCategorias

    tree = ET.parse('BD-Categorias.xml') #abrir xml

    root = tree.getroot() #obtener xml


    for i in root.findall('Categoria'):

        if i.attrib.get('id') == id_Categoria:

            nombre = i.find('nombre').text
            descripcion = i.find('descripcion').text
            Carga = i.find('cargaTrabajo').text

            contenido = jsonify({'nombre': nombre , 'descripcion': descripcion, 'Carga de Trabajo': Carga})


    return contenido


@app.route('/Consultar-Cliente/<nit>', methods = ["GET"])

def Consultar_Cliente(nit):

    nit = nit

    tree = ET.parse('BD-Clientes.xml') #abrir xml

    root = tree.getroot() #obtener xml


    for i in root.findall('Cliente'):

        if i.attrib.get('nit') == nit:

            nombre = i.find('nombre').text
            usuario= i.find('usuario').text
            clave = i.find('clave').text
            direccion = i.find('direccion').text
            correo = i.find('correo').text

            contenido = jsonify({'nombre': nombre , 'descripcion': usuario, 'Carga de Trabajo': clave, 'direccion': direccion, 'correo': correo})


    return contenido




if __name__ == '__main__':

    app.run(debug=True)





