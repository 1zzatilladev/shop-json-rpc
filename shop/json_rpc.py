from modernrpc.server import RpcServer
from .models import Product, Category
from .serializers import ProductSerializer, CategorySerializer

rpc_server = RpcServer()


@rpc_server.register_procedure
def get_products() -> list:
    products = Product.objects.all()
    return ProductSerializer(products, many=True).data


@rpc_server.register_procedure
def get_categories() -> list:
    categories = Category.objects.all()
    return CategorySerializer(categories, many=True).data


@rpc_server.register_procedure
def create_product(name: str, price: float, category_id: int) -> dict:
    product = Product.objects.create(
        name=name,
        price=price,
        category_id=category_id
    )
    return {
        "id": product.id,
        "name": product.name,
        "price": product.price
    }


@rpc_server.register_procedure
def test_uchun(ism: str) -> str:
    return ism.upper()