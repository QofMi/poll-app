from rest_framework.response import Response
from rest_framework.exceptions import ParseError
from django.http import Http404


class AdminPollListMixin:
    """
    GET - Получение списка опросов
    POST - Создание нового опроса
    """
    poll_model = None
    poll_serializer = None

    def get(self, request):
        object = self.poll_model.objects.all()
        return Response(self.poll_serializer(object, many=True).data)

    def post(self,  request):
        try:
            serializer = self.poll_serializer(data=request.data)
            if serializer.is_valid(raise_exception=True):
                valid_data = serializer.validated_data
                new_object = self.poll_model(**valid_data)
                new_object.save()

                return Response(self.poll_serializer(new_object).data)

        except Exception as error:
            raise ParseError(error)


class AdminPollByIdMixin:
    """
    GET - Получение опроса по id
    PATCH - Редактирование опроса
    DELETE - Удаление опроса
    """
    poll_model = None
    poll_serializer = None
    question_serializer = None
    option_serializer = None

    def get(self, request, id):
        try:
            object = self.poll_model.objects.get(id=id)
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

    def patch(self, request, id):
        try:
            object = self.poll_model.objects.get(id=id)
            serializer = self.poll_serializer(data=request.data)

            if serializer.is_valid(raise_exception=True):
                valid_data = serializer.validated_data
                object.title = valid_data['title']
                object.description = valid_data['description']
                object.finish_date = valid_data['finish_date']
                object.save()

                return Response(self.poll_serializer(object).data)

        except self.poll_model.DoesNotExist:
            raise Http404
        except Exception as error:
            raise ParseError(error)

    def delete(self, request, id):
        try:
            object = self.poll_model.objects.get(id=id)
            object.delete()

            return Response(f'Object {object} was deleted!')

        except self.poll_model.DoesNotExist:
            raise Http404
        except Exception as error:
            raise ParseError(error)


class AdminQuestionMixin:
    """
    GET - Получение списка вопросов
    POST - Создание нового вопроса для опроса
    """
    poll_model = None
    question_object = None
    question_serializer = None

    def get(self, request, id):
        object = self.question_object.objects.all()
        return Response(self.question_serializer(object, many=True).data)

    def post(self, request, id):
        try:
            object = self.poll_model.objects.get(id=id)
            serializer = self.question_serializer(data=request.data)

            if serializer.is_valid(raise_exception=True):
                valid_data = serializer.validated_data
                valid_data['poll'] = object
                new_question = self.question_object(**valid_data)
                new_question.save()

                return Response(self.question_serializer(new_question).data)

        except self.poll_model.DoesNotExist:
            raise Http404
        except Exception as error:
            raise ParseError(error)


class AdminQuestionByIdMixin:
    """
    GET - Получение вопроса по id
    PATCH - Редактирование вопроса
    DELETE - Удаление вопроса
    """
    question_object = None
    question_serializer = None
    option_serializer = None

    def get(self, request, poll_id, question_id):
        try:
            object = self.question_object.objects.get(id=question_id)
            serializer = self.question_serializer(object).data

            if object.question_type:
                serializer['options'] = []
                for option in object.options_set.all():
                    options = self.option_serializer(option).data
                    serializer['options'].append(options)

            return Response(serializer)

        except self.question_object.DoesNotExist:
            raise Http404
        except Exception as error:
            raise ParseError(error)

    def patch(self, request, poll_id, question_id):
        try:
            object = self.question_object.objects.get(id=question_id)
            serializer = self.question_serializer(data=request.data)

            if serializer.is_valid(raise_exception=True):
                valid_data = serializer.validated_data
                object.type = valid_data['type']
                object.text = valid_data['text']
                object.save()

                return Response(self.question_serializer(object).data)

        except self.question_object.DoesNotExist:
            raise Http404
        except Exception as error:
            raise ParseError(error)

    def delete(self, request, poll_id, question_id):
        try:
            object = self.question_object.objects.get(id=question_id)
            object.delete()

            return Response(f'Question {object} was deleted!')

        except self.question_object.DoesNotExist:
            raise Http404
        except Exception as error:
            raise ParseError(error)


class AdminOptionsMixin:
    """
    GET - Получение списка вариантов ответа для вопроса
    POST - Создание нового варианта ответа
    """
    question_object = None
    option_object = None
    option_serializer = None

    def get(self, request, poll_id, question_id):
        object = self.option_object.objects.all()
        return Response(self.option_serializer(object, many=True).data)

    def post(self, request, poll_id, question_id):
        try:
            object = self.question_object.objects.get(id=question_id)
            serializer = self.option_serializer(data=request.data)
            if object.question_type:
                if serializer.is_valid(raise_exception=True):
                    valid_data = serializer.validated_data
                    valid_data['question'] = object
                    new_option = self.option_object(**valid_data)
                    new_option.save()

                    return Response(self.option_serializer(new_option).data)
            else:
                raise Exception('Invalid question type')

        except self.question_object.DoesNotExist:
            raise Http404
        except Exception as error:
            raise ParseError(error)


class AdminOptionsByIdMixin:
    """
    GET - Получение варианта ответа по id
    PATCH - Редактирование варианта ответа
    DELETE - Удаление варианта ответа
    """
    question_object = None
    option_object = None
    option_serializer = None

    def get(self, request, poll_id, question_id, option_id):
        try:
            object = self.option_object.objects.get(id=option_id)
            serializer = self.option_serializer(object).data

            return Response(serializer)

        except self.option_object.DoesNotExist:
            raise Http404
        except Exception as error:
            raise ParseError(error)

    def patch(self, request, poll_id, question_id, option_id):
        try:
            object = self.option_object.objects.get(id=option_id)
            serializer = self.option_serializer(data=request.data)

            if serializer.is_valid(raise_exception=True):
                valid_data = serializer.validated_data
                object.index = valid_data['index']
                object.text = valid_data['text']
                object.save()

                return Response(self.option_serializer(object).data)

        except self.option_object.DoesNotExist:
            raise Http404
        except Exception as error:
            raise ParseError(error)

    def delete(self, request, poll_id, question_id, option_id):
        try:
            object = self.option_object.objects.get(id=option_id)
            object.delete()

            return Response(f'Option {object} was deleted!')

        except self.option_object.DoesNotExist:
            raise Http404
        except Exception as error:
            raise ParseError(error)
