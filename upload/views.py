from django.shortcuts import render, redirect
from main.models import User
from datetime import datetime
from .models import Document

# Create your views here.
def fileView(request):
    if 'user_name' in request.session.keys():
        return render(request, 'upload/uploadFile.html')
    else :
        return redirect('main_index')

def file(request):
    try:
        file = request.FILES['fileInput']

        origin_file_name = file.name
        user_id = request.session['user_email']
        user = User.objects.get(user_id=user_id)
        now_HMS = datetime.today().strftime('%H%M%S')
        file_upload_name = now_HMS+"_"+user.user_name+"_"+origin_file_name
        file.name = file_upload_name
        document = Document(file_path=file, file_name=file_upload_name, user_id=user)
        document.save()
        return redirect('main_index')
    except Exception as e:
        error = '업로드에 실패했습니다.'
        print(e)
        content = {'message': error}
        return render(request, 'main/error.html', content)
