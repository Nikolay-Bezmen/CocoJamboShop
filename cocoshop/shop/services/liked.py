from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from shop.models import Products, Favourite


@login_required
@csrf_exempt
def add_to_favourites(request, prid):
    """Add a product to the user's favourites."""
    product = get_object_or_404(Products, id=prid)

    # Check if the product is already in the user's favourites
    favourite, created = Favourite.objects.get_or_create(user=request.user, product=product)

    if not created:
        return JsonResponse({
            'status': 'error',
            'message': f"{product.name} is already in your favourites."
        }, status=400)

    messages.success(request, f"{product.name} added to your favourites.")
    return JsonResponse({
        'status': 'success',
        'message': f"{product.name} added to your favourites.",
        'favourite_item': {
            'product_id': favourite.product.id,
            'product_name': favourite.product.name
        }
    })


@login_required
@csrf_exempt
def remove_from_favourites(request, prid):
    """Remove a product from the user's favourites."""
    product = get_object_or_404(Products, id=prid)
    favourite = Favourite.objects.filter(user=request.user, product=product).first()

    if not favourite:
        return JsonResponse({
            'status': 'error',
            'message': f"{product.name} is not in your favourites."
        }, status=404)

    favourite.delete()
    messages.success(request, f"{product.name} removed from your favourites.")
    return JsonResponse({
        'status': 'success',
        'message': f"{product.name} removed from your favourites."
    })


@login_required
@csrf_exempt
def check_favourites(request, prid):
    """Check if a specific product is in the user's cart."""
    product = get_object_or_404(Products, id=prid)
    favourite = Favourite.objects.filter(user=request.user, product=product).first()

    if not favourite:
        return JsonResponse({
            'status': 'error',
            'message': f"{product.name} is not in your favourites."
        }, status=404)
    else:
        response_data = {
            'status': 'success',
            'message': 'Product is not in the cart.',
        }

    return JsonResponse(response_data)
