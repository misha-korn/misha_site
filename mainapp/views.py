from django.shortcuts import render, HttpResponse, HttpResponseRedirect
from django.urls import reverse
from mainapp.calculator import (
    message_processing,
    sokrashenie_biggest,
    sokrashenie,
    addition,
    subtraction,
    bigger_smaller,
    checking_for_positivity,
    znam,
    arithmetic_operations,
    arifmetic_operations_div_mult,
    error,
)
from mainapp.models import Answer, Question, Test, TestAnswer
import random


# Create your views here.


def main(request):
    return render(request, "mainapp/main.html")


def calculator_f(request):
    context = {"answer": ""}
    text_calc = request.GET.get("text_calc")
    if text_calc:
        # считаем
        answer = message_processing(text_calc)
        context = {"answer": answer, "text_calc": text_calc}
    return render(request, "mainapp/calculator.html", context=context)


def iq_test(request):
    return render(request, "mainapp/iq_test.html")


def start_test(request, n_que):
    if request.GET.get("name"):
        test_obj = Test.objects.create(name=request.GET.get("name"))
        test_obj.save()
        test_id = test_obj.id
    elif request.GET.get("answer"):
        test_id = request.GET.get("test")
        test_answer_obj = TestAnswer.objects.create(
            test_id=test_id,
            question_num=n_que,
            question_id=int(request.GET.get("question")),
            answer_id=int(request.GET.get("answer")),
        )
        test_answer_obj.save()

    index_question = n_que + 1
    question_lst = Question.objects.all()

    # print(n_que, len(question_lst))

    if n_que < len(question_lst):
        question = question_lst[n_que]
        answers_list = Answer.objects.filter(question=question)
        if index_question == len(question_lst):
            last_question = True
        else:
            last_question = False
        answers_list = list(answers_list)
        random.shuffle(answers_list)
        context = {
            "question": question,
            "answers_list": answers_list,
            "index_question": index_question,
            "last_question": last_question,
            "test_id": test_id,
        }

    # print(Question.objects.all()[0].text)
    return render(request, "mainapp/start_test.html", context)


def result(request):
    test_id = request.GET.get("test")
    test_answer_obj = TestAnswer.objects.create(
        test_id=test_id,
        question_num=4,
        question_id=int(request.GET.get("question")),
        answer_id=int(request.GET.get("answer")),
    )
    test_answer_obj.save()
    your_answers = TestAnswer.objects.filter(test_id=test_id)
    correct_answers = round(
        your_answers.filter(answer__correct=1).count() * (100 / len(your_answers))
    )

    all_answers = Answer.objects.all()
    context = {
        "your_answers": your_answers,
        "all_answers": all_answers,
        "correct_answers": correct_answers,
    }
    return render(request, "mainapp/result.html", context)


# def start_test(request):
#     return render(request, "mainapp/start_test.html")
