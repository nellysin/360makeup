from django.conf.urls import url
from django.conf import settings
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'^about-us/$', views.about_us, name='about_us'),

    # Product detail page
    # Regex explanation:
    # First character must be a letter
    # After that it can have lowercase letters, -s, and numbers
    url(r'^product/(?P<productname>([A-Z]|[a-z])([A-Z]|[a-z]|-|\d)*)/$', views.product_detail, name='product_detail'),

    # User-related pages
    url(r'^signup/$', views.signup, name='signup'),
    url(r'^login/$', auth_views.login, {'template_name': 'site360/signuplogin.html'}, name='signup_login'),
    url(r'^logout/$', auth_views.logout, {'next_page': settings.LOGOUT_REDIRECT_URL}, name='logout'),
    url(r'^success/$', views.auth_success, name='auth_success'),
    url(r'^profile/(?P<username>(\w|-|_)+)/$', views.profile_info, name='profile_info'),

    # Search-related pages
    url(r'^category/(?P<categoryname>([A-Z]|[a-z])*)/$', views.category_search, name='category_search'),

    url(r'^tutorials/$', views.tutorials, name='tutorials'),
    url(r'^stores/$', views.stores, name='stores'),

]
