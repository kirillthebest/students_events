from functools import reduce

from events.forms import LoginForm, DocumentForm
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from events.models import Profile, Event, ProfileEvent, StudentGroup
from django.contrib.auth import authenticate, logout as do_logout, login
from django.contrib.auth.decorators import login_required
import datetime
from django.db.models import Q
from django.contrib import messages
import operator

def get_profile(request):
    return get_object_or_404(Profile, user=request.user)

def ru_plural(value, variants):
    value = abs(int(value))

    if value % 10 == 1 and value % 100 != 11:
        variant = 0
    elif value % 10 >= 2 and value % 10 <= 4 and \
            (value % 100 < 10 or value % 100 >= 20):
        variant = 1
    else:
        variant = 2

    return variants[variant]

@login_required
def show_events_page(request):
    profile = get_profile(request)
    events = Event.objects.filter(Q(event_end__gte=datetime.datetime.now()) | Q(event_end__isnull=True))
    for event in events:
        if ProfileEvent.objects.filter(profile=profile, event=event).count():
            event.is_participate = True
        else:
            event.is_participate = False
    return render(request, 'events/events.html', {
        'profile': profile,
        'events': events
    })

@login_required
def show_student_page(request):
    profile = get_profile(request)
    if profile.user.is_superuser:
        return redirect('events_page')

    filter_names = ('event__event_date__gte', 'event__event_date__lte')

    events = ProfileEvent.objects.filter(profile=profile).all()

    filter_clauses = [Q(**{filter: request.GET[filter]})
                  for filter in filter_names
                  if request.GET.get(filter)]

    if filter_clauses:
        events = events.filter(reduce(operator.and_, filter_clauses))

    if request.GET.get('only_active'):
        events = events.filter(score__isnull=True)

    date_from = request.GET.get('event__event_date__gte') or ''
    date_to = request.GET.get('event__event_date__lte') or ''
    only_active = request.GET.get('only_active') or ''

    rating = 0
    for event in events:
        if event.score:
            rating += event.score
    return render(request, 'events/student.html', {
        'profile': profile,
        'events': events, 'only_active': only_active,
        'date_from': date_from, 'date_to': date_to,
        'rating': str(rating) + " " + ru_plural(rating, ['балл', 'балла', 'баллов'])
    })

def upload_event_document(request):
    if request.method == 'POST':
        instance = get_object_or_404(ProfileEvent, id=request.POST.get('event_id'))
        form = DocumentForm(request.POST, request.FILES, instance=instance)
        if form.is_valid():
            form.save()
            return redirect('student_page')


def participate(request, event_id):
    event = get_object_or_404(Event, pk=event_id)
    ProfileEvent(profile=get_profile(request), event=event).save()
    messages.success(request, "Вы записались на мероприятие '"+event.name+"'")
    return redirect('events_page')

@login_required
def show_teacher_page(request):
    profile = get_profile(request)
    if not profile.user.is_superuser:
        return redirect('events_page')

    filter_names = ('event__event_date__gte', 'event__event_date__lte', 'profile_id', 'profile__group_id')

    events = ProfileEvent.objects.all()

    filter_clauses = [Q(**{filter: request.GET[filter]})
                      for filter in filter_names
                      if request.GET.get(filter)]

    if filter_clauses:
        events = events.filter(reduce(operator.and_, filter_clauses))

    if request.GET.get('only_active'):
        events = events.filter(score__isnull=True)

    date_from = request.GET.get('event__event_date__gte') or ''
    date_to = request.GET.get('event__event_date__lte') or ''
    only_active = request.GET.get('only_active') or ''
    student_selected = request.GET.get('profile_id') or ''
    group_selected = request.GET.get('profile__group_id') or ''

    rating = 0
    for event in events:
        if event.score:
            rating += event.score

    rating_text = 'Общий рейтинг: '
    if student_selected:
        rating_text = 'Рейтинг студента ' + str(get_object_or_404(Profile, id=student_selected)) + ": "
    if group_selected:
        rating_text = 'Рейтинг группы ' + str(get_object_or_404(StudentGroup, id=group_selected)) + ": "

    return render(request, 'events/teacher.html', {
        'profile': profile, 'students': Profile.objects.filter(user__is_superuser=False), 'groups': StudentGroup.objects.all(),
        'events': events, 'only_active': only_active, 'student_selected': int(student_selected or 0),
        'date_from': date_from, 'date_to': date_to, 'group_selected': int(group_selected or 0),
        'rating': str(rating_text) + str(rating) + " " + ru_plural(rating, ['балл', 'балла', 'баллов'])
    })

# выход (деавторизация)
def logout(request):
    do_logout(request)
    return redirect('auth')

# авторизация
def auth(request):

    # если юзер уже авторизован - выходим
    if request.user.is_authenticated:
        return redirect('events_page')

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
