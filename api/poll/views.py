from rest_framework.views import APIView
from rest_framework import authentication, permissions
from .serializers import *
from .models import *
from .admin_services import *
from .user_services import *


# ADMIN

class AdminAPIView(APIView):
    authentication_classes = [authentication.BasicAuthentication]
    permission_classes = [permissions.IsAdminUser]


class AdminPollList(AdminPollListMixin, AdminAPIView):
    poll_model = Poll
    poll_serializer = PollSerializers


class AdminPollById(AdminPollByIdMixin, AdminAPIView):
    poll_model = Poll
    poll_serializer = PollSerializers
    question_serializer = QuestionSerializers
    option_serializer = OptionsSerializers


class AdminQuestion(AdminQuestionMixin, AdminAPIView):
    poll_model = Poll
    question_object = Question
    question_serializer = QuestionSerializers


class AdminQuestionById(AdminQuestionByIdMixin, AdminAPIView):
    question_object = Question
    question_serializer = QuestionSerializers
    option_serializer = OptionsSerializers


class AdminOptions(AdminOptionsMixin, AdminAPIView):
    question_object = Question
    option_object = Options
    option_serializer = OptionsSerializers


class AdminOptionsById(AdminOptionsByIdMixin, AdminAPIView):
    question_object = Question
    option_object = Options
    option_serializer = OptionsSerializers


# USER

class PollList(PollListMixin, APIView):
    poll_model = Poll
    poll_serializer = PollSerializers


class PollById(PollByIdMixin, APIView):
    poll_model = Poll
    poll_serializer = PollSerializers
    question_serializer = QuestionSerializers
    option_serializer = OptionsSerializers
    answer_object = Answer
    user_answer_object = UserAnswer


class UserPoll(UserPollMixin, APIView):
    user_answer_object = UserAnswer
    user_answer_serializer = UserAnswerSerializers
