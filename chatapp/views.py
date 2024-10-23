from django.shortcuts import render, HttpResponse, HttpResponseRedirect
from django.urls import reverse
from chatapp.models import User, Chat, ChatUserInfo, Message
from chatapp.forms import UserLoginForm, UserRegistrForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse


@login_required
def chat(request):
    # print(request.user)
    if request.method == "GET":
        chat_id = request.GET.get("mess")
        chats_by_user = ChatUserInfo.objects.filter(user=request.user).values_list(
            "chat_id", flat=True
        )

        user_chats = ChatUserInfo.objects.filter(chat__in=chats_by_user).exclude(
            user=request.user
        )

        message_chat = None

        if chat_id:
            message_chat = Message.objects.filter(chat_id=chat_id)
            chat_id = int(chat_id)
        #     print(message_chat)
        # print(user_chats)

        context = {
            "user_chats": user_chats,
            "message_chat": message_chat,
            "req_user": request.user,
            "chat_id": chat_id,
        }

        return render(request, "chatapp/chat.html", context)
    else:
        new_message = request.POST.get("message")
        chat_id = request.POST.get("chat_id")
        message = Message.objects.create(
            text=new_message,
            user=request.user,
            chat=Chat.objects.get(id=chat_id),
        )
        message.save()
        return HttpResponseRedirect(f"/chat/?mess={chat_id}")


def login_view(request):
    if request.method == "GET":
        login_form = UserLoginForm()
    else:
        login_form = UserLoginForm(data=request.POST)
        if login_form.is_valid():
            username = request.POST["username"]
            password = request.POST["password"]
            user = authenticate(username=username, password=password)
            print(user)
            if user:
                login(request, user)
                # Успешный вход
                return HttpResponseRedirect(reverse("chatapp:chat"))
    context = {"login_form": login_form}
    return render(request, "chatapp/login.html", context)


def registr(request):
    if request.method == "GET":
        registr_form = UserRegistrForm()
    else:
        registr_form = UserRegistrForm(data=request.POST)
        if registr_form.is_valid():
            registr_form.save()
            return HttpResponseRedirect(reverse("chatapp:chat"))
    context = {"registr_form": registr_form}
    return render(request, "chatapp/registr.html", context)


def messenger(request):
    return render(request, "chatapp/messenger.html")


def profile(request):
    return render(request, "chatapp/profile.html")


def exit(request):
    logout(request)
    return HttpResponseRedirect(reverse("mainapp:main"))


def get_messages(request):
    chat_id = request.GET.get("chat_id")
    chat = Message.objects.filter(chat_id=chat_id)
    # chat = Message.objects.all()
    return JsonResponse({"messages": list(chat.values())})


def getuser_byusername(request):
    username = request.GET.get("username")
    users = User.objects.filter(username__startswith=username)
    print(users)
    return JsonResponse({"users": list(users.values())})


def create_chat(request):
    id1 = request.GET.get("id1")
    id2 = request.GET.get("id2")
    set_ids1 = set(
        ChatUserInfo.objects.filter(user_id=id2).values_list("chat_id", flat=True)
    )
    set_ids2 = set(
        ChatUserInfo.objects.filter(user_id=id1).values_list("chat_id", flat=True)
    )
    common_chat = list(set_ids1 & set_ids2)

    if not common_chat:
        user1 = User.objects.get(id=id1)
        chat_name_1 = user1.username
        user2 = User.objects.get(id=id2)
        chat_name_2 = user2.username
        chat = Chat.objects.create(name=chat_name_1 + " " + chat_name_2)
        chat.save()
        chat1 = ChatUserInfo.objects.create(chat_id=chat.id, user_id=id1)
        chat2 = ChatUserInfo.objects.create(chat_id=chat.id, user_id=id2)
        chat1.save()
        chat2.save()
        return HttpResponseRedirect(f"/chat/?mess={chat.id}")
    return HttpResponseRedirect(f"/chat/?mess={common_chat[0]}")
