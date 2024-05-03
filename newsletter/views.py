import requests
from django.shortcuts import render
from django.conf import settings
from django.contrib import messages
from django.shortcuts import redirect, render
import base64
import requests
import hashlib


def check_subscription_status(email):
    email_hash = hashlib.md5(email.lower().encode('utf-8')).hexdigest()
    api_key = settings.MAILCHIMP_API_KEY
    url = f"https://{settings.MAILCHIMP_SERVER_PREFIX}.api.mailchimp.com/3.0/lists/{settings.MAILCHIMP_LIST_ID}/members/{email_hash}"
    user_pass = base64.b64encode(f"anystring:{api_key}".encode()).decode('utf-8')
    headers = {"Authorization": f"Basic {user_pass}"}

    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        data = response.json()
        return data['status'] in ['subscribed', 'pending']
    return False


def subscribe_newsletter(request):
    if not request.user.is_authenticated:
        messages.error(request, "You need to be logged in to subscribe.", extra_tags='update')
        return redirect('account:login')

    email = request.user.email
    email_hash = hashlib.md5(email.lower().encode('utf-8')).hexdigest()

    data = {
        "email_address": email,
        "status": "subscribed",
        "status_if_new": "subscribed"
    }

    api_key = settings.MAILCHIMP_API_KEY
    url = f"https://{settings.MAILCHIMP_SERVER_PREFIX}.api.mailchimp.com/3.0/lists/{settings.MAILCHIMP_LIST_ID}/members/{email_hash}"

    user_pass = base64.b64encode(f"anystring:{api_key}".encode()).decode('utf-8')
    headers = {
        "Authorization": f"Basic {user_pass}"
    }

    # Try to update existing member first
    response = requests.put(url, json=data, headers=headers)

    if response.status_code == 200 or response.status_code == 201:
        messages.success(request, "You have been subscribed to the newsletter.", extra_tags='addition')
    elif response.status_code == 404:  
        post_url = f"https://{settings.MAILCHIMP_SERVER_PREFIX}.api.mailchimp.com/3.0/lists/{settings.MAILCHIMP_LIST_ID}/members"
        post_response = requests.post(post_url, json=data, headers=headers)
        if post_response.status_code == 200 or post_response.status_code == 201:
            messages.success(request, "You have been subscribed to the newsletter.", extra_tags='addition')
        else:
            error_data = post_response.json()
            error_message = error_data.get('detail', 'Please try again later.')
            messages.error(request, f"Failed to subscribe. Error: {error_message}", extra_tags='deletion')
    else:
        error_data = response.json()
        error_message = error_data.get('detail', 'Please try again later.')
        messages.error(request, f"Failed to subscribe. Error: {error_message}", extra_tags='deletion')

    return redirect('account:edit_details')


def thankyou_newsletter(request):
    return render(request, "newsletter/thankyou.html", {"thankyou": thankyou_newsletter})


def unsubscribe_newsletter(request):
    if not request.user.is_authenticated:
        messages.error(request, "You need to be logged in to unsubscribe.", extra_tags='update')
        return redirect('account:login')

    user = request.user
    email = user.email

    import hashlib
    email_hash = hashlib.md5(email.lower().encode('utf-8')).hexdigest()

    api_key = settings.MAILCHIMP_API_KEY
    list_id = settings.MAILCHIMP_LIST_ID
    data = {
        "status": "unsubscribed"
    }

    url = f"https://{settings.MAILCHIMP_SERVER_PREFIX}.api.mailchimp.com/3.0/lists/{list_id}/members/{email_hash}"
    
    import base64
    user_pass = base64.b64encode(f"anystring:{api_key}".encode()).decode('utf-8')
    headers = {
        "Authorization": f"Basic {user_pass}"
    }

    response = requests.patch(url, json=data, headers=headers)

    if response.status_code == 200:
        messages.success(request, "You have been unsubscribed from the newsletter.", extra_tags='deletion')
    else:
        error_data = response.json()
        error_message = error_data.get('detail', 'Please try again later.')
        messages.error(request, f"Failed to unsubscribe. Error: {error_message}", extra_tags='deletion')

    return redirect('account:edit_details')
