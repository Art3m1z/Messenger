from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.contrib.auth.forms import UserCreationForm
from .models import Room, Topic, Message
from .forms import RoomForm
from .models import User


def logout_user(request):
    logout(request)
    return redirect('home')


def login_page(request):
    page = 'login'
    context = {'page': page}
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        username = request.POST.get('username').lower()
        password = request.POST.get('password')

        try:
            User.objects.get(username=username)
        except:
            messages.error(request, "User doesn't exist or deleted.")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, "Username OR password is incorrect.")

    return render(request, 'base/login_form.html', context)


def register_page(request):
    form = UserCreationForm()
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request, user)
            return redirect("home")
        else:
            messages.error(request, 'Something goes wrong!')
    context = {'form': form}
    return render(request, 'base/login_form.html', context)


def home(request):
    q = request.GET.get('q') if request.GET.get('q') is not None else ''  # /проверить значения/
    rooms = Room.objects.filter(
        Q(topic__name__icontains=q) |
        Q(name__icontains=q) |
        Q(description__icontains=q)
    )  # /проверить значения/

    room_count = rooms.count()
    topics = Topic.objects.all()
    room_messages = Message.objects.filter(room__topic__name__icontains=q)
    context = {'rooms': rooms, 'topics': topics,
               'room_count': room_count,
               "room_messages": room_messages}  # /проверить значения/
    return render(request, 'base/home.html', context)


def room(request, pk):
    room = Room.objects.get(id=pk)
    messages_room = room.message_set.all().order_by('-created')
    participants = room.participants.all()

    if request.method == "POST":
        Message.objects.create(user=request.user, room=room, body=request.POST.get('body'))
        room.participants.add(request.user)
        return redirect('room', pk=room.id)

    context = {"room": room, "messages_room": messages_room, "participants": participants}
    return render(request, 'base/room.html', context)


@login_required(login_url='login')
def delete_message(request, pk):
    message = Message.objects.get(id=pk)

    # if request.user is not message.user:
    #     return HttpResponse('You are not a creator!')

    if request.method == 'POST':
        message.delete()
        return redirect('home')
    return render(request, 'base/delete_form.html', {'obj': message})


@login_required(login_url='login')
def create_room(request):
    form = RoomForm()
    if request.method == "POST":  # /проверить значения/
        form = RoomForm(request.POST)
        if form.is_valid():  # /проверить значения/
            form.save()
            return redirect('home')

    context = {"form": form}
    return render(request, 'base/room_form.html', context)


@login_required(login_url='login')
def update_form(request, pk):
    room = Room.objects.get(id=pk)
    form = RoomForm(instance=room)

    if request.user is not room.host:
        return HttpResponse('You are not allowed here!')

    if request.method == "POST":
        form = RoomForm(request.POST, instance=room)

        if form.is_valid():
            form.save()

            return redirect('home')

    context = {'form': form}
    return render(request, 'base/room_form.html', context)


@login_required(login_url='login')
def delete_form(request, pk):
    room = Room.objects.get(id=pk)

    if request.user is not room.host:
        return HttpResponse('You are not allowed here!')

    if request.method == 'POST':
        room.delete()
        return redirect('home')
    return render(request, 'base/delete_form.html', {'obj': room})
