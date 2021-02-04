from django.urls import path
from .views import *


urlpatterns = [
    # ADMIN
    path('admin/api/polls', AdminPollList.as_view()),
    path('admin/api/polls/<int:id>', AdminPollById.as_view()),
    path('admin/api/polls/<int:id>/questions', AdminQuestion.as_view()),
    path('admin/api/polls/<int:poll_id>/questions/<question_id>', AdminQuestionById.as_view()),
    path('admin/api/polls/<int:poll_id>/questions/<int:question_id>/options', AdminOptions.as_view()),
    path('admin/api/polls/<int:poll_id>/questions/<question_id>/options/<int:option_id>', AdminOptionsById.as_view()),

    # USER
    path('api/polls', PollList.as_view()),
    path('api/polls/<int:id>', PollById.as_view()),
    path('api/user/answer/<int:id>', UserPoll.as_view()),

]
