from django.core.exceptions import ValidationError
from datetime import date


QUESTION_TYPES = ['TEXT', 'CHOICE', 'MULTIPLE_CHOICE']


def validate_question_type(value) -> None:
    """ Проверка типа вопроса """
    if not value in QUESTION_TYPES:
        raise ValidationError('Invalid question type')


def check_active_poll(model) -> None:
    """ Проверка активности опроса """
    get_today = date.today()
    if model.finish_date < get_today:
        raise model.DoesNotExist
