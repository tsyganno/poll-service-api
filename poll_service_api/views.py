from django.shortcuts import render
from rest_framework.response import Response
from poll_service_api.serializers import VoteSerializer, QuestionSerializer
from rest_framework.generics import ListAPIView, GenericAPIView

from poll_service_api.models import Vote, Question


class VoteListView(ListAPIView):
    queryset = Vote.objects.all()
    serializer_class = VoteSerializer


class QuestionListView(ListAPIView):
    serializer_class = QuestionSerializer

    def get_queryset(self):
        return Question.objects.filter(vote__id=self.kwargs['pk'])

