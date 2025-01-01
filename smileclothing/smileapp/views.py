from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from .models import Product, Category,Order
from django.shortcuts import render, redirect
from .forms import ProductForm
from .models import Product
from django.contrib.auth.decorators import login_required
from .models import  Cart, CartItem,Order
from django.db import transaction
from django.views.generic import ListView
from .forms import ProfileUpdateForm
from .models import Profile,OrderItem
from .forms import ContactForm,CheckoutForm
from django.core.mail import send_mail
import razorpay
from django.conf import settings
from django.conf import settings
from django.http import JsonResponse




def register_view(request):
    if request.method == "POST":
        fullname = request.POST.get("fname")
        username = request.POST.get("username")
        password = request.POST.get("password")
        email = request.POST.get("email")
        if fullname and username and password and email:
            if User.objects.filter(email=email).exists():
                return render(request, 'registration.html', {'error': 'Email already exists.'})
            if User.objects.filter(username=username).exists():
                return render(request, 'registration.html', {'error': 'Username already exists.'})
            user = User.objects.create_user(username=username, email=email, password=password, first_name=fullname)
            user.save()
            messages.success(request, "Registration successful!")
            return redirect("login")

        return render(request, 'registration.html', {'error': 'Please fill in all fields.'})
    return render(request, 'registration.html')


def login_view(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home') 
        else:
            return render(request, 'login.html', {'error': 'Invalid username or password'})
    return render(request, 'login.html')

def logout_view(request):
    logout(request)
    return redirect('login')

def home(request):
    featured_products = Product.objects.filter(is_featured=True)[:4]
    latest_products = Product.objects.order_by('-created')[:4]
    categories = Category.objects.all()
    cart_item_count = 4

    context = {
        'featured_products': featured_products,
        'latest_products': latest_products,
        'categories': categories,
        'cart_item_count': cart_item_count,
    }
    return render(request, 'home.html', context)
def product_list(request, category_slug=None):
    category = None
    categories = Category.objects.all()  # Fetch all categories
    products = Product.objects.filter(stock__gt=0)  # Fetch all products in stock

    # If category_slug is passed, filter products by category
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)

    return render(request, 'product_list.html', {
        'category': category,
        'categories': categories,
        'products': products
    })



def product_detail(request, id, slug):
    product = get_object_or_404(Product, id=id, slug=slug)
    return render(request, 'product_detail.html', {'product': product})



@login_required
def add_to_cart(request, id, slug):
    product = get_object_or_404(Product, id=id, slug=slug)
    
    # Get or create the cart for the current user
    cart, created = Cart.objects.get_or_create(user=request.user)
    
    # Get or create the CartItem for the product in the user's cart
    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
    
    cart_item.quantity += 1
    cart_item.save()

    return redirect('cart_view')



@login_required
def cart_view(request):
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_items = CartItem.objects.filter(cart=cart)

    for item in cart_items:
        item.total_price = item.product.price * item.quantity  # Calculate total price for the item

    total_price = sum(item.total_price for item in cart_items)  # Calculate overall total price

    return render(request, 'cart.html', {'cart_items': cart_items, 'total_price': total_price})

@login_required
def remove_from_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart = Cart.objects.get(user=request.user)
    cart_item = get_object_or_404(CartItem, cart=cart, product=product)  # Use get_object_or_404 here
    cart_item.delete()

    return redirect('cart_view')



@login_required
def profile_view(request):
    # Get the user's profile or create it if it doesn't exist
    profile, created = Profile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('profile')  # Redirect to the same profile page after saving
    else:
        form = ProfileUpdateForm(instance=profile)

    return render(request, 'profile.html', {'form': form, 'profile': profile})
@login_required
def order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    return render(request, 'order_detail.html', {'order': order})


@login_required
def checkout(request):
    cart = Cart.objects.get(user=request.user)
    cart_items = CartItem.objects.filter(cart=cart)
    total_price = sum(item.product.price * item.quantity for item in cart_items)
    
    if request.method == 'POST':
        # Handle the order processing (e.g., save order, clear cart, etc.)
        cart_items.delete()  # Clear the cart after purchase
        return render(request, 'order_confirmation.html')
    
    return render(request, 'checkout.html', {'cart_items': cart_items, 'total_price': total_price})


def view_orders(request):
    if request.user.is_authenticated:
        orders = Order.objects.filter(user=request.user)  # Fetch orders for the logged-in user
    else:
        orders = []  # If the user is not logged in, return an empty list

    return render(request, 'orders.html', {'orders': orders})




def create_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)  # Make sure to include request.FILES
        if form.is_valid():
            form.save()
            return redirect('product_list')  # Redirect to product list after saving
    else:
        form = ProductForm()
    return render(request, 'shop/create_product.html', {'form': form})



class ProductListView(ListView):
    model = Product
    template_name = 'product_list.html'
    context_object_name = 'products'

    def get_queryset(self):
        slug = self.kwargs.get('slug')
        if slug:
            # Filter products by category slug
            return Product.objects.filter(category__slug=slug)
        return Product.objects.all()


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Get the category based on the slug from the URL
        slug = self.kwargs.get('slug')
        category = None
        if slug:
            category = Category.objects.get(slug=slug)
            context['category_slug'] = slug
        
        context['category'] = category
        context['categories'] = Category.objects.all()  # Add all categories to context
        return context




def contact_view(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            # Process the form data
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            message = form.cleaned_data['message']
            
            # Send an email (you can configure this in your settings.py)
            send_mail(
                f'Contact Form Submission from {name}',
                message,
                email,  # From email
                ['your_email@example.com'],  # To email
                fail_silently=False,
            )
            
            # Display success message
            messages.success(request, 'Your message has been sent successfully!')
            return redirect('contact_view')  # Redirect to the same page or a different one

    else:
        form = ContactForm()  # Create a new instance of the form

    return render(request, 'contactus.html', {'form': form})

@login_required
def buy_now(request, id, slug):
    product = get_object_or_404(Product, id=id, slug=slug)
    
    # Get or create the cart for the current user
    cart, created = Cart.objects.get_or_create(user=request.user)
    
    # Get or create the CartItem for the product in the user's cart
    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
    
    # Set the quantity to 1 (or any default value) for the "Buy Now" feature
    cart_item.quantity = 1
    cart_item.save()
    
    # Redirect to the checkout page after adding the item to the cart
    return redirect('checkout')

@login_required
def checkout(request):
    # Function to calculate total from user's cart
    def calculate_cart_total(user):
        cart = request.session.get('cart', {})
        total = sum(float(item['price']) * item['quantity'] for item in cart.values())
        return total

    if request.method == 'POST':
        form = CheckoutForm(request.POST)
        if form.is_valid():
            # Save the order details
            order = form.save(commit=False)
            order.user = request.user  # associate the order with the logged-in user
            order.total_amount = calculate_cart_total(request.user)  # Calculate total
            order.save()

            if order.payment_method == 'Online':
                # Redirect to payment gateway (e.g., Razorpay)
                return redirect('payment_gateway', order_id=order.id)
            else:
                # Confirm order for Cash on Delivery
                return redirect('order_confirmation', order_id=order.id)
    else:
        form = CheckoutForm()

    return render(request, 'checkout.html', {'form': form})

@login_required
def view_orders(request):
    if request.user.is_authenticated:
        orders = Order.objects.filter(user=request.user)  # Fetch orders for the logged-in user
    else:
        orders = []  # If the user is not logged in, return an empty list

    return render(request, 'orders.html', {'orders': orders})



@login_required
def order_confirmation(request, order_id):
    # Confirm the order, mark status as confirmed
    order = Order.objects.get(id=order_id, user=request.user)
    order.status = 'Confirmed'
    order.save()

    return render(request, 'order_confirmation.html', {'order': order})


def calculate_cart_total(user):
    # Assuming you have a Cart model that tracks the user's items
    cart_items = CartItem.objects.filter(cart__user=user)
    total = sum(item.product.price * item.quantity for item in cart_items)
    return total



@login_required
def payment_gateway(request, order_id):
    order = Order.objects.get(id=order_id, user=request.user)

    client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_SECRET_KEY))

    payment = client.order.create({
        "amount": order.total_amount * 100,  # Razorpay works with paise
        "currency": "INR",
        "payment_capture": "1"
    })

    # Redirect to Razorpay Payment Page
    return render(request, 'payment_page.html', {'order': order, 'payment': payment})


@login_required
def orders_list(request):
    orders = Order.objects.filter(user=request.user)
    return render(request, 'orders_list.html', {'orders': orders})

# views.py

def orders_view(request):
    # Fetch the orders for the logged-in user
    orders = Order.objects.filter(user=request.user)

    # Pass the orders to the template
    return render(request, 'orders.html', {'orders': orders})

