import json
import base64
from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.core.files.base import ContentFile
from django.views.decorators.csrf import csrf_exempt

from .models import Profile, Product
from .utils import get_bot_response, save_chat

def index_view(request):
    return render(request, 'index.html')

def home_view(request):
    return render(request, 'home.html')

def catalog_view(request):
    return render(request, 'catalog.html')

def orders_view(request):
    return render(request, 'orders.html')

def about_view(request):
    return render(request, 'about.html')

def profile_view(request):
    return render(request, 'profile.html')

def selection_view(request):
    return render(request, 'selection_guide.html')

def delivery_view(request):
    return render(request, 'delivery_terms.html')

def contacts_view(request):
    return render(request, 'contacts.html')


@csrf_exempt
def register_user(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            username = data.get('username')
            password = data.get('password')
            email = data.get('email', '')
            phone = data.get('phone', '')

            if not username or not password:
                return JsonResponse({'status': 'error', 'message': 'Логин мен құпия сөз керек!'}, status=400)

            if User.objects.filter(username=username).exists():
                return JsonResponse({'status': 'error', 'message': 'Бұл есім бос емес!'}, status=400)

            user = User.objects.create_user(username=username, email=email, password=password)
            Profile.objects.create(user=user, phone=phone)
            
            return JsonResponse({'status': 'success', 'message': 'Тіркелу сәтті!'}, status=201)
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=500)
    return JsonResponse({'status': 'error', 'message': 'Тек POST қабылданады'}, status=405)

@csrf_exempt
def login_user(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            username = data.get('username')
            password = data.get('password')
            
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                profile, _ = Profile.objects.get_or_create(user=user)
                
                return JsonResponse({
                    'status': 'success',
                    'user': {
                        'username': user.username,
                        'email': user.email,
                        'phone': profile.phone,
                        'image': profile.image.url if profile.image else '/media/profile_pics/default.jpeg'
                    }
                })
            return JsonResponse({'status': 'error', 'message': 'Логин немесе құпия сөз қате!'}, status=401)
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)
    return JsonResponse({'status': 'error', 'message': 'Метод рұқсат етілмеген'}, status=405)

# --- ПРОФИЛЬМЕН ЖҰМЫС ---

@csrf_exempt
def update_profile(request):
    if request.method == 'POST':
        try:
            if not request.user.is_authenticated:
                return JsonResponse({'status': 'error', 'message': 'Авторизация қажет'}, status=401)

            data = json.loads(request.body)
            user = request.user
            user.username = data.get('username', user.username)
            user.email = data.get('email', user.email)
            user.save()

            profile, _ = Profile.objects.get_or_create(user=user)
            if 'phone' in data:
                profile.phone = data.get('phone')

            image_data = data.get('image')
            if image_data and image_data.startswith('data:image'):
                format, imgstr = image_data.split(';base64,')
                ext = format.split('/')[-1]
                filename = f"user_{user.id}_avatar.{ext}"
                profile.image.save(filename, ContentFile(base64.b64decode(imgstr)), save=False)

            profile.save()
            return JsonResponse({'status': 'success', 'user': {'username': user.username, 'phone': profile.phone}})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)
    return JsonResponse({'status': 'error', 'message': 'POST керек'}, status=405)

# --- API ДЕРЕКТЕРІ ---

def get_products(request):
    products = Product.objects.all()
    data = [{
        'id': p.id,
        'name': p.name,
        'price': float(p.price),
        'image': p.image.url if p.image else '/media/products/default_flower.jpg',
        'category': p.category
    } for p in products]
    return JsonResponse({'status': 'success', 'products': data})

@csrf_exempt
def chat_api(request):
    if request.method == "POST":
        try:
            # Егер JavaScript-тен FormData арқылы келсе:
            user_message = request.POST.get('message', '').strip()
            # Егер JSON арқылы келсе, оны да тексереміз:
            if not user_message and request.body:
                data = json.loads(request.body)
                user_message = data.get('message', '').strip()

            if not user_message:
                return JsonResponse({'status': 'error', 'message': 'Хабарлама бос'}, status=400)

            bot_answer = get_bot_response(user_message)
            save_chat(user_message, bot_answer)
            
            return JsonResponse({'status': 'success', 'reply': bot_answer})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=500)
    return JsonResponse({'status': 'error', 'message': 'Тек POST қабылданады'}, status=405)


def catalog_view(request):
    products = Product.objects.all() # Базадан барлық тауарды алу
    return render(request, 'catalog.html', {'products': products})