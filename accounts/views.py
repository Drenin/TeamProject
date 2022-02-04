from django.shortcuts import render
from .forms import RegisterForm

# Create your views here.


# Create your models here.
def register(request):
    if request.method == 'POST':
        user_form = RegisterForm(request.POST)
        if user_form.is_valid():
            new_user = user_form.save(commit=False)
            new_user.set_password(user_form.cleaned_data['password']) # 암호화
            new_user.save() # DB 저장
            return render(request, 'registration/register_done.html', {'form':user_form})
    else:
        user_form = RegisterForm()
    return render(request, 'registration/register.html', {'form':user_form})