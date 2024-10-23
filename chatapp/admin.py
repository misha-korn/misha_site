from django.contrib import admin
from chatapp.models import Message, Chat, User, ChatUserInfo

# Register your models here.
admin.site.register(Message)
admin.site.register(Chat)
admin.site.register(User)
admin.site.register(ChatUserInfo)
