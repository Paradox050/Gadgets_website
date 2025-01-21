from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Product, Category, Order, Customer, Cart, CartItem,OrderItem
from .forms import SignupForm, ProfileForm, CheckoutForm
from django.http import JsonResponse, HttpResponseRedirect, Http404
from django.db import transaction
import os
from django.conf import settings
from django.contrib.auth.forms import AuthenticationForm


def home(request):
    categories = Category.objects.all()  # Fetch all categories (Mobiles, Cameras, Televisions)
    featured_products = Product.objects.filter(is_featured=True)  # Display featured products if any
    return render(request, 'core/home.html', {'categories': categories, 'featured_products': featured_products})

def category_view(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    products = Product.objects.filter(category=category)
    
    # Define images for electronics categories
    category_images = {
        1: 'assets/mobiles_header.png',
        2: 'assets/cameras_header.png',
        3: 'assets/televisions_header.png',
    }
    
    header_image_url = category_images.get(category_id, 'assets/default_header.jpg')
    
    return render(request, 'core/category.html', {'category': category, 'products': products, 'header_image_url': header_image_url})


def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    return render(request, 'core/productdetail.html', {'product': product})


@login_required
def cart_view(request):
    try:
        cart = Cart.objects.get(user=request.user, is_active=True)
    except Cart.DoesNotExist:
        cart = None

    cart_items = cart.items.all() if cart else []
    total_items = sum(item.quantity for item in cart_items)
    total_price = sum(item.product.price * item.quantity for item in cart_items)

    return render(request, 'core/cart.html', {
        'cart': cart,
        'total_items': total_items,
        'total_price': total_price
    })


# views.py

@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    
    # Get selected attributes
    ram = request.GET.get('ram')
    storage = request.GET.get('storage')
    color = request.GET.get('color')
    
    # Check if the cart exists
    cart, created = Cart.objects.get_or_create(user=request.user, is_active=True)
    
    # Create or update the cart item
    cart_item, created = CartItem.objects.get_or_create(
        product=product,
        cart=cart,
        ram=ram,
        storage=storage,
        color=color,
    )
    
    # Update the quantity if the item already exists
    if not created:
        cart_item.quantity += 1
    cart_item.save()
    
    return redirect('cart')  # Redirect to the cart page



@login_required
def update_cart_item(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id)
    new_quantity = int(request.GET.get('quantity', 1))

    if new_quantity > 0:
        cart_item.quantity = new_quantity
        cart_item.save()
    else:
        cart_item.delete()

    return redirect('cart')

@login_required
def remove_from_cart(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id)
    cart_item.delete()
    return redirect('cart')


@login_required
def checkout(request):
    # Retrieve the user's cart
    cart = Cart.objects.get(user=request.user)
    
    # Calculate the total amount for the cart
    total_amount = cart.total_price()
    
    # Create the order
    order = Order.objects.create(user=request.user, total_amount=total_amount, payment_mode='COD')
    
    # Process each cart item
    for cart_item in cart.items.all():
        # Get the product from the cart item
        product = cart_item.product
        
        # Get the selected RAM and storage from the cart item (assuming these are stored in CartItem)
        ram = cart_item.ram  # For example: '4GB', '8GB'
        storage = cart_item.storage  # For example: '128GB', '256GB'
        
        # Determine the correct stock field based on RAM and Storage selection
        if ram == '4GB' and storage == '128GB':
            product.stock_4gb_128gb -= cart_item.quantity
        elif ram == '4GB' and storage == '256GB':
            product.stock_4gb_256gb -= cart_item.quantity
        elif ram == '4GB' and storage == '512GB':
            product.stock_4gb_512gb -= cart_item.quantity
        elif ram == '4GB' and storage == '1TB':
            product.stock_4gb_1tb -= cart_item.quantity
        elif ram == '8GB' and storage == '128GB':
            product.stock_8gb_128gb -= cart_item.quantity
        elif ram == '8GB' and storage == '256GB':
            product.stock_8gb_256gb -= cart_item.quantity
        elif ram == '8GB' and storage == '512GB':
            product.stock_8gb_512gb -= cart_item.quantity
        elif ram == '8GB' and storage == '1TB':
            product.stock_8gb_1tb -= cart_item.quantity
        
        # Save the product with updated stock
        product.save()
        
        # Create the order item with the selected variant's price and quantity
        OrderItem.objects.create(
            order=order,
            product=product,
            ram=ram,
            storage=storage,
            quantity=cart_item.quantity,
            price=product.price * cart_item.quantity,
        )
    
    # Empty the cart after successful checkout
    cart.items.all().delete()
    
    # Render the receipt page
    return render(request, 'core/receipt.html', {'order': order, 'total_amount': total_amount})


def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            return redirect('profile')
        else:
            messages.error(request, 'Invalid credentials!')
    else:
        form = AuthenticationForm()
    return render(request, 'core/login.html', {'form': form})

def signup_view(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Account created successfully! You can now login.')
            return redirect('login')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = SignupForm()
    return render(request, 'core/signup.html', {'form': form})

@login_required
def profile_view(request):
    customer, created = Customer.objects.get_or_create(user=request.user)
    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=customer)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('profile')
    else:
        form = ProfileForm(instance=customer)
    return render(request, 'core/profile.html', {'form': form})

def logout_view(request):
    logout(request)
    messages.success(request, "You have been logged out.")
    return redirect('login')

def about_view(request):
    return render(request, 'core/about.html')

def privacy_policy_view(request):
    return render(request, 'core/privacy_policy.html')

def terms_conditions_view(request):
    return render(request, 'core/terms_conditions.html')

def help_view(request):
    return render(request, 'core/help.html')