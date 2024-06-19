from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.views import View
from .forms import LoginForm, RegisterForm, CreateBookForm, UserEditForm
from django.contrib.auth.mixins import LoginRequiredMixin
from .permissions import SellerRequiredMixin, AdminRequiredMixin
from .models import Book, Cart, Category, User
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator


class LoginView(View):
    def get(self, request):
        form = LoginForm()
        return render(request, 'shop/login.html', {"form": form})

    def post(self, request):
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('shop:home')

        form = LoginForm()
        return render(request, 'shop/login.html', {"form": form})


class RegisterView(View):
    def get(self, request):
        form = RegisterForm()
        return render(request, 'shop/register.html', {"form": form})

    def post(self, request):
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            password = form.cleaned_data['password']
            user.set_password(password)
            user.save()

            return redirect('shop:login')
        form = RegisterForm()
        return render(request, 'shop/register.html', {"form": form})


class ProfileView(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, 'shop/profile.html')


class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect('shop:login')


class AllBookView(View):
    def get(self, request):
        books = Book.objects.filter(in_stock=True)
        cart = Cart.objects.count()
        return render(request, 'home.html', {"books": books, "cart": cart})


class BookDetailView(View):
    def get(self, request, book_id):
        book = get_object_or_404(Book, id=book_id)
        cart = Cart.objects.count()
        return render(request, 'shop/detail.html', {"book": book, "cart": cart})

    def post(self, request, book_id):
        book = get_object_or_404(Book, id=book_id)
        quantity = int(request.POST['cart'])
        if Cart.objects.filter(book=book).exists():
            cart = Cart.objects.filter(book=book).first()
            cart.quantity += quantity
            cart.save()
        else:
            cart = Cart()
            cart.book = book
            cart.quantity = quantity
            cart.save()

        return redirect('shop:home')


class CartDetailView(View):
    def get(self, request):
        books = Cart.objects.all()
        return render(request, 'shop/cart_detail.html', {"books": books})


def delete_from_cart(request, book_id):
    cart = get_object_or_404(Cart, id=book_id)
    cart.delete()
    return redirect('shop:home')

def delete_from_users(request, user_id):
    user = get_object_or_404(User, id=user_id)
    user.delete()
    return redirect('shop:users_view')

class CreateView(SellerRequiredMixin,View):
    def get(self, request):
        form = CreateBookForm()
        return render(request, 'shop/create_book.html', {"form": form})

    def post(self, request):
        form = CreateBookForm(request.POST, request.FILES)
        if form.is_valid():
            category_id = form.cleaned_data['category'].id
            category = get_object_or_404(Category, id=category_id)
            book = form.save(commit=False)
            book.category = category
            book.save()
            return redirect('shop:home')
        form = CreateBookForm()
        return render(request, 'shop/create_book.html', {"form": form})


def delete_from_book(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    book.delete()
    return redirect('shop:home')


class UsersView(AdminRequiredMixin,View):
    def get(self, request):
        users = User.objects.all()
        return render(request, 'shop/users_detail.html', {"users": users})


@method_decorator(login_required, name='dispatch')
class UserEditView(View):
    def get(self, request, id):
        user = get_object_or_404(User, id=id)
        form = UserEditForm(instance=user)
        return render(request, 'shop/edit_user.html', {"form": form})

    def post(self, request, id):
        user = get_object_or_404(User, id=id)
        form = UserEditForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('shop:users_view')
        return render(request, 'shop/edit_user.html', {"form": form})




