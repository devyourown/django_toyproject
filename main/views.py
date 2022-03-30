from django.shortcuts import render, redirect
import hashlib
from .models import User
from upload.models import Document
import os
from django.http import HttpResponse

# Create your views here.
def encryptPassword(password):
    encoded = password.encode()
    return hashlib.sha256(encoded).hexdigest()

def check_loggedin(request):
    if 'user_name' in request.session.keys():
        return True
    else :
        return False

def login(request):
    if request.method == 'POST':
        try:
            login_email = request.POST['loginEmail']
            login_pw = request.POST['loginPW']
            login_user = User.objects.get(user_id=login_email)
            encrypted_pw = encryptPassword(login_pw)
            if login_user.user_pw == encrypted_pw:
                request.session['user_name'] = login_user.user_name
                request.session['user_email'] = login_user.user_id
                return redirect('main_index')
            else :
                raise Exception;
        except Exception as e:
            print(e)
            error_message = "아이디 또는 비밀번호가 일치하지 않습니다."
            content = {'message':error_message}
            return render(request, 'main/error.html', content)
    else :
        return render(request, 'main/login.html')

def error(request):
    return render(request, 'main/error.html')

def index(request):
    if check_loggedin(request):
        user_id = request.session['user_email']
        user = User.objects.get(user_id=user_id)
        files = Document.objects.filter(user_id=user)
        content = {'files':files}
        return render(request, 'main/index.html', content)
    else :
        return redirect('main_login')

def download(request):
    file_path = request.POST['filePath']
    print(file_path)
    if os.path.exists(file_path):
        binary_file = open(file_path, 'rb')
        response = HttpResponse(binary_file.read(), content_type="application/liquid; charset=utf-8")
        response['Content-Disposition'] = 'attachment; filename=' + os.path.basename(file_path)
        return response
    else:
        message = '파일이 존재하지 않습니다.'
        return render(request, 'main/error.html', {'message':message})

def logout(request):
    del request.session['user_name']
    del request.session['user_email']
    return redirect('main_login')

