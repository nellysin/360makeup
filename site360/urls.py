from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.home, name='home'),

    #Category search page regex explanation:
    #First character must be a letter
    #After that it can have lowercase letters, -s, and numbers
    url(r'^product/(?P<productname>[a-z]([a-z]|-|\d)*)/$', views.product_detail, name='product_detail'),
]
