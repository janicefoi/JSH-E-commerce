from django.shortcuts import render, redirect,  get_object_or_404
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import AuthenticationForm
from .forms import CustomUserCreationForm, UserProfileUpdateForm, UserEmailUpdateForm
from .models import UserProfile, Customer, Item, Cart, CartItem, Wishlist
from django.contrib.auth.decorators import login_required
import json
from django.contrib.gis.geos import Point
from django.db.models import F, Case, When, IntegerField
from django.http import JsonResponse


def home(request):
    return render(request, 'home.html')

def about_us(request):
    return render(request, 'about_us.html')

def contact_us(request):
    return render(request, 'contact_us.html')

def dashboard(request):
    items = Item.objects.all()  
    return render(request, 'dashboard.html', {'items': items})


def registration(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()

            # Create a Customer profile for the new user
            customer = Customer(user=user, email=user.email)
            customer.save()

            login(request, user)
            print("User registered and logged in successfully.")
            return redirect('dashboard')
        else:
            print("Form is not valid. Errors:", form.errors)  
    else:
        form = CustomUserCreationForm()

    return render(request, 'registration.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('dashboard')
    else:
        form = AuthenticationForm()

    return render(request, 'login.html', {'form': form})

@login_required
def update_profile(request):
    user_profile = UserProfile.objects.get(email=request.user.email)
    customer = Customer.objects.get(user=user_profile)
    
    if request.method == 'POST':
        email_form = UserEmailUpdateForm(request.POST, instance=user_profile)
        profile_form = UserProfileUpdateForm(request.POST, instance=user_profile)

        if email_form.is_valid() and profile_form.is_valid():
            print("Forms are valid.")
            email_form.save()
            profile = profile_form.save(commit=False)

            # Check if 'selected_location' is in the POST data
            if 'selected_location' in request.POST:
                selected_location = request.POST['selected_location']
                try:
                    lat, lng = map(float, selected_location.split(','))
                except ValueError:
                    print("Invalid location data")
                else:
                    user_profile.location = Point(lng, lat, srid=4326)
                    user_profile.location = user_profile.location
                    user_profile.save()
                    user_profile.phone_number = profile_form.cleaned_data['phone_number']
                    user_profile.save()
                    print("Profile and user_profile saved.")
                    print(f"Updated email: {user_profile.email}")
                    print(f"Updated location: {user_profile.location}")
                    print(f"Updated phone_number: {profile_form.cleaned_data['phone_number']}")

                    # Update the associated Customer's location and phone number
                    customer.location = user_profile.location
                    customer.phone_number = profile_form.cleaned_data['phone_number']
                    customer.save()
                    print("Customer saved.")
                    return redirect('dashboard')
        else:
            print("Form is not valid. Errors:", email_form.errors, profile_form.errors)
    
    else:
        email_form = UserEmailUpdateForm(instance=user_profile)
        profile_form = UserProfileUpdateForm(instance=user_profile)
    
    user_profile_json = json.dumps({
        "location": {
            "latitude": user_profile.location.latitude if user_profile.location else 0.0,
            "longitude": user_profile.location.longitude if user_profile.location else 0.0,
        }
    })

    return render(request, 'update_profile.html', {
        'email_form': email_form,
        'profile_form': profile_form,
        'user_profile_json': user_profile_json,
    })



def add_to_wishlist(request, item_id):
    item = get_object_or_404(Item, pk=item_id)
    if request.user.is_authenticated:
        wishlist, created = Wishlist.objects.get_or_create(user=request.user)
        wishlist.items.add(item)
        wishlist.save()

    return redirect('dashboard')


def view_wishlist(request):
    if request.user.is_authenticated:
        wishlist, created = Wishlist.objects.get_or_create(user=request.user)
        wishlist_items = wishlist.items.all()

        return render(request, 'wishlist.html', {'wishlist_items': wishlist_items})
    return redirect('login') 

def wishlist_item_count(request):
    # Check if the user is authenticated and has a wishlist
    if request.user.is_authenticated and hasattr(request.user, 'wishlist'):
        wishlist = request.user.wishlist
        item_count = wishlist.items.count()
    else:
        item_count = 0

    print(f'Wishlist item count: {item_count}')

    return JsonResponse({'item_count': item_count})





@login_required
def add_to_cart(request, item_id, quantity):
    item = Item.objects.get(pk=item_id)
    user_profile = UserProfile.objects.get(email=request.user.email)
    customer, created = Customer.objects.get_or_create(user=user_profile)

    # Check if the customer already has an open cart
    cart = Cart.objects.filter(customer=customer).first()

    if not cart:
        # If no open cart exists, create a new one
        cart = Cart.objects.create(customer=customer)
        print(f"Created new cart: Order by {customer.user.email} on {cart.date}")

    try:
        # Check if the item is already in the cart
        cart_item = CartItem.objects.get(cart=cart, item=item)
        cart_item.quantity += int(quantity)
        cart_item.save()
        print(f"Updated cart item: {cart_item.quantity}x {item.name}")
    except CartItem.DoesNotExist:
        # If the item is not in the cart, create a new cart item
        CartItem.objects.create(cart=cart, item=item, quantity=int(quantity), customer=customer)
        print(f"Created new cart item: {quantity}x {item.name}")

    return redirect('dashboard')



def view_cart(request):
    # Get the user profile and associated customer
    user_profile = UserProfile.objects.get(email=request.user.email)
    customer, created = Customer.objects.get_or_create(user=user_profile)

    # Check if the customer already has an open cart
    cart = Cart.objects.filter(customer=customer).first()

    # Debugging print statements
    print("User:", user_profile)
    print("Customer:", customer)
    print("Cart:", cart)

    if cart:
        # Get cart items and calculate the cart total
        cart_items = CartItem.objects.filter(cart=cart)
        cart_total = sum(item.item.price * item.quantity for item in cart_items)
    else:
        # If the cart is not found, set cart_items and cart_total to empty values
        cart_items = []
        cart_total = 0

    context = {
        'cart_items': cart_items,
        'cart_total': cart_total,
    }

    return render(request, 'cart.html', context)



def checkout(request):
    return render(request, 'checkout.html')


def cart_item_count(request):
    item_count = CartItem.objects.count()
    return JsonResponse({'item_count': item_count})



def category_items_view(request, category):
    category_items = Item.objects.filter(category=category)
    context = {
        'category_items': category_items,
    }
    return render(request, 'category_items.html', context)



