from django.shortcuts import render_to_response, render
from django.template import RequestContext
from django.core import serializers

from demo.apps.ventas.models import producto, cliente
from demo.apps.home.forms import ContactForm, LoginForm,RegisterForm
from django.core.mail import EmailMultiAlternatives # Enviamos HTML
from django.contrib.auth.models import User
import django
from demo.settings import URL_LOGIN
from django.contrib.auth import login,logout,authenticate
from django.http import HttpResponseRedirect, HttpResponse
# Paginacion en Django
from django.core.paginator import Paginator,EmptyPage,InvalidPage
from django.contrib.auth.decorators import login_required
try:
    import django.utils.simplejson
except:
    import json as simplejson


from io import BytesIO
from django.views.generic import ListView
#from reportlab.platypus.tables import SimpleDocTemplate, Paragraph, TableStyle
from reportlab.platypus.tables import  TableStyle
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import Table



def index_view(request):
    #version = django.get_version()  
    #ctx = {'jango_version':version}
    return render_to_response('home/index.html')#, context_instance=RequestContext(request))


@login_required(login_url=URL_LOGIN)
def about_view(request):
	#print (request.session.session_key)
	mensaje = "Esto es un mensaje desde mi vista"
	ctx = {'msg':mensaje}
	return render(request,'home/about.html',ctx)#,context_instance=RequestContext(request))

def productos_view(request,pagina):
	if request.method=="POST":
		if "product_id" in request.POST:
			try:
				id_producto = request.POST['product_id']
				p = producto.objects.get(pk=id_producto)
				mensaje = {"status":"True","product_id":p.id}# Lo consume Js
				p.delete() # Elinamos objeto de la base de datos
				return HttpResponse(simplejson.dumps(mensaje),content_type='application/json')
			except:
				mensaje = {"status":"False"}# Lo consume Js
				return HttpResponse(simplejson.dumps(mensaje),content_type='application/json')
	lista_prod = producto.objects.filter(status=True) # Select * from ventas_productos where status = True
	paginator = Paginator(lista_prod,5) # Cuantos productos quieres por pagina? = 3
	try:
		page = int(pagina)
	except:
		page = 1
	try:
		productos = paginator.page(page)
	except (EmptyPage,InvalidPage):
		productos = paginator.page(paginator.num_pages)
	ctx = {'productos':productos}
	return render(request,'home/productos.html',ctx)#),context_instance=RequestContext(request))

def singleProduct_view(request,id_prod):
	prod = producto.objects.get(id=id_prod)
	cats = prod.categorias.all() # Obteniendo las categorias del producto encontrado
	ctx = {'producto':prod,'categorias':cats}
	return render(request,'home/SingleProducto.html',ctx)#,context_instance=RequestContext(request))

@login_required(login_url=URL_LOGIN)
def contacto_view(request):
	info_enviado = False # Definir si se envio la informacion o no se envio
	email = ""
	titulo = ""
	texto = ""
	if request.method == "POST":
		formulario = ContactForm(request.POST)
		if formulario.is_valid():
			info_enviado = True
			email = formulario.cleaned_data['Email']
			titulo = formulario.cleaned_data['Titulo']
			texto = formulario.cleaned_data['Texto']

			# Configuracion enviando mensaje via GMAIL
			to_admin = 'dolfasoftsas@gmail.com'
			html_content = "Informacion recibida de [%s] <br><br><br>***Mensaje****<br><br>%s"%(email,texto)
			msg = EmailMultiAlternatives('Correo de Contacto',html_content,'from@server.com',[to_admin])
			msg.attach_alternative(html_content,'text/html') # Definimos el contenido como HTML
			msg.send() # Enviamos  en correo
	else:
		formulario = ContactForm()
	ctx = {'form':formulario,'email':email,'titulo':titulo,'texto':texto,'info_enviado':info_enviado}
	return render(request,'home/contacto.html',ctx)#,context_instance=RequestContext(request))


def login_view(request):
	mensaje = ""
	if request.user.is_authenticated():
		return HttpResponseRedirect('/')
	else:
		if request.method == "POST":
			form = LoginForm(request.POST)
			if form.is_valid():
				next = request.POST['next']
				username = form.cleaned_data['username']
				password = form.cleaned_data['password']
				usuario = authenticate(username=username,password=password)
				if usuario is not None and usuario.is_active:
					login(request,usuario)
					request.session['carrito']=[]
					return HttpResponseRedirect(next)
				else:
					mensaje = "usuario y/o password incorrecto"
		print(request)			
		#next = request.REQUEST.get('next')# la proxima url
		#next = request.GET['next']
		next = "/"
		form = LoginForm()
		ctx = {'form':form,'mensaje':mensaje,'next':next}
		return render(request,'home/login.html',ctx)#,context_instance=RequestContext(request))

def logout_view(request):
	logout(request)
	return HttpResponseRedirect('/')



def register_view(request):
	form = RegisterForm()
	if request.method == "POST":
		form = RegisterForm(request.POST)
		if form.is_valid():
			usuario = form.cleaned_data['username']
			email = form.cleaned_data['email']
			password_one = form.cleaned_data['password_one']
			password_two = form.cleaned_data['password_two']
			u = User.objects.create_user(username=usuario,email=email,password=password_one)
			u.save() # Guardar el objeto
			return render(request,'home/thanks_register.html')#,context_instance=RequestContext(request))
		else:
			ctx = {'form':form}
			return 	render(request,'home/register.html',ctx)#,context_instance=RequestContext(request))
	ctx = {'form':form}
	return render(request,'home/register.html',ctx)#,context_instance=RequestContext(request))
	
def generar_clientes(request):
    print ("Genero el PDF")
    response = HttpResponse(content_type='application/pdf')
    pdf_name = "clientes.pdf"  # llamado clientes
    # la linea 26 es por si deseas descargar el pdf a tu computadora
    # response['Content-Disposition'] = 'attachment; filename=%s' % pdf_name
    buff = BytesIO()
    doc = SimpleDocTemplate(buff,
                            pagesize=letter,
                            rightMargin=10,
                            leftMargin=10,
                            topMargin=60,
                            bottomMargin=18,
                            )
    clientes = []
    styles = getSampleStyleSheet()
    header = Paragraph("Listado de Clientes", styles['Heading1'])
    clientes.append(header)
    headings = ('Nombre', 'Apellidos')
    allclientes = [(p.nombre, p.apellidos) for p in cliente.objects.all()]
    print (allclientes)

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

def generar_productos(request):
    print ("Genero el PDF")
    response = HttpResponse(content_type='application/pdf')
    pdf_name = "productos.pdf"  # llamado clientes
    # la linea 26 es por si deseas descargar el pdf a tu computadora
    # response['Content-Disposition'] = 'attachment; filename=%s' % pdf_name
    buff = BytesIO()
    doc = SimpleDocTemplate(buff,
                            pagesize=letter,
                            rightMargin=10,
                            leftMargin=10,
                            topMargin=60,
                            bottomMargin=18,
                            )
    productos = []
    styles = getSampleStyleSheet()
    header = Paragraph("Listado de Productos", styles['Heading2'])
    productos.append(header)
    headings = ('Nombre', 'Descripcion', 'precio', 'stock')
    allproductos = [(p.nombre, p.descripcion, p.precio, p.stock) for p in producto.objects.all()]
    print (allproductos)

    t = Table([headings] + allproductos)
    t.setStyle(TableStyle(
        [
            ('GRID', (0, 0), (3, -1), 1, colors.dodgerblue),
            ('LINEBELOW', (0, 0), (-1, 0), 2, colors.darkblue),
            ('BACKGROUND', (0, 0), (-1, 0), colors.dodgerblue)
        ]
    ))
    productos.append(t)
    doc.build(productos)
    response.write(buff.getvalue())
    buff.close()
    return response
"""
def generar_pdf(html):
    # Función para generar el archivo PDF y devolverlo mediante HttpResponse
    result = StringIO.StringIO()
    pdf = pisa.pisaDocument(StringIO.StringIO(html.encode("UTF-8")), result)
    if not pdf.err:
        return HttpResponse(result.getvalue(), mimetype='application/pdf')
    return HttpResponse('Error al generar el PDF: %s' % cgi.escape(html))

def libro_pdf(request):
    # vista de ejemplo con un hipotético modelo Libro
    html = render_to_string('productos.html', {'pagesize':'A4'}, context_instance=RequestContext(request))
    return generar_pdf(html)

"""