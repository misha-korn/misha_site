from django.urls import path
from mainapp.views import main, calculator_f, iq_test, start_test, result

app_name = "mainapp"

urlpatterns = [
    path("", main, name="main"),
    path("calculator/", calculator_f, name="calculator"),
    path("iq_test/", iq_test, name="iq_test"),
    path("start_test/<int:n_que>/", start_test, name="start_test"),
    path("result/", result, name="result"),
    
]
