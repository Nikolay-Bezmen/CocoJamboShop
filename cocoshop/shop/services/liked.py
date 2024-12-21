from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from shop.models import Products, Favourite
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_to_favourites(request, prid):
    """Add a product to the user's favourites."""
    product = get_object_or_404(Products, id=prid)
    favourite, created = Favourite.objects.get_or_create(user=request.user, product=product)

    return JsonResponse({
        'status': 'success',
        'message': f"{product.name} {'added to' if created else 'already in'} your favourites.",
        'favourite_item': {
            'product_id': favourite.product.id,
            'product_name': favourite.product.name
        }
    })

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def remove_from_favourites(request, prid):
    """Remove a product from the user's favourites."""
    product = get_object_or_404(Products, id=prid)
    favourite = Favourite.objects.filter(user=request.user, product=product).first()

    if favourite:
        favourite.delete()
        message = f"{product.name} removed from your favourites."
    else:
        message = f"{product.name} is not in your favourites."

    return JsonResponse({
        'status': 'success',
        'message': message
    })

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def check_favourites(request, prid):
    """Check if a specific product is in the user's favourites."""
    try:
        product = Products.objects.get(id=prid)
        is_favourite = Favourite.objects.filter(user=request.user, product=product).exists()
        
        return JsonResponse({
            'status': 'success',
            'isFavourite': is_favourite,
            'message': f"Product {'is' if is_favourite else 'is not'} in favourites."
        })
    except Products.DoesNotExist:
        return JsonResponse({
            'status': 'error',
            'isFavourite': False,
            'message': f"Product with id {prid} not found."
        })