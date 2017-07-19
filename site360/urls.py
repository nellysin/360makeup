from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'^about-us$', views.about_us, name='about_us'),

    #Category search page regex explanation:
    #First character must be a letter
    #After that it can have lowercase letters, -s, and numbers
    url(r'^product/(?P<productname>[A-Z][a-z]([a-z]|-|\d)*)/$', views.product_detail, name='product_detail'),
    url(r'^signuplogin$', views.signup_login, name='signup_login'),
]
