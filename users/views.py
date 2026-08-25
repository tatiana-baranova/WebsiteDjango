import hashlib
import hmac
import time
from django.shortcuts import render, redirect
from .forms import UserRegisterForm, UserUpdateForm, ProfileImageForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.conf import settings
from .models import Payment
# import json
# from django.http import JsonResponse
# from django.views.decorators.http import require_GET
# from django.contrib.auth.forms import UserCreationForm
# from django.views.decorators.csrf import csrf_exempt




def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Користувач {username} успішно зареєстрований')
            return redirect('home')
    else:
        form = UserRegisterForm()

    return render(request, 'users/registration.html', {'title': 'Сторінка реєстрації', 'form': form})

@login_required
def profile(request):
    if request.method == 'POST':
        profile_form = ProfileImageForm(request.POST, request.FILES, instance=request.user.profile)
        update_user_form = UserUpdateForm(request.POST, instance=request.user)

        if profile_form.is_valid() and update_user_form.is_valid():
            update_user_form.save()
            profile_form.save()

            messages.success(request, "Профіль успішно оновлений")
            return redirect('profile')
    else:
        profile_form = ProfileImageForm(instance=request.user.profile)
        update_user_form = UserUpdateForm(instance=request.user)


    data = {
        'profile_form': profile_form,
        'update_user_form': update_user_form
    }
    return render(request, 'users/profile.html', data)
@login_required
def create_payment(request):
    amount = 555
    currency = 'UAH'

    product_name = 'Підписка Full'
    product_count = 1
    product_price = amount

    payment = Payment.objects.create(
        user=request.user,
        plan='full',
        amount=amount,
        status='pending'
    )

    order_reference = f'{payment.pk}_{int(time.time())}'

    payment.order_reference = order_reference
    payment.save()

    order_date = int(time.time())

    signature_string = ';'.join([
        settings.WAYFORPAY_MERCHANT_ACCOUNT,
        '127.0.0.1',
        order_reference,
        str(order_date),
        str(amount),
        currency,
        product_name,
        str(product_count),
        str(product_price),
    ])

    merchant_signature = hmac.new(
        settings.WAYFORPAY_SECRET_KEY.encode('utf-8'),
        signature_string.encode('utf-8'),
        hashlib.md5
    ).hexdigest()

    context = {
        'merchant_account': settings.WAYFORPAY_MERCHANT_ACCOUNT,
        'merchant_domain_name': '127.0.0.1',

        'order_reference': order_reference,
        'order_date': order_date,

        'amount': amount,
        'currency': currency,

        'product_name': product_name,
        'product_count': product_count,
        'product_price': product_price,

        'merchant_signature': merchant_signature,
    }

    return render(
        request,
        'users/create_payment.html',
        context
    )


# @csrf_exempt
# def wayforpay_callback(request):
#     if request.method != 'POST':
#         return JsonResponse({
#             'status': 'error','message': 'Only POST requests are allowed'},
#             status=405
#         )
#     print('CONTENT TYPE:', request.content_type)
#     print('RAW BODY:', request.body)
#
#     try:
#         data = json.loads(request.body.decode('utf-8'))
#     except (json.JSONDecodeError, UnicodeDecodeError) as error:
#         print('JSON ERROR:', error)
#
#         return JsonResponse(
#             {'status': 'error', 'message': 'Invalid JSON'},
#             status=400
#         )
#
#     print('WAYFORPAY CALLBACK:')
#     print(data)
#
#     order_reference = data.get('orderReference')
#     transaction_status = data.get('transactionStatus')
#
#     if not order_reference:
#         return JsonResponse(
#             {'status': 'error', 'message': 'orderReference is missing'},
#             status=400
#         )
#
#     try:
#         payment = Payment.objects.get(
#             order_reference=order_reference
#         )
#     except Payment.DoesNotExist:
#         return JsonResponse(
#             {'status': 'error', 'message': 'Payment not found'},
#             status=404
#         )
#     if transaction_status == 'Approved':
#         payment.status = 'paid'
#         payment.save(update_fields=['status'])
#
#         user = payment.user
#         user.profile.account_type = 'full'
#         user.profile.save(update_fields=['account_type'])
#
#         print(
#             f'Payment {payment.order_reference} approved. '
#             f'User {user.username} upgraded to full.'
#         )
#
#     elif transaction_status:
#         payment.status = transaction_status.lower()
#         payment.save(update_fields=['status'])
#
#     return JsonResponse({
#         'status': 'accept'
#     })
#
#
# @require_GET
# def test_callback(request):
#     return render(request, 'users/test_callback.html')