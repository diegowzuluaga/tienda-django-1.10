from django.conf.urls import url
from demo.apps.ventas.views import (add_product_view,edit_product_view,compra_producto_view,
	get_carrito_compras, borrar_carrito, comprar_carrito	)

urlpatterns = [#patterns('demo.apps.ventas.views',
	url(r'^add/producto/$',add_product_view,name= "vista_agregar_producto"),
	url(r'^edit/producto/(?P<id_prod>.*)/$',edit_product_view,name= "vista_editar_producto"),
	url(r'^compra/producto/(?P<id_prod>.*)/$',compra_producto_view,name= "vista_compra_producto"),
	url(r'^carrito/$',get_carrito_compras,name= "vista_carrito"),
	url(r'^borrar-carrito/$',borrar_carrito,name= "borrar_carrito"),
	url(r'^hacer-compra/$',comprar_carrito,name= "comprar"),
]