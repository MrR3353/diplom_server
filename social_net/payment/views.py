from decimal import Decimal
import stripe
from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import render, redirect, reverse, get_object_or_404

from .models import Order
from repository.models import Repository

# создать экземпляр Stripe
stripe.api_key = settings.STRIPE_SECRET_KEY
stripe.api_version = settings.STRIPE_API_VERSION


def payment_process(request, repository_id):
    if request.method == 'POST':
        repository = get_object_or_404(Repository, pk=repository_id)
        order = Order.objects.create(user=request.user, repository=repository, price=repository.price)
        success_url = request.build_absolute_uri(reverse('payment:completed'))
        cancel_url = request.build_absolute_uri(reverse('payment:canceled'))
        # данные сеанса оформления платежа Stripe
        session_data = {
            'mode': 'payment',
            'client_reference_id': order.id,
            'success_url': success_url,
            'cancel_url': cancel_url,
            'line_items': [
                {
                    'price_data': {
                        'unit_amount': int(repository.price * Decimal('100')),
                        'currency': 'usd',
                        'product_data': {'name': repository.name},
                    },
                    'quantity': 1,
                }
            ]
        }
        # создать сеанс оформления платежа Stripe
        session = stripe.checkout.Session.create(**session_data)
        # перенаправить к платежной форме Stripe
        return redirect(session.url, code=303)
    else:
        return JsonResponse({'message': 'Method not allowed'}, status=405)


def payment_completed(request):
    return render(request, 'payment/completed.html')


def payment_canceled(request):
    return render(request, 'payment/canceled.html')

