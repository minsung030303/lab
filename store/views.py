from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .models import Product, Wishlist
import random
from django.views.decorators.csrf import csrf_exempt
import json

def index(request):
    all_products = list(Product.objects.all())
    random.shuffle(all_products)
    products = all_products[:10]  # 무작위 상품 10개만 추출

    # ✅ 찜한 상품 ID 리스트 추가
    user_wishlist = []
    if request.user.is_authenticated:
        user_wishlist = Wishlist.objects.filter(user=request.user).values_list('product_id', flat=True)

    return render(request, 'store/index.html', {
        'products': products,
        'user_wishlist': list(user_wishlist),  # 리스트로 변환해서 템플릿에서 in 사용
    })

def product_list(request):
    products = Product.objects.all()
    user_wishlist = []
    if request.user.is_authenticated:
        user_wishlist = Wishlist.objects.filter(user=request.user).values_list('product_id', flat=True)
    return render(request, 'store/product_list.html', {'products': products, 'user_wishlist': user_wishlist})

def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    is_wished = False
    if request.user.is_authenticated:
        is_wished = Wishlist.objects.filter(user=request.user, product=product).exists()
    return render(request, 'store/product_detail.html', {'product': product, 'is_wished': is_wished})

@login_required
def add_to_wishlist(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    Wishlist.objects.get_or_create(user=request.user, product=product)
    return JsonResponse({'status': 'added'})

@login_required
def remove_from_wishlist(request, product_id):
    Wishlist.objects.filter(user=request.user, product_id=product_id).delete()
    return JsonResponse({'status': 'removed'})

@login_required
def wishlist_page(request):
    wishlist_items = Wishlist.objects.filter(user=request.user).select_related('product')
    return render(request, 'store/wishlist.html', {'wishlist_items': wishlist_items})

@login_required
@csrf_exempt
def delete_selected_wishlist(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        product_ids = data.get('product_ids', [])
        Wishlist.objects.filter(user=request.user, product_id__in=product_ids).delete()
        return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'invalid'}, status=400)