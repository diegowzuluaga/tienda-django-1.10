from django.conf.urls import url
from  demo.apps.home.views import (index_view,about_view,productos_view,singleProduct_view,contacto_view,
		login_view, register_view, logout_view,generar_clientes,generar_productos)



urlpatterns = [#patterns('demo.apps.home.views',
    url(r'^$',index_view,name='vista_principal'),
	url(r'^about/$',about_view,name='vista_about'),
	url(r'^productos/page/(?P<pagina>.*)/$',productos_view,name='vista_productos'),
	url(r'^producto/(?P<id_prod>.*)/$',singleProduct_view,name='vista_single_producto'),
	url(r'^contacto/$',contacto_view,name='vista_contacto'),
	url(r'^login/$',login_view,name='vista_login'),
	url(r'^registro/$',register_view,name='vista_registro'),
	url(r'^logout/$',logout_view,name='vista_logout'),
	url(r'^generarClientes/$',generar_clientes,name='vista_generarClientes'),
	url(r'^generarProductos/$',generar_productos,name='vista_generarProducos'),
]
