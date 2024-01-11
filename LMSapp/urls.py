from . import views, user_login
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from .views import *

urlpatterns = [
                  path('base', BaseView.as_view(), name='BASE'),
                  path('404', views.pagenotfound, name='404'),
                  path('', HomeView.as_view(), name='home'),
                  path('courses', views.singlecourse, name='singlecourse'),
                  path('courses/filterdata', views.filterdata, name="filterdata"),
                  path('course/<slug:slug>', views.coursedetails, name="coursedetails"),
                  path('search', views.searchcourse, name='searchcourse'),
                  path('contactus', views.contactus, name='contactus'),
                  path('aboutus', views.aboutus, name='aboutus'),
                  path('accounts/', include('django.contrib.auth.urls')),
                  path('accounts/register', user_login.REGISTER, name='register'),
                  path('accounts/doLogin', user_login.DO_LOGIN, name='doLogin'),
                  path('accounts/profile', user_login.PROFILE, name='profile'),
                  path('accounts/profile_update', user_login.Profile_Update, name='profileUpdate'),
                  path('checkout/<slug:slug>', views.checkout, name='checkout'),
                  path('author', admin.site.urls),
                  path('mycourse', views.mycourse, name='mycourse'),
                  path('paidregistered/<slug:slug>', views.paidregistered, name='paidregistered'),
                  path('register_course', views.register_course_details, name='registerCourse'),
                  path('auther_course_detail', views.auther_course_details, name='autherCourse'),

              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
