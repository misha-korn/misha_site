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
    count_drob = request.GET.get("count_drob")
    chisl = []
    znam = []
    znak = []
    cel = []
    if text_calc:
        # считаем
        answer = message_processing(text_calc)
        context = {"answer": answer, "text_calc": text_calc}
    elif count_drob:
        print(request.GET)
        for i in range(int(count_drob) - 1):
            chisl.append(request.GET.get("chisl" + str(i)))
            znam.append(request.GET.get("znam" + str(i)))
            znak.append(request.GET.get("znak" + str(i)))
            # print(request.GET.get("znak" + str(i)))
            cel.append(request.GET.get("celoe" + str(i)))
        chisl.append(request.GET.get("chisl" + str(i + 1)))
        znam.append(request.GET.get("znam" + str(i + 1)))
        cel.append(request.GET.get("celoe" + str(i + 1)))
        text_primer = ""
        for i in range(int(count_drob) - 1):
            if cel[i]:
                text_primer += cel[i]
                text_primer += " "
            text_primer += chisl[i]
            text_primer += "/"
            text_primer += znam[i]
            text_primer += " "
            # print(znak[i], int(count_drob) - 1, znak)
            text_primer += znak[i]
            text_primer += " "
        if cel[i + 1]:
            text_primer += cel[i + 1]
            text_primer += " "
        text_primer += chisl[i + 1]
        text_primer += "/"
        text_primer += znam[i + 1]
        print(cel)
        print(chisl)
        print(znam)
        print(znak)
        print(text_primer)
        answer2 = message_processing(text_primer)
        print(answer2)
        znak.append("")
        primer = [
            [i, cel[i], chisl[i], znam[i], znak[i]] for i in range(int(count_drob))
        ]

        if answer2 == "-0":
            answer2 = "0"

        context = {
            "answer2": answer2,
            "text_primer": text_primer,
            "primer": primer,
            "znaki": ["+", "-", "*", "/"],
        }
    else:
        primer = [[0, "", "", "", "+"], [1, "", "", "", ""]]
        context = {
            "primer": primer,
            "znaki": ["+", "-", "*", "/"],
        }

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
