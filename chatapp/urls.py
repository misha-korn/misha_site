from django.urls import path
from chatapp.views import (
    chat,
    login_view,
    registr,
    messenger,
    profile,
    exit,
    get_messages,
    getuser_byusername,
    create_chat,
)

app_name = "chatapp"

urlpatterns = [
    path("", chat, name="chat"),
    path("login/", login_view, name="login"),
    path("registr/", registr, name="registr"),
    path("messenger/", messenger, name="messenger"),
    path("profile/", profile, name="profile"),
    path("exit", exit, name="exit"),
    path("get_messages", get_messages, name="get_messages"),
    path("chat_search_user", getuser_byusername, name="getuser_byusername"),
    path("create_chat", create_chat, name="create_chat"),
]
