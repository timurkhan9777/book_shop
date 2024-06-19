from django.urls import path
from .views import (LoginView,RegisterView,ProfileView,LogoutView,BookDetailView,
                    CartDetailView,delete_from_cart,CreateView,delete_from_book,
                    UsersView,UserEditView,AllBookView,delete_from_users)

app_name='shop'

urlpatterns = [
    path('',AllBookView.as_view(),name='home'),
    path('login/',LoginView.as_view(),name='login'),
    path('logout/',LogoutView.as_view(),name='logout'),
    path('register/',RegisterView.as_view(),name='register'),
    path('profile/',ProfileView.as_view(),name='profile'),
    path('book-detail/<int:book_id>/',BookDetailView.as_view(),name='book_detail'),
    path('cart-delete/<int:book_id>/',delete_from_cart,name='delete'),
    path('book-delete/<int:book_id>/',delete_from_book,name='book_delete'),
    path('edit-user/<int:id>/',UserEditView.as_view(),name='edit_user'),
    path('cart-detail/',CartDetailView.as_view(),name='cart_detail'),
    path('create-book/',CreateView.as_view(),name='create_book'),
    path('users-view/',UsersView.as_view(),name='users_view'),
    path('users-delete/<int:user_id>/',delete_from_users,name='users_delete'),
]