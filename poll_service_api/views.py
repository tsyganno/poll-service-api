from django.shortcuts import render
from django.http import HttpResponseNotFound, HttpResponseServerError, HttpResponseRedirect, HttpResponse
from django.shortcuts import reverse
from django.contrib.auth.models import User
from poll_service_api.serializers import VoteSerializer, QuestionSerializer, AnswerSerializer, QuestionDetailSerializer
from rest_framework.generics import ListAPIView, RetrieveAPIView, CreateAPIView, ListCreateAPIView

from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response

from poll_service_api.models import Vote, Question, Variant, Answer

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
    request.session['username'] = 'lol'
    user = User()
    user.username = 'lol'
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
        value = self.request.session['username']
        num = User.objects.get(username=value)
        return serializer.save(user_id=num.pk, question_id=self.kwargs['question_pk'])

    def get_object(self):
        return Question.objects.get(question__id=self.kwargs['question_pk'])


class ResultsListView(ListAPIView):
    serializer_class = AnswerSerializer

    def get_queryset(self):
        return Answer.objects.filter(user__id=self.kwargs['pk'])


"""
def record_to_model_one_answer(request, pk: int):
    answer = Answer()
    num = Vote.objects.filter(question__id=pk).first().id
    variants = Variant.objects.filter(question__id=pk)
    if request.POST:
        for el in variants:
            if el.id == int(request.POST['variant']):
                answer.answer = el.name_variant
                answer.user = request.user
                answer.question = Question.objects.get(id=pk)
                answer.save()
    return HttpResponseRedirect(reverse('questions', args=[num]))


def record_to_model_some_answers(request, pk: int):
    answer = Answer()
    num = Vote.objects.filter(question__id=pk).first().id
    variants = Variant.objects.filter(question__id=pk)
    id_list = request.POST.getlist('variantid')
    answer_word = ''
    if request.POST:
        for variant in variants:
            for el in id_list:
                if variant.id == int(el):
                    answer_word += str(variant.name_variant) + ' '
        answer.answer = answer_word
        answer.user = request.user
        answer.question = Question.objects.get(id=pk)
        answer.save()
    return HttpResponseRedirect(reverse('questions', args=[num]))
"""










