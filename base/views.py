from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse
from django.views import View
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.contrib.auth.forms import UserCreationForm
from .models import Room, Topic, Message, User
from .forms import RoomForm, UserForm, MyUserCreationForm

template_login = 'base/login_form.html'


class LoginPage(View):

    def get(self, request):
        page = 'login'
        if request.user.is_authenticated:
            return redirect('home')
        context = {'page': page}
        return render(request, template_login, context)

    def post(self, request):
        email = request.POST.get('email')
        password = request.POST.get('password')

        try:
            User.objects.get(email=email)
        except:
            messages.error(request, "User doesn't exist or deleted.")

        user = authenticate(request, email=email, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, "Username OR password is incorrect.")


class LogoutUser(View):
    def get(self, request):
        logout(request)
        return redirect('home')


class RegisterPage(View):

    def get(self, request):
        form = MyUserCreationForm()
        return render(request, template_login, {"form": form})

    def post(self, request):
        form = MyUserCreationForm()
        if request.method == 'POST':
            form = MyUserCreationForm(request.POST)
            if form.is_valid():
                user = form.save(commit=False)
                user.username = user.username.lower()
                user.save()
                login(request, user)

                return redirect("home")
            else:
                messages.error(request, 'Something goes wrong!')
                messages.error(request, 'Password should contain at least one number without special symbols')
        context = {'form': form}
        return render(request, template_login, context)


class HomePage(View):

    def get(self, request):
        template = 'base/home.html'
        q = request.GET.get('q') if request.GET.get('q') is not None else ''  # /проверить значения/
        rooms = Room.objects.filter(
            Q(topic__name__icontains=q) |
            Q(name__icontains=q) |
            Q(description__icontains=q)
        )  # /проверить значения/

        room_count = rooms.count()
        topics = Topic.objects.all()[0:3]
        room_messages = Message.objects.filter(room__topic__name__icontains=q)
        context = {'rooms': rooms, 'topics': topics,
                   'room_count': room_count,
                   "room_messages": room_messages}  # /проверить значения/
        return render(request, template, context)


class RoomPage(View):

    def get(self, request, pk):
        template = "base/room.html"
        room = Room.objects.get(id=pk)
        messages_room = room.message_set.all()
        participants = room.participants.all()
        context = {"room": room, "messages_room": messages_room, "participants": participants}
        return render(request, template, context)

    def post(self, request, pk):
        room = Room.objects.get(id=pk)
        room.message_set.all()
        room.participants.all()
        Message.objects.create(user=request.user, room=room, body=request.POST.get('body'))
        room.participants.add(request.user)

        return redirect('room', pk=room.id)


class UserProfile(View):

    def get(self, request, pk):
        template = 'base/profile.html'
        user = User.objects.get(id=pk)
        rooms = user.room_set.all()
        room_messages = user.message_set.all()
        topics = Topic.objects.all()
        context = {"user": user, "rooms": rooms, "room_messages": room_messages,
                   "topics": topics,
                   }
        return render(request, template, context)


class DeleteMessage(View):

    def get(self, request, pk):
        template = 'base/delete_form.html'
        message = Message.objects.get(id=pk)
        return render(request, template, {'obj': message})

    def post(self, request, pk):
        message = Message.objects.get(id=pk)
        message.delete()
        return redirect('home')


class CreateRoom(View):

    def get(self, request):
        template = 'base/create_room.html'
        form = RoomForm()
        topics = Topic.objects.all()
        context = {"form": form, "topics": topics}
        return render(request, template, context)

    def post(self, request):
        topic_name = request.POST.get('topic')
        topic, created = Topic.objects.get_or_create(name=topic_name)
        Room.objects.create(
            host=request.user,
            topic=topic,
            name=request.POST.get('name'),
            description=request.POST.get('description'),
        )
        return redirect('home')


class UpdateForm(View):

    def get(self, request, pk):
        template = 'base/create_room.html'

        room = Room.objects.get(id=pk)
        form = RoomForm(instance=room)
        topics = Topic.objects.all()
        if request.user != room.host:
            return HttpResponse('You are not allowed here!')
        context = {'form': form, "topics": topics, "room": room}

        return render(request, template, context)

    def post(self, request, pk):
        room = Room.objects.get(id=pk)

        topic_name = request.POST.get('topic')
        topic, created = Topic.objects.get_or_create(name=topic_name)
        room.name = request.POST.get('name')
        room.topic = topic
        room.description = request.POST.get('description')
        room.save()

        return redirect('home')


class DeleteRoom(View):

    def get(self, request, pk):
        template = 'base/delete_form.html'
        room = Room.objects.get(id=pk)
        if request.user != room.host:
            return HttpResponse('You are not allowed here!')
        return render(request, template, {'obj': room})

    def post(self, request, pk):
        room = Room.objects.get(id=pk)
        room.delete()
        return redirect('home')


class UserUpdate(View):

    def get(self, request):
        template = 'base/update_user.html'
        user = request.user
        form = UserForm(instance=user)
        context = {"form": form}
        return render(request, template, context)

    def post(self, request):
        user = request.user
        form = UserForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            return redirect('user_profile', pk=user.id)


class BrowseTopic(View):

    def get(self, request):
        template = 'base/topic.html'
        q = request.GET.get('q') if request.GET.get('q') is not None else ''
        topics = Topic.objects.filter(name__icontains=q)
        topics_count = topics.count()
        context = {"topics": topics, "topics_count": topics_count}
        return render(request, template, context)


class BrowseActivities(View):

    def get(self, request):
        template = 'base/activity.html'
        activity = Message.objects.all()
        context = {"activity": activity}

        return render(request, template, context)
