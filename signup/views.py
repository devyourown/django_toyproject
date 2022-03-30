from django.shortcuts import render, redirect
from main.models import User
from random import randint
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from main.views import encryptPassword

# Create your views here.
def send_code(email, code):
    try:
        server_email = 'woorinae47@gmail.com'
        msg_html = "<h1>인증번호 : " + str(code) + "</h1>"
        msg = EmailMessage(subject="인증 코드 발송 메일", body=msg_html,
                           from_email=server_email,
                           bcc=[email])
        msg.content_subtype = 'html'
        msg.send()
        return True
    except Exception as e:
        print(e)
        return False

def signup(request):
    return render(request, 'signup/signup.html')

def email(request):
    try:
        user_name = request.POST['signupName']
        user_email = request.POST['signupEmail']
        user_pw = request.POST['signupPW']
        encrypted = encryptPassword(user_pw)
        new_user = User(user_id=user_email, user_name=user_name, user_pw=encrypted)
        new_user.save()
        code = randint(1000, 9999)
        if not send_code(user_email, code):
            raise Exception('email 보내기 실패')
        request.session['temp_user'] = user_email
        request.session['temp_code'] = code
        return render(request, 'signup/verifyView.html')
    except Exception as e:
        print(e)
        content = {'message' : "회원가입에 실패했습니다."}
        return render(request, 'main/error.html', content)

def verifyView(request):
    return render(request, 'signup/verifyView.html')

def verify(request):
    code = request.POST['verifyCode']
    print(request.session['temp_code'])
    print(code)
    if int(code) == int(request.session['temp_code']):
        user_email = request.session['temp_user']
        verified_user = User.objects.get(user_id=user_email)
        verified_user.user_validation = True
        verified_user.save()
        del request.session['temp_user']
        del request.session['temp_code']
        request.session['user_name'] = verified_user.user_name
        request.session['user_email'] = user_email
        return render(request, 'signup/verifyGood.html')
    else :
        return redirect('signup_verifyView')

def verified(request):
    if 'user_name' in request.session.keys():
        return render(request, 'signup/verifyGood.html')
    else :
        return redirect('signup')


