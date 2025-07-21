import requests
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import JsonResponse

def signup_view(request):
    if request.method == 'POST':
        username = request.POST['username']  # 이메일
        password = request.POST['password']
        nickname = request.POST['nickname']  # 닉네임 받기
        email = request.POST['username']

        if not User.objects.filter(username=username).exists():
            user = User.objects.create_user(username=username, password=password, email=email)
            user.first_name = nickname  # 닉네임을 first_name에 저장
            user.save()
            return redirect('login')
        else:
            return render(request, 'accounts/signup.html', {'error': '이미 존재하는 아이디입니다.'})
    return render(request, 'accounts/signup.html')

def check_email_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        exists = User.objects.filter(username=email).exists()
        return JsonResponse({'exists': exists})

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('index')
        else:
            return render(request, 'accounts/login.html', {'error': '아이디 또는 비밀번호가 틀렸습니다.'})
    return render(request, 'accounts/login.html')

def logout_view(request):
    logout(request)
    return redirect('index')

# 로그인 버튼 눌렀을 때 호출되는 뷰
def kakao_login(request):
    client_id = '06e4266f5d2a8de1abf8488c33c8b88b'
    redirect_uri = 'http://43.200.176.71:8000/accounts/kakao/callback'
    kakao_auth_url = (
        f"https://kauth.kakao.com/oauth/authorize"
        f"?client_id={client_id}&redirect_uri={redirect_uri}"
        f"&response_type=code"
        f"&prompt=login"
    )
    return redirect(kakao_auth_url)

def kakao_callback(request):
    code = request.GET.get("code")

    client_id = '06e4266f5d2a8de1abf8488c33c8b88b'
    redirect_uri = 'http://43.200.176.71:8000/accounts/kakao/callback'

    # 토큰 요청
    token_url = 'https://kauth.kakao.com/oauth/token'
    data = {
        'grant_type': 'authorization_code',
        'client_id': client_id,
        'redirect_uri': redirect_uri,
        'code': code,
    }
    token_res = requests.post(token_url, data=data).json()
    access_token = token_res.get('access_token')

    # 사용자 정보 요청
    profile_url = 'https://kapi.kakao.com/v2/user/me'
    headers = {'Authorization': f'Bearer {access_token}'}
    profile_res = requests.get(profile_url, headers=headers).json()

    kakao_id = profile_res.get('id')
    account_info = profile_res.get('kakao_account', {})
    profile_info = account_info.get('profile', {})

    email = account_info.get('email')
    nickname = profile_info.get('nickname')
    name = account_info.get('name')

    # 회원이 이미 존재하는지 확인 (없으면 생성)
    username = f'kakao_{kakao_id}'
    user, created = User.objects.get_or_create(username=username)
    if created:
        user.first_name = nickname
        user.email = email
        user.set_unusable_password()
        user.save()

    # 로그인 처리 후 리다이렉트
    login(request, user)
    return redirect('index')  # 또는 원하는 URL name

def logout_view(request):
    logout(request)  # Django 세션 로그아웃

    # Kakao 로그아웃 URL로 리디렉션
    kakao_logout_url = (
        "https://kauth.kakao.com/oauth/logout"
        "?client_id=06e4266f5d2a8de1abf8488c33c8b88b"
        "&logout_redirect_uri=http://43.200.176.71:8000/accounts/kakao/logout_done/"
    )
    return redirect(kakao_logout_url)

def kakao_logout_done(request):
    # 로그아웃 완료 후 index 페이지로 이동
    return redirect('index')

def naver_login(request):
    client_id = 'fJJtm4jpU7cj30PP4q1m'
    redirect_uri = 'http://43.200.176.71:8000/accounts/naver/callback/'
    state = 'RANDOM_STATE_STRING'  # CSRF 방지용
    naver_auth_url = (
        f"https://nid.naver.com/oauth2.0/authorize"
        f"?response_type=code&client_id={client_id}"
        f"&redirect_uri={redirect_uri}&state={state}"
    )
    return redirect(naver_auth_url)

def naver_callback(request):
    code = request.GET.get("code")
    state = request.GET.get("state")
    client_id = 'fJJtm4jpU7cj30PP4q1m'
    client_secret = 'iufspvtwad'
    redirect_uri = 'http://43.200.176.71:8000/accounts/naver/callback/'

    token_url = 'https://nid.naver.com/oauth2.0/token'
    data = {
        'grant_type': 'authorization_code',
        'client_id': client_id,
        'client_secret': client_secret,
        'code': code,
        'state': state,
    }

    token_res = requests.post(token_url, data=data).json()
    access_token = token_res.get('access_token')

    profile_url = 'https://openapi.naver.com/v1/nid/me'
    headers = {'Authorization': f'Bearer {access_token}'}
    profile_res = requests.get(profile_url, headers=headers).json()

    # 사용자 정보
    naver_id = profile_res['response']['id']
    email = profile_res['response'].get('email')
    nickname = profile_res['response'].get('nickname')

    # 유저 생성 or 가져오기
    username = f'naver_{naver_id}'
    user, created = User.objects.get_or_create(username=username)
    if created:
        user.first_name = nickname or ''
        user.email = email or ''
        user.set_unusable_password()
        user.save()

    login(request, user)
    return redirect('index')
