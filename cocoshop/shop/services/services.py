# services/product_service.py

from shop.models import Products, Carts, CartItems, Categories, Brands, User


class ProductService:

    # @staticmethod
    # def get_discounted_products():
    #     products = Products.objects.filter(on_sale=True)
    #     return products

    @staticmethod
    def update_product_stock(product_id, new_quantity):
        product = Products.objects.filter(product_id=product_id).update(quantity=new_quantity)
        return product

    @staticmethod
    def get_all_products():
        products = Products.objects.all()
        return products

    @staticmethod
    def get_product_by_id(product_id):
        products = Products.objects.filter(id=product_id)
        return products

    @staticmethod
    def get_products_by_category(category_id):
        products = Products.objects.filter(category_id=category_id)
        return products


class CartServices:
    @staticmethod
    def get_user_cart(user_id):
        user_cart = Carts.objects.get(id=user_id)
        return user_cart


class CartListService:
    @staticmethod
    def remove_product_from_cart(user_id, product_id):
        try:
            cart_id = CartServices.get_user_cart(user_id).id
            CartItems.objects.filter(cart_id=cart_id, product_id=product_id).delete()
            return {"success": True, "message": "Product removed from cart"}
        except Carts.DoesNotExist:
            return {"success": False, "message": "Cart not found"}
        except Products.DoesNotExist:
            return {"success": False, "message": "Product not found"}
        except Exception as e:
            return {"success": False, "message": str(e)}

    @staticmethod
    def get_user_cart_list(user_id):
        cart_id = CartServices.get_user_cart(user_id).id
        cart_items = CartItems.objects.filter(cart_id=cart_id)
        return cart_items

    @staticmethod
    def update_cart_item_quantity(user_id, product_id, new_quantity):
        user_cart_list = CartListService.get_user_cart_list(user_id)
        updated_cart_item = CartItems.objects.filter(cart_id=user_cart_list.cart_id,
                                                     product_id=product_id).update(quantity=new_quantity)
        return updated_cart_item
