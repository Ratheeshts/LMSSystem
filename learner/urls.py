"""

dashboard URL Configuration
Written by Ratheesh @ 20-Feb-2020
The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('dashboard/', include('dashboard.urls'))
        re_path(r'^read_material/(?P<pk>\d+)/$', views.read_material,name='read_material'),
url(
    r'^project_config/(?P<product>\w+)/(?P<project_id>\w+)/$',
    'tool.views.ProjectConfig',
    name='project_config'
),
"""
from django.urls import path,re_path
from . import views
urlpatterns = [
    path('', views.login_request,name='login'),
    path('login', views.login_request,name='login'),
    path('view_learning_materials', views.view_learning_materials,name='view_learning_materials'),
    re_path(r'^view_learning_materials/(?P<topic>.*)/$', views.view_learning_materials,name='view_learning_materials'),
    path('history', views.history,name='history'),
    re_path(r'^read_material/(?P<pk>\d+)/$', views.read_material,name='read_material'),
    path('add_learn_material', views.add_learn_material,name='add_learn_material'),
    path('add_learner', views.add_learner,name='add_learner'),
        path('learners', views.view_learners,name='learners'),

        path('materials', views.view_materials,name='materials'),

    path("logout", views.logout_request, name="logout"),
    re_path(r'^read_material/(?P<pk>\d+)/add_session', views.add_session,name='add_session')


]
