from django.db import models
from .utils import validate_question_type
import uuid


class Poll(models.Model):
    """ Модель опроса """
    title = models.CharField(max_length=150, db_index=True)
    description = models.CharField(max_length=400, blank=True)
    start_date = models.DateField()
    finish_date = models.DateField()

    def __str__(self):
        return self.title


class Question(models.Model):
    """ Модель вопросов """
    poll = models.ForeignKey('Poll', on_delete=models.CASCADE, blank=True)
    type = models.CharField(max_length=30, validators=[validate_question_type])
    text = models.CharField(max_length=200)

    @property
    def question_type(self):
        return self.type in ['CHOICE', 'MULTIPLE_CHOICE']

    def __str__(self):
        return str(f'{self.poll} - {self.text}')


class Options(models.Model):
    """ Модель вариантов """
    question = models.ForeignKey('Question', on_delete=models.CASCADE, blank=True)
    index = models.PositiveIntegerField()
    text = models.CharField(max_length=100)

    def __str__(self):
        return self.text


class UserAnswer(models.Model):
    """ Модель заполненного опроса """
    user_id = models.IntegerField(db_index=True, blank=True)
    poll = models.ForeignKey('Poll', on_delete=models.CASCADE)

    def __str__(self):
        return str(f'{self.poll} - {self.user_id}')


class Answer(models.Model):
    """ Модель ответа на вопрос """
    user_answer = models.ForeignKey('UserAnswer', on_delete=models.CASCADE, blank=True)
    question = models.ForeignKey('Question', on_delete=models.CASCADE, blank=True)
    question_type = models.CharField(max_length=30, validators=[validate_question_type])
    question_text = models.CharField(max_length=200)
    question_answer = models.CharField(max_length=200)

    def __str__(self):
        return str(f'{self.question} - {self.question_answer}')
