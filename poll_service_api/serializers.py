from rest_framework import serializers
from django.contrib.auth.models import User

from poll_service_api.models import Vote, Question, Answer


class VoteSerializer(serializers.ModelSerializer):

    class Meta:
        model = Vote
        fields = '__all__'


class QuestionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Question
        fields = ['id', 'vote', 'type_question', 'text']


class QuestionDetailSerializer(serializers.ModelSerializer):
    variants = serializers.SlugRelatedField(many=True, read_only=True, slug_field='name_variant')

    class Meta:
        model = Question
        fields = ['id', 'type_question', 'text', 'variants']


class FilteredListSerializer(serializers.ListSerializer):

    def to_representation(self, data):
        value = self.context['request'].session['username']
        num = User.objects.get(username=value)
        data = data.filter(user=num.pk)
        return super(FilteredListSerializer, self).to_representation(data)


class AnswerSerializer(serializers.ModelSerializer):

    class Meta:
        list_serializer_class = FilteredListSerializer
        model = Answer
        fields = ['id', 'answer', 'question', 'user']
        read_only_fields = ('user', 'question',)


class ResultSerializer(serializers.ModelSerializer):
    answers = AnswerSerializer(many=True, read_only=True)

    class Meta:
        model = Question
        fields = ['id', 'type_question', 'text', 'correct_answer', 'answers']


class AnswerForDeleteSerializer(serializers.ModelSerializer):

    class Meta:
        model = Answer
        fields = ['id', 'answer', 'question', 'user']
