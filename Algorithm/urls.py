from django.urls import path

from .views import AlgorithmCategoryAPIView, AlgorithmCategoryListAPIView, AlgorithmListAPIView, AlgorithmAPIView, \
    CommentListAPIView, UserProgressAPIView, UserProgressListCreateAPIView

urlpatterns = [
    path('categories/', AlgorithmCategoryListAPIView.as_view()),
    path('categories/<slug:slug>/', AlgorithmCategoryAPIView.as_view()),
    path('', AlgorithmListAPIView.as_view()),
    path('learned/', UserProgressListCreateAPIView.as_view()),
    path('learned/<slug:slug>/', UserProgressAPIView.as_view()),
    path('<slug:slug>/', AlgorithmAPIView.as_view()),
    path('<slug:slug>/comments/', CommentListAPIView.as_view()),
]
