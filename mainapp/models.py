from django.db import models

# Create your models here.


class Question(models.Model):
    text = models.TextField()
    img = models.ImageField(upload_to="question_img", null=True, blank=True)

    def __str__(self):
        return f"{self.id}.{self.text}"


class Answer(models.Model):
    text = models.TextField()
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    correct = models.BooleanField(default=False)
    img = models.ImageField(upload_to="answer_img", null=True, blank=True)

    def __str__(self):
        return f"{self.id}. Вопрос: {self.question.id}. Текст ответа: {self.text}"


class Test(models.Model):
    name = models.TextField()


class TestAnswer(models.Model):
    test = models.ForeignKey(Test, on_delete=models.CASCADE)
    question_num = models.IntegerField()
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE)
