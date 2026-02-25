from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import *
# Create your views here.
def home(request):
    return render(request,'home.html')



def register_view(request):
    if request.method == "POST":
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        username = request.POST.get("username")
        email = request.POST.get("email")
        password1 = request.POST.get("password1")
        password2 = request.POST.get("password2")

        # Check passwords match
        if password1 != password2:
            messages.error(request, "Passwords do not match!")
            return redirect("register")

        # Check username exists
        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists!")
            return redirect("register")

        # Check email exists
        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already registered!")
            return redirect("register")

        # Create user
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password1,
            first_name=first_name,
            last_name=last_name
        )

        messages.success(request, "Account created successfully! Please login.")
        return redirect("login")

    return render(request, "register.html")


def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)

            if user.is_superuser:
                return redirect("admin_dashboard")
            else:
                return redirect("user_dashboard")
        else:
            messages.error(request, "Invalid username or password")
            return redirect("login")

    return render(request, "login.html")


def admin_dashboard(request):
    products = Cloth.objects.select_related('category').all().order_by('-created_at')
    users = User.objects.all().order_by('-date_joined')

    context = {
        'products': products,
        'users': users,
        'total_products': products.count(),
        'total_users': users.count(),
    }

    return render(request, 'admin.html', context)





def logout_view(request):
    logout(request)
    messages.success(request,"login successfull")
    return redirect("login")



def products(request):
    categories = Category.objects.all()

    if request.method == "POST":
        name = request.POST.get('name')
        size = request.POST.get('size')
        price = request.POST.get('price')
        description = request.POST.get('description')
        image = request.FILES.get('image')
        category_id = request.POST.get('category')
        color = request.POST.get('color')
        stock = request.POST.get('stock')

        Cloth.objects.create(
            name=name,
            size=size,
            price=price,
            description=description,
            image=image,
            category_id=category_id,
            color=color,
            stock=stock
        )

        messages.success(request, "Cloth added successfully!")
        return redirect('products')

    return render(request, 'products.html', {'categories': categories})

from .models import Category
from django.shortcuts import render, redirect
from django.contrib import messages


def category(request):
    categories = Category.objects.all()

    if request.method == "POST":
        name = request.POST.get('name')

        Category.objects.create(name=name)
        messages.success(request, "Category added successfully!")
        return redirect('add_category')

    return render(request, 'category.html', {'categories': categories})
from .models import Cloth

def user_dashboard(request):
    products = Cloth.objects.select_related('category').all().order_by('-created_at')

    return render(request, 'user_dash.html', {
        'products': products
    })


def cloth_detail(request, id):
    product = get_object_or_404(Cloth, id=id)

    # Check if this user already booked this cloth
    already_booked = Booking.objects.filter(
        user=request.user,
        cloth=product
    ).exists()

    if request.method == "POST" and not already_booked:
        quantity = int(request.POST.get("quantity"))
        address = request.POST.get("address")

        if quantity <= product.stock:
            # Reduce stock
            product.stock -= quantity
            product.save()

            # Save booking
            Booking.objects.create(
                user=request.user,
                cloth=product,
                quantity=quantity,
                address=address
            )

            messages.success(request, "Cloth booked successfully!")
            return redirect('cloth_detail', id=product.id)

    return render(request, 'cloth_detail.html', {
        'product': product,
        'already_booked': already_booked
    })
def my_orders(request):
    orders = Booking.objects.filter(user=request.user).select_related('cloth')

    for order in orders:
        order.total_price = order.quantity * order.cloth.price

    return render(request, 'my_orders.html', {
        'orders': orders
    })