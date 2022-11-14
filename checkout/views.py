from django.shortcuts import render, redirect, reverse
from django.contrib import messages
from django.conf import settings

from .forms import OrderForm
from bag.contexts import bag_contents

import stripe


def checkout(request):
    stripe_public_key = settings.STRIPE_PUBLIC_KEY
    stripe_secret_key = settings.STRIPE_SECRET_KEY
    print(f"Stripe PK: {stripe_public_key}")
    print(f"Stripe SK: {stripe_secret_key}")
    bag = request.session.get('bag', {})
    if not bag:
        messages.error(request, "There's nothing in your bag at the moment")
        return redirect(reverse('products'))

    current_bag = bag_contents(request)
    total = current_bag['grand_total']
    stripe_total = round(total * 100)
    stripe.api_key = stripe_secret_key
    intent = stripe.PaymentIntent.create(
        amount=stripe_total,
        currency=settings.STRIPE_CURRENCY,
        
    )

    print(intent)

    order_form = OrderForm()
    template = 'checkout/checkout.html'
    context = {
        'order_form': order_form,
        'stripe_public_key': 'pk_test_51M44lAFHGuZumMTzikjo1pda0tLaVQV2hIj9XmEkLsWtNdHH6xvGy3e3KFfBaLQaPqUSw94a8HT33epJ0h2qAXDa00MYL4dXLf',
        'client_secret': 'test client secret',
    }

    return render(request, template, context)
