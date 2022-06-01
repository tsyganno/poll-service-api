from django.urls import path
from poll_service_api.views import VoteListView, QuestionListView, QuestionView, AnswerCreateView, ResultsListView, login


urlpatterns = [
    path('login/', login, name='login'),
    path('votes/', VoteListView.as_view(), name='votes'),
    path('votes/<int:vote_pk>/questions/', QuestionListView.as_view(), name='questions'),
    path('votes/question/<int:question_pk>/', QuestionView.as_view(), name='question'),
    path('votes/answer/<int:question_pk>/', AnswerCreateView.as_view(), name='question'),
    path('votes/results/user/', ResultsListView.as_view(), name='results'),
]
