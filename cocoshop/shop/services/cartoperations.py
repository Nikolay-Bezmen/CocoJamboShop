from django.contrib.auth.decorators import login_required
from django.contrib import messages
from shop.models import Carts, CartItems
from django.http import JsonResponse
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt


def get_or_create_cart(user):
    """Retrieve the current user's cart or create a new one."""
    cart, created = Carts.objects.get_or_create(user=user)
    return cart


@login_required
@csrf_exempt
def add_to_cart(request, prid):
    """Add a product to the cart or update its quantity if it already exists."""
    cart = get_or_create_cart(request.user)
    cart_item, created = CartItems.objects.get_or_create(cart=cart, product_id=prid, defaults={'quantity': 1})

    if not created:
        cart_item.quantity += 1
        cart_item.save()

    messages.success(request, f"{cart_item.product.name} added to the cart.")
    response_data = {
        'status': 'success',
        'message': f"{cart_item.product.name} added to the cart.",
        'cart_item': {
            'product_id': cart_item.product.id,
            'quantity': cart_item.quantity
        }
    }

    return JsonResponse(response_data)

@login_required
@csrf_exempt
def check_cart(request, prid):
    """Check if a specific product is in the user's cart."""
    cart = get_or_create_cart(request.user)
    try:
        cart_item = CartItems.objects.get(cart=cart, product_id=prid)
        response_data = {
            'status': 'success',
            'message': f"{cart_item.product.name} is in the cart.",
            'cart_item': {
                'product_id': cart_item.product.id,
                'quantity': cart_item.quantity
            }
        }
    except CartItems.DoesNotExist:
        response_data = {
            'status': 'success',
            'message': 'Product is not in the cart.',
            'cart_item': None
        }

    return JsonResponse(response_data)

@login_required
@csrf_exempt
def delete_from_cart(request, prid):
    """Decrease the quantity of a specific product in the cart by 1."""
    cart = get_or_create_cart(request.user)
    try:
        cart_item = CartItems.objects.get(cart=cart, product_id=prid)

        # Decrease the quantity by 1
        if cart_item.quantity > 1:
            cart_item.quantity -= 1
            cart_item.save()
            response_data = {
                'status': 'success',
                'message': f"One quantity of {cart_item.product.name} removed from the cart.",
                'cart_item': {
                    'product_id': cart_item.product.id,
                    'quantity': cart_item.quantity
                }
            }
        else:
            # If the quantity is 1, remove the cart item
            cart_item.delete()
            response_data = {
                'status': 'success',
                'message': f"{cart_item.product.name} removed from the cart completely.",
            }

        messages.success(request, response_data['message'])
    except CartItems.DoesNotExist:
        response_data = {
            'status': 'error',
            'message': 'Product not found in the cart.',
        }

    return JsonResponse(response_data)


@login_required
@csrf_exempt
def delete_all_from_cart(request, prid):
    """Remove all quantities of a specific product from the cart."""
    cart = get_or_create_cart(request.user)
    try:
        cart_item = CartItems.objects.get(cart=cart, product_id=prid)
        cart_item.delete()
        messages.success(request, f"All quantities of {cart_item.product.name} removed from the cart.")
        response_data = {
            'status': 'success',
            'message': f"All quantities of {cart_item.product.name} removed from the cart.",
        }
    except CartItems.DoesNotExist:
        response_data = {
            'status': 'error',
            'message': 'Product not found in the cart.',
        }

    return JsonResponse(response_data)



@login_required
@csrf_exempt
def clear_cart(request):
    """Clear all items from the cart."""
    cart = get_or_create_cart(request.user)
    cart.items.all().delete()
    messages.success(request, "All items removed from the cart.")
    response_data = {
        'status': 'success',
        'message': "All items removed from the cart.",
    }

    return JsonResponse(response_data)

