from django.conf.urls import url
from demo.apps.webServices.wsProductos.views import wsProductos_view

urlpatterns = [
	url(r'^ws/productos/$',wsProductos_view,name= "ws_productos_url"),
]