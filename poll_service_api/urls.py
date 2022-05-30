from django.urls import path
from poll_service_api.views import VoteListView, QuestionListView


urlpatterns = [
    path('vote/', VoteListView.as_view()),
    path('vote/question/<int:pk>/', QuestionListView.as_view()),
]
