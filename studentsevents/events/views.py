from django.contrib.auth import authenticate, login, logout
from events.forms import LoginForm
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from events.models import Profile

def show_events_page(request):
    return render(request, 'events/events.html')


def show_student_page(request):
    return render(request, 'events/student.html')


def show_teacher_page(request):
    return render(request, 'events/teacher.html')


# Create your views here.
def show_login_page(request):
    return render(request, 'events/auth.html')

# авторизация
def auth(request):

    # если юзер уже авторизован - выходим
    # if request.user.is_authenticated:
    #     return redirect('logout')

    # инициализируем объект формы
    form = LoginForm()

    if request.method == 'POST':
        # если форма была отправлена - заполняем объект данным из POST запроса
        form = LoginForm(request.POST)

        if form.is_valid():
            # валидируем форму
            try:
                # если юзер ввел правильные логин и пароль - авторизуем
                user = authenticate(request, username=form.cleaned_data['username'], password=form.cleaned_data['password'])
                if user is not None:
                    if get_object_or_404(Profile, user_id=user.id):
                        login(request, user)
                        return redirect('events_page')
                    else:
                        form.add_error(None, 'Неверные данные!')
                else:
                    form.add_error(None, 'Неверные данные!')
            except Exception as e:
                print(str(e))
                form.add_error(None, 'Ошибка при авторизации. Пожалуйста, обратитесь к администратору')

    # иначе отображаем страницу с авторизацией
    return render(request, 'events/auth.html', {'form': form})
