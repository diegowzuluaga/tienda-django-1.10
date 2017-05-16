from django.shortcuts import render_to_response, render
from django.template import RequestContext
from demo.apps.ventas.forms import addProductForm
from demo.apps.ventas.models import producto, factura
from django.http import HttpResponseRedirect
from datetime import datetime, date, time, timedelta


def edit_product_view(request,id_prod):
	info = "iniciado"
	prod = producto.objects.get(pk=id_prod)
	if request.method == "POST":
		form = addProductForm(request.POST,request.FILES,instance=prod)
		if form.is_valid():
			edit_prod = form.save(commit=False)
			form.save_m2m()
			edit_prod.status = True
			edit_prod.save() # Guardamos el objeto
			info = "Correcto"
			return HttpResponseRedirect('/producto/%s/'%edit_prod.id)
	else:
		form = addProductForm(instance=prod)
	ctx = {'form':form,'informacion':info}
	return render(request,'ventas/editProducto.html',ctx)#,context_instance=RequestContext(request))

def add_product_view(request):
	info = "iniciado"
	if request.method == "POST":
		form = addProductForm(request.POST,request.FILES)
		if form.is_valid():
			add = form.save(commit=False)
			add.status = True
			add.save() # Guardamos la informacion
			form.save_m2m() # Guarda las relaciones de ManyToMany
			info = "Guardado satisfactoriamente"
			return HttpResponseRedirect('/producto/%s'%add.id)
	else:
		form = addProductForm()
	ctx = {'form':form,'informacion':info}
	return render(request,'ventas/addProducto.html',ctx)#,context_instance=RequestContext(request)) 

"""
def add_product_view(request):
	info = "Inicializando" 
	if request.user.is_authenticated():
		if request.method == "POST":
			form = addProductForm(request.POST,request.FILES)# request.FILES para la imagen
			if form.is_valid():
				nombre = form.cleaned_data.get('nombre')
				descripcion = form.cleaned_data.get('descripcion')
				imagen = form.cleaned_data.get('imagen') # Esto se obtiene con el request.FILES
				precio = form.cleaned_data.get('precio')
				stock = form.cleaned_data.get('stock')
				p = producto()
				if imagen: # Generamos una pequenia validacion.
					p.imagen = imagen
				p.nombre 		=  nombre
				p.descripcion 	= descripcion
				p.precio 		= precio
				p.stock 		= stock
				p.status = True
				p.save() # Guardar la informacion
				info = "Se guardo satisfactoriamente!!!!!"
			else:
				info = "informacion con datos incorrectos"			
		form = addProductForm()
		ctx = {'form':form, 'informacion':info}
		#return render_to_response('ventas/addProducto.html',ctx)#,context_instance=RequestContext(request))
		#return render(request,'ventas/addProducto.html',ctx)#,context_instance=RequestContext(request))
		return render(request,'ventas/addProducto.html',ctx)#,context_instance=RequestContext(request))
	else:
		return HttpResponseRedirect('/')
"""
"""
def edit_product_view(request,id_prod):
	info = ""
	p = producto.objects.get(id=id_prod)
	if request.method == "POST":
		form = addProductForm(request.POST,request.FILES)
		if form.is_valid():
				nombre = form.cleaned_data['nombre']
				descripcion = form.cleaned_data['descripcion']
				imagen = form.cleaned_data['imagen'] # Esto se obtiene con el request.FILES
				precio = form.cleaned_data['precio']
				stock = form.cleaned_data['stock']
				p.nombre 		=  nombre
				p.descripcion 	= descripcion
				p.precio 		= precio
				p.stock 		= stock
				if imagen:
					p.imagen = imagen
				p.save() # Guardar la informacion
				info = "Se guardo satisfactoriamente!!!!!"
				return HttpResponseRedirect('/producto/%s'%p.id)
	if request.method == "GET":
		form = addProductForm(initial={
									'nombre':p.nombre,
									'descripcion':p.descripcion,
									'precio':p.precio,
									'stock':p.stock,
			})
	ctx = {'form':form,'info':info,'producto':p}
	return render_to_response('ventas/editProducto.html',ctx,context_instance=RequestContext(request))


def edit_product_view(request,id_prod):
	info = "iniciando"
	prod = producto.objects.get(pk=id_prod)
	if request.method == "POST":
		form = addProductForm(request.POST,request.FILES,instance=prod)
		if form.is_valid():
				edit_prod = form.save(commit=False)
				form.save_m2m()
				edit_prod.status = True
				edit_prod.save()
				info = "Se guardo satisfactoriamente!!!!!"
				return HttpResponseRedirect('/producto/%s/'%edit_prod.id)
	else:
		form = addProductForm(instance = prod)
	ctx = {'form':form,'informacion':info}
	return render_to_response('ventas/editProducto.html',ctx)#,context_instance=RequestContext(request)) 		
"""	 
def compra_producto_view(request,id_prod):
	if request.user.is_authenticated():
		p = producto.objects.get(pk = id_prod)
		#cliente = request.user
		#print(cliente)
		#color="blue"
		lista = request.session['carrito']
		lista.append(p.id)
		#request.session['carrito'].append(p.id)
		request.session['carrito']=lista
		print(request.session['carrito'])
		print(lista	)
		return HttpResponseRedirect("/productos/page/1")
	else:
		return HttpResponseRedirect("/login/")


"""
def compra_producto_view(request,id_prod):
	if request.user.is_authenticated():
		p = producto.objects.get(pk = id_prod)
		dic = request.session['carrito']
		keys = dic.keys()
		if not p.nombre in keys:
			dic[p.nombre] = [1,p]
		else:
			dic[p.nombre] =[dic[p.nombre][0]+1,p]
		request.session['carrito']=dic
		print(request.session['carrito'])
		return HttpResponseRedirect("/productos/page/1")
	else:
		return HttpResponseRedirect("/login/")		
"""

def get_carrito_compras(request):
	productos = request.session['carrito']
	lista = []
	for p in productos:
		produ = producto.objects.get(pk = p)
		#precio   = produ.precio
		#iva      = produ.iva
		#p_total  = float(precio)*(1+iva/100)
		#produ.append(p_total)
		lista.append(produ)
	return render(request,'ventas/carrito.html',{'productos':lista})#,context_instance=RequestContext(request))

def borrar_carrito(request):
	lista = []
	request.session['carrito'] = lista
	return render(request,'ventas/carrito.html',{'productos':lista})

def comprar_carrito(request):
	productos = request.session['carrito']
	f = factura.objects.count()+1
	lista = []
	total = 0
	for p in productos:
		lis      = {}
		produ    = producto.objects.get(pk = p)
		#lis.append(produ.nombre)
		item     = produ.id
		nombre   = produ.nombre
		cantidad = 1
		#lis.append(cantidad)
		precio   = produ.precio
		#lis.append(str(produ.precio))
		iva      = produ.iva
		#lis.append(produ.iva)
		p_total  = round(float(produ.precio)*(1+produ.iva/100),2)
		#lis.append(p_total)
		lis      = {'item': item, 'producto': nombre, 'cantidad': cantidad, 'precio':precio, 'iva':iva, 'p_total':p_total}
		lista.append(lis)
		total   += p_total
		#lista.append(produ)
	fecha = datetime.now()
	context = {'productos': lista, 'total': total, 'fecha': fecha, 'factura':f}	
	print(lista)
	print(total)
	return render(request,'ventas/factura.html',context)



	
	
	