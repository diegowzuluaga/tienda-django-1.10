from django.contrib import admin
from .models import cliente, producto, categoriaProducto, factura
# Register your models here.

class productoAdmin(admin.ModelAdmin):
	list_display = ('nombre','thumbnail','precio','stock')
	list_filter = ('nombre','precio')
	search_fields = ['nombre','precio']
	fields = ('nombre','descripcion',('precio','stock','imagen'),'categorias','status')

class facturaAdmin(admin.ModelAdmin):
    readonly_fields = ('total','cliente','producto','fecha')
	
admin.site.register(cliente)
admin.site.register(producto, productoAdmin)
admin.site.register(categoriaProducto)
admin.site.register(factura, facturaAdmin)