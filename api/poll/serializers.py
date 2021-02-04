from rest_framework import serializers
from .models import *
from .utils import validate_question_type


class PollSerializers(serializers.ModelSerializer):
    class Meta:
        model = Poll
        fields = '__all__'

    def validate(self, data):
        """
        Проверка даты старта.
        """
        if data['start_date'] > data['finish_date']:
            raise serializers.ValidationError("finish must occur after start")
        return data


class QuestionSerializers(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = '__all__'


class OptionsSerializers(serializers.ModelSerializer):
    class Meta:
        model = Options
        fields = '__all__'


class UserAnswerSerializers(serializers.ModelSerializer):
    class Meta:
        model = UserAnswer
        fields = '__all__'


class AnswerSerializers(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = '__all__'
