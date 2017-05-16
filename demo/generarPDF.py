# -*- coding: utf-8 -*-
from io import BytesIO

from django.http import HttpResponse
from django.views.generic import ListView
from reportlab.platypus import SimpleDocTemplate, Paragraph, TableStyle
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import Table

from .models import Clientes

class IndexView(ListView):
    template_name = "index.html"
    model = Clientes
    context_object_name = "c"

def generar_pdf(request):
    print "Genero el PDF"
    response = HttpResponse(content_type='application/pdf')
    pdf_name = "clientes.pdf"  # llamado clientes
    # la linea 26 es por si deseas descargar el pdf a tu computadora
    # response['Content-Disposition'] = 'attachment; filename=%s' % pdf_name
    buff = BytesIO()
    doc = SimpleDocTemplate(buff,
                            pagesize=letter,
                            rightMargin=40,
                            leftMargin=40,
                            topMargin=60,
                            bottomMargin=18,
                            )
    clientes = []
    styles = getSampleStyleSheet()
    header = Paragraph("Listado de Clientes", styles['Heading1'])
    clientes.append(header)
    headings = ('Nombre', 'Email', 'Edad', 'Dirección')
    allclientes = [(p.nombre, p.email, p.edad, p.direccion) for p in Clientes.objects.all()]
    print allclientes

    t = Table([headings] + allclientes)
    t.setStyle(TableStyle(
        [
            ('GRID', (0, 0), (3, -1), 1, colors.dodgerblue),
            ('LINEBELOW', (0, 0), (-1, 0), 2, colors.darkblue),
            ('BACKGROUND', (0, 0), (-1, 0), colors.dodgerblue)
        ]
    ))
    clientes.append(t)
    doc.build(clientes)
    response.write(buff.getvalue())
    buff.close()
    return response
	
	2 Importo BytesIO nos permite un lugar de almacenamiento temporal del pdf

6 a la 10 importo todo lo que necesitare para generar mi documento:

SimpleDocTemplate: La plantilla del documento
Paragraph: Para escribir párrafos
TableSytle: Lo que hará bonita a nuestra tabla
getSampleStyleSheet: Importamos una clase de hoja de estilo
colors: Esto aún no descubro que hace 😆
letter: El tamaño de la hoja
Table: Nos permite crear tablas (igual esta el longTable)
23 decimos que va a hacer un documento PDF

24 damos el nombre al documento

26 descomentamos la linea si queremos descargar el documento a nuestra computadora

27 almacenamos BytesIO a la variable buff

28 configuramos nuestro documento

35 creamos una lista

36 almacenamos getSampleStyleSheet a una variable llamada styles

37, 38 agregamos un titulo a nuestro documento usando Paragraph

39 agregamos los encabezaos de las Columnas

40 aqui creamos una variable que almacena todos los datos que tengo en el modelo Clientes

43 creo una variable donde agrego a Table los nombres de las columnas con sus datos correspondientes que están el allclientes

44 doy color a la tabla

51 agrego todo a mi lista

52 genero el documento a partir de la lista clientes

53 Recupero el archivo almacenado

54 Librero la memoria

55 regreso la respuesta 