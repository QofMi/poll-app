from rest_framework.response import Response
from rest_framework.exceptions import ParseError
from django.http import Http404
from datetime import date
from .utils import check_active_poll


class PollListMixin:
    """ Получение списка активных опросов """
    poll_model = None
    poll_serializer = None

    def get(self, request):
        today = date.today()
        object = self.poll_model.objects.filter(start_date__lte=today, finish_date__gte=today)

        return Response(self.poll_serializer(object, many=True).data)


class PollByIdMixin:
    """
    GET - Получение информации об опросе
    POST - Прохождение опроса пользователем
    """
    poll_model = None
    poll_serializer = None
    question_serializer = None
    option_serializer = None
    answer_object = None
    user_answer_object = None

    def get(self, request, id):
        try:
            object = self.poll_model.objects.get(id=id)
            check_active_poll(object)

            serializer = self.poll_serializer(object).data
            serializer['questions'] = []
            for question in object.question_set.all():
                questions = self.question_serializer(question).data

                if question.question_type:
                    options = question.options_set.all()
                    questions['options'] = self.option_serializer(options, many=True).data
                serializer['questions'].append(questions)

            return Response(serializer)

        except self.poll_model.DoesNotExist:
            raise Http404
        except Exception as error:
            raise ParseError(error)

    def post(self, request, id):
        try:
            object = self.poll_model.objects.get(id=id)
            check_active_poll(object)

            user_id = request.data['user_id']
            answer_dict = request.data['answers']

            if self.user_answer_object.objects.filter(user_id=user_id, poll=object).count() > 0:
                raise Exception('This user already has submitted to this poll')

            answer_list = []
            for question in object.question_set.all():
                answer_data = answer_dict[str(question.id)]
                answer = self.answer_object(question=question, question_type=question.type, question_text=question.text)

                if question.type == 'TEXT':
                    answer.question_answer = answer_data

                if question.type == 'CHOICE':
                    option = question.options_set.filter(index=answer_data).first()
                    if option:
                        answer.question_answer = option.text

                if question.type == 'MULTIPLE_CHOICE':
                    options = question.options_set.all()
                    result = []
                    for index in answer_data:
                        option = next((o for o in options if o.index == index), None)
                        if option:
                            result.append(option.text)
                    answer.question_answer = json.dumps(result)

                answer_list.append(answer)

            new_user_answer = self.user_answer_object(user_id=user_id, poll=object)
            new_user_answer.save()
            for new_answer in answer_list:
                new_answer.user_answer = new_user_answer
                new_answer.save()

            return Response('Accepted')

        except self.poll_model.DoesNotExist:
            raise Http404()
        except Exception as ex:
            raise ParseError(ex)


class UserPollMixin:
    """
    Вывод пройденных пользователем опросов, с детализацией выбранных ответов
    """
    user_answer_object = None
    user_answer_serializer = None

    def get(self, request, id):
        try:
            results_answer = []
            for user_answer in self.user_answer_object.objects.filter(user_id=id):
                serializer = self.user_answer_serializer(user_answer).data
                serializer['answers'] = []
                for answer in user_answer.answer_set.all():
                    question_answer = answer.question_answer
                    if answer.question_type == 'MULTIPLE_CHOICE':
                        question_answer = json.loads(question_answer)

                    serializer['answers'].append({
                        'question': {
                            'id': answer.question_id,
                            'type': answer.question_type,
                            'text': answer.question_answer
                        },
                        'answer': question_answer
                    })

                results_answer.append(serializer)

            return Response(results_answer)

        except Exception as ex:
            raise ParseError(ex)
