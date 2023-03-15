from django.urls import path

from . import views

urlpatterns = [
    path('config/', views.index, name='config'),
    path('config/user/', views.user, name='user'),
    path('config/user/set', views.setuser, name='setuser'),
    path('config/add', views.addgame, name='add'),
    path('config/addalias', views.addalias, name='addalias'),
    path('config/deletealias', views.deletealias, name='deletealias'),
    path('config/delete', views.deletegame, name='delete'),
    path('config/<str:game_code>/categories/',
         views.categories, name='categories'),
    path('config/<str:game_code>/categories/add',
         views.addcategory, name='addcategory'),
    path('config/<str:game_code>/categories/addcategoryalias',
         views.addcategoryalias, name='addcategoryalias'),
    path('config/<str:game_code>/categories/deletecategoryalias',
         views.deletecategoryalias, name='deletecategoryalias'),
    path('config/<str:game_code>/categories/deletecategory',
         views.deletecategory, name='deletecategory'),
    path('config/<str:game_code>/categories/changelevel',
         views.changelevel, name='changelevel'),
    path('config/<str:game_code>/categories/<str:category>/filter/',
         views.variables, name='variables'),
    path('config/<str:game_code>/categories/<str:category>/filter/add',
         views.addfilter, name="addfilter"),
    path('config/<str:game_code>/categories/<str:category>/filter/delete',
         views.deletefilter, name="deletefilter"),
    path('about/', views.about, name='about'),
    path('pb/about', views.helpmsg, name='helpmsg'),
    path('pb/help', views.help, name='help'),
    path('pb/<str:game_code>+<str:category_code>+<str:srdc_guest>',
         views.srdcrequest, name='srdcrequest'),
    path('pb/<str:game_code>+<str:category_code>',
         views.srdcrequest, name='srdcrequest'),
    path('pb/<str:game_code>', views.multisrdcrequest, name='multisrdcrequest')
]
