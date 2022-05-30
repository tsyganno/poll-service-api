from rest_framework import serializers
from django.contrib.auth.models import User

from poll_service_api.models import Vote, Question


class VoteSerializer(serializers.ModelSerializer):

    class Meta:
        model = Vote
        fields = '__all__'


class QuestionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Question
        fields = '__all__'
