from django.db import models


# Create your models here.

class cliente(models.Model):
	nombre		= models.CharField(max_length=200)
	apellidos	= models.CharField(max_length=200)
	status		= models.BooleanField(default=True)

	def __str__(self):
		nombreCompleto = "%s %s"%(self.nombre,self.apellidos)
		return nombreCompleto

class categoriaProducto(models.Model):
	nombre 	= models.CharField(max_length=200)
	descripcion = models.TextField(max_length=400)

	def __str__(self):
		return self.nombre

class producto(models.Model):

	def url(self,filename):
		ruta = "MultimediaData/Producto/%s/%s"%(self.nombre,str(filename))
		return ruta

	def thumbnail(self):
		return '<a href="/media/%s"><img src="/media/%s" width=50px heigth=50px/></a>'%(self.imagen,self.imagen)

	thumbnail.allow_tags = True

	nombre		= models.CharField(max_length=100)
	descripcion	= models.TextField(max_length=300)
	status		= models.BooleanField(default=True)
	imagen 		= models.ImageField(upload_to=url,null=True,blank=True)
	precio		= models.DecimalField(max_digits=6,decimal_places=2)
	iva			= models.FloatField()
	stock		= models.IntegerField()
	categorias	= models.ManyToManyField(categoriaProducto,null=True,blank=True)

	def __str__(self):
		return u'%s' % (self.nombre)
		
class factura(models.Model):
    total = models.IntegerField()
    cliente = models.ForeignKey(cliente)
    producto = models.ForeignKey(producto)
    fecha = models.DateField()
   
    def __str__(self):
        return u'%s %s'%(self.cliente,self.producto)  	
        