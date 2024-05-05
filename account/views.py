from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.sites.shortcuts import get_current_site
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from orders.views import user_orders
from store.models import Product

from .forms import RegistrationForm, UserEditForm, UserAddressForm
from orders.views import user_orders
from .models import Customer, Address
from .tokens import account_activation_token
from newsletter.views import check_subscription_status


@login_required
def wishlist(request):
    products = Product.objects.filter(users_wishlist=request.user)
    return render(request, "account/user/user_wish_list.html", {"wishlist": products})


@login_required
def add_to_wishlist(request, id):
    product = get_object_or_404(Product, id=id)
    if not product.users_wishlist.filter(id=request.user.id).exists():
        product.users_wishlist.add(request.user)
        messages.success(request, f"Added {product.title} to your ", extra_tags='wishlist addition')
    else:
        messages.info(request, f"{product.title} is already on your ", extra_tags='wishlist update')
    return HttpResponseRedirect(request.META["HTTP_REFERER"])


@login_required
def remove_from_wishlist(request, id):
    product = get_object_or_404(Product, id=id)
    if product.users_wishlist.filter(id=request.user.id).exists():
        product.users_wishlist.remove(request.user)
        messages.info(request, f"{product.title} has been removed.", extra_tags='deletion')
    return HttpResponseRedirect(request.META["HTTP_REFERER"])


@login_required
def dashboard(request):
    orders = user_orders(request)
    return render(request,
                  'account/user/dashboard.html', {'orders': orders})


@login_required
def custom_logout(request):
    logout(request)
    next_page = request.GET.get('next', '/')
    return render(request, 'account/registration/logout.html')


@login_required
def edit_details(request):
    # Check newsletter subscription status
    is_subscribed = check_subscription_status(request.user.email)

    if request.method == 'POST':
        user_form = UserEditForm(request.POST, request.FILES, instance=request.user)

        if user_form.is_valid():
            user = user_form.save(commit=False)
            clear_image = request.POST.get('clear_image', False)
            if clear_image:
                user.profile_image.delete()  # Delete the existing profile image
                user.profile_image = None  # Set profile image to None
            user.save()
            messages.success(request, 'Details successfully updated!', extra_tags='addition')
            return redirect('account:edit_details')
        else:
            for field, errors in user_form.errors.items():
                    for error in errors:
                        messages.error(request, f'Error in {field}: {error}', extra_tags='updated')
    else:
        user_form = UserEditForm(instance=request.user)

    return render(request, 'account/user/edit_details.html', {
        'user_form': user_form,
        'is_subscribed': is_subscribed
    })


@login_required
def delete_user(request):
    user = Customer.objects.get(user_name=request.user)
    user.is_active = False
    user.save()
    logout(request)
    return redirect('account:delete_confirmation')


def account_register(request):

    if request.user.is_authenticated:
        return redirect('account:dashboard')

    if request.method == 'POST':
        registerForm = RegistrationForm(request.POST)
        if registerForm.is_valid():
            user = registerForm.save(commit=False)
            user.email = registerForm.cleaned_data['email']
            user.set_password(registerForm.cleaned_data['password'])
            user.is_active = False
            user.save()
            current_site = get_current_site(request)
            subject = 'Activate your Account'
            message = render_to_string('account/registration/account_activation_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            user.email_user(subject=subject, message=message)
            return HttpResponse('registered succesfully and activation sent')
    else:
        registerForm = RegistrationForm()
    return render(request, 'account/registration/register.html', {'form': registerForm})


def account_activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = Customer.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError):
        user = None
    except Customer.DoesNotExist:
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        return redirect('account:dashboard')
    else:
        return render(request, 'account/registration/activation_invalid.html')
    

# Addresses
@login_required
def view_address(request):
    addresses = Address.objects.filter(customer=request.user)
    return render(request, "account/user/addresses.html", {"addresses": addresses})


@login_required
def add_address(request):
    if request.method == "POST":
        address_form = UserAddressForm(data=request.POST)
        if address_form.is_valid():
            address_form = address_form.save(commit=False)
            address_form.customer = request.user
            address_form.save()
            messages.success(request, 'Address successfully added!', extra_tags='addition')
            return HttpResponseRedirect(reverse("account:addresses"))
        else:
            for field, errors in address_form.errors.items():
                    for error in errors:
                        messages.error(request, f'Error in {field}: {error}', extra_tags='updated')
    else:
        address_form = UserAddressForm()
    return render(request, "account/user/edit_addresses.html", {"form": address_form})


@login_required
def edit_address(request, id):
    if request.method == "POST":
        address = Address.objects.get(pk=id, customer=request.user)
        address_form = UserAddressForm(instance=address, data=request.POST)
        if address_form.is_valid():
            address_form.save()
            messages.success(request, 'Address successfully updated!', extra_tags='addition')
            return HttpResponseRedirect(reverse("account:addresses"))
        else:
            for field, errors in address_form.errors.items():
                    for error in errors:
                        messages.error(request, f'Error in {field}: {error}', extra_tags='updated')
    else:
        address = Address.objects.get(pk=id, customer=request.user)
        address_form = UserAddressForm(instance=address)
    return render(request, "account/user/edit_addresses.html", {"form": address_form})


@login_required
def delete_address(request, id):
    try:
        address = Address.objects.get(pk=id, customer=request.user)
        address.delete()
        messages.success(request, 'Address successfully deleted!', extra_tags='deletion')
    except Address.DoesNotExist:
        messages.error(request, 'Address does not exist or you do not have permission to delete it.', extra_tags='updated')
    return redirect("account:addresses")


@login_required
def set_default(request, id):
    try:
        address_to_set_default = Address.objects.get(pk=id, customer=request.user)
        Address.objects.filter(customer=request.user, default=True).update(default=False)
        address_to_set_default.default = True
        address_to_set_default.save()
        messages.success(request, 'Default address successfully updated!', extra_tags='addition')
    except Address.DoesNotExist:
        messages.error(request, 'Address does not exist or you do not have permission to set it as default.', extra_tags='updated')
    return redirect("account:addresses")