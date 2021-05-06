from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:entry>/", views.show_entry, name='entry'),
    path("search", views.search_entry, name='search'),
    path("new", views.create_entry, name='create'),
    path("error", views.submit_entry, name='error'),
    path("wiki/<str:entry_title>/delete", views.delete_entry, name='delete'),
    path('wiki/<str:entry_title>/edit', views.render_edit_page, name='render_edit'),
    path('update', views.update_entry, name='edit'),
    path('random/', views.random_entry, name='random')
]
