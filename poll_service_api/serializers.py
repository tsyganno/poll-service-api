from rest_framework import serializers

from poll_service_api.models import Vote, Question, Variant, Answer


class VoteSerializer(serializers.ModelSerializer):

    class Meta:
        model = Vote
        fields = '__all__'


class QuestionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Question
        fields = ['vote', 'type_question', 'text']


class AnswerSerializer(serializers.ModelSerializer):

    class Meta:
        model = Answer
        fields = ['answer', 'date_of_answer', 'question', 'user']
        read_only_fields = ('user', 'question',)


class QuestionDetailSerializer(serializers.ModelSerializer):
    variants = serializers.SlugRelatedField(many=True, read_only=True, slug_field='name_variant')

    class Meta:
        model = Question
        fields = ['id', 'type_question', 'text', 'variants']


