from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('register', views.register),
    path('login', views.login),
    path('success', views.success),
    path('logout', views.logout),
    path('add_book', views.add_book),
    path('update_book', views.update),
    path('books/<int:book_id>', views.view_book),
    path('delete/<int:book_id>', views.delete),
    path('display/<int:book_id>', views.display),
    path('add_fav/<int:book_id>', views.add_fav),
    path('unfav/<int:book_id>', views.unfav),
]
