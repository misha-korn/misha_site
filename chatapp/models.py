from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    img = models.ImageField(upload_to="user_img", default="user_img/default.png")

    def __str__(self):
        return f"{self.id}.{self.username}"


class Chat(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.id}.{self.name}"


class Message(models.Model):
    text = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.id}.{self.user.username} | {self.text[:20]}"


class ChatUserInfo(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.id} | {self.chat.id}.{self.user.username}"
