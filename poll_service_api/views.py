from django.shortcuts import render
from django.http import HttpResponseNotFound, HttpResponseServerError, HttpResponseRedirect, HttpResponse
from django.shortcuts import reverse
from django.utils import timezone
from django.contrib.auth.models import User
from poll_service_api.serializers import VoteSerializer, QuestionSerializer, AnswerSerializer, QuestionDetailSerializer, ResultSerializer
from rest_framework.generics import ListAPIView, RetrieveAPIView, CreateAPIView, ListCreateAPIView
from random import choice
import string

from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response

from poll_service_api.models import Vote, Question, Variant, Answer


def custom_handler404(request, exception):
    return HttpResponseNotFound('Ресурс не найден!')


def custom_handler500(request):
    return HttpResponseServerError('Ошибка сервера!')


"""
# Регистрируем псевдоним для чата на 30 дней
    if 'register' in request.POST:
        request.session.set_expiry(2592000)  # устанавливаем время жизни сессии
        request.session['username'] = request.POST['username']
    # Удаляем псевдоним для чата из своей сессии
    if 'unregister' in request.POST:
        request.session['username'].pop(request.POST['username'])
"""


def login(request):
    array = string.ascii_letters
    name = str(timezone.now())
    for i in range(10):
        name += choice(array)
    request.session.set_expiry(2592000)
    request.session['username'] = name
    user = User()
    user.username = name
    user.save()
    return HttpResponse('Добро пожаловать в опросник!')


class VoteListView(ListAPIView):
    queryset = Vote.objects.all()
    serializer_class = VoteSerializer


class QuestionListView(ListAPIView):
    serializer_class = QuestionSerializer

    def get_queryset(self):
        return Question.objects.filter(vote__id=self.kwargs['vote_pk'])


class QuestionView(RetrieveAPIView):
    serializer_class = QuestionDetailSerializer

    def get_object(self):
        return Question.objects.get(id=self.kwargs['question_pk'])


class AnswerCreateView(CreateAPIView):
    serializer_class = AnswerSerializer

    def perform_create(self, serializer):
        if not self.request.session['username']:
            return HttpResponseRedirect(reverse('login'))
        value = self.request.session['username']
        num = User.objects.get(username=value)
        return serializer.save(user_id=num.pk, question_id=self.kwargs['question_pk'])

    def get_object(self):
        return Question.objects.get(question__id=self.kwargs['question_pk'])


class ResultsListView(ListAPIView):
    serializer_class = ResultSerializer

    def get_queryset(self):
        if not self.request.session['username']:
            return HttpResponseRedirect(reverse('login'))
        value = self.request.session['username']
        num = User.objects.get(username=value)
        return Question.objects.filter(answers__user__id=num.pk).distinct()
