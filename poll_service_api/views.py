from django.http import HttpResponseNotFound, HttpResponseServerError, HttpResponse
from django.utils import timezone
from django.contrib.auth.models import User
from poll_service_api.serializers import VoteSerializer, QuestionSerializer, AnswerSerializer, ResultSerializer, QuestionDetailSerializer
from rest_framework.generics import ListAPIView, RetrieveAPIView, CreateAPIView, DestroyAPIView
from random import choice
import string

from poll_service_api.models import Vote, Question, Answer


def custom_handler404(request, exception):
    return HttpResponseNotFound('Ресурс не найден!')


def custom_handler500(request):
    return HttpResponseServerError('Ошибка сервера!')


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


class AnswerCreateView(CreateAPIView, RetrieveAPIView):

    def get_serializer_class(self):
        if self.request.method in ('GET',):
            return QuestionDetailSerializer
        return AnswerSerializer

    def perform_create(self, serializer):
        value = self.request.session['username']
        num = User.objects.get(username=value)
        return serializer.save(user_id=num.pk, question_id=self.kwargs['question_pk'])

    def get_object(self):
        return Question.objects.get(id=self.kwargs['question_pk'])


class ResultsListView(ListAPIView):
    serializer_class = ResultSerializer

    def get_queryset(self):
        value = self.request.session['username']
        num = User.objects.get(username=value)
        return Question.objects.filter(answers__user__id=num.pk).distinct()


class DeleteResultsListView(DestroyAPIView, ListAPIView):
    serializer_class = AnswerSerializer

    def get_object(self):
        value = self.request.session['username']
        num = User.objects.get(username=value)
        return Answer.objects.filter(user__id=num.pk).distinct()

    def get_queryset(self):
        value = self.request.session['username']
        num = User.objects.get(username=value)
        return Answer.objects.filter(user__id=num.pk).distinct()
