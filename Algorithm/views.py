from django.db import IntegrityError
from rest_framework.generics import ListAPIView, CreateAPIView, RetrieveAPIView
from rest_framework.permissions import IsAuthenticated, AllowAny

from .models import AlgorithmCategory, Algorithm, Comment, UserProgress
from .serializers import AlgorithmCategorySerializer, AlgorithmSerializer, CommentSerializer, UserProgressSerializer


class AlgorithmCategoryListAPIView(ListAPIView):
    queryset = AlgorithmCategory.objects.select_related('parent')
    serializer_class = AlgorithmCategorySerializer
    search_fields = ('name', 'parent__name')
    ordering_fields = ('name',)
    ordering = ('id',)


class AlgorithmCategoryAPIView(RetrieveAPIView):
    queryset = AlgorithmCategory.objects.select_related('parent')
    serializer_class = AlgorithmCategorySerializer
    lookup_field = 'slug'

    def retrieve(self, request, *args, **kwargs):
        response = super().retrieve(request, *args, **kwargs)

        response.data['children'] = self.get_serializer(
            instance=self.get_queryset().filter(parent__slug=kwargs.get('slug')),
            many=True
        ).data

        return response


class AlgorithmListAPIView(ListAPIView):
    queryset = Algorithm.objects.select_related('category')
    serializer_class = AlgorithmSerializer
    ordering_fields = ('name', 'category__name', 'created_at')
    ordering = ('-created_at',)
    search_fields = ('name', 'category__name')
    filterset_fields = ('category__slug',)


class AlgorithmAPIView(RetrieveAPIView):
    queryset = Algorithm.objects.select_related('category')
    serializer_class = AlgorithmSerializer
    lookup_field = 'slug'


class CommentListAPIView(ListAPIView, CreateAPIView):
    lookup_field = 'slug'
    queryset = Comment.objects.select_related('algorithm')
    serializer_class = CommentSerializer
    ordering_fields = ('created_at',)
    ordering = ('-created_at',)

    def get_permissions(self):
        if self.request.method == 'POST':
            return [IsAuthenticated()]
        return [AllowAny()]

    def get_queryset(self):
        return Comment.objects.filter(algorithm__slug=self.kwargs['slug'])

    def perform_create(self, serializer):
        algorithm = Algorithm.objects.get(slug=self.kwargs['slug'])
        serializer.save(user=self.request.user, algorithm=algorithm)


class UserProgressAPIView(RetrieveAPIView):
    serializer_class = UserProgressSerializer
    queryset = UserProgress.objects.all()
    permission_classes = [IsAuthenticated]
    lookup_url_kwarg = 'slug'
    lookup_field = 'algorithm__slug'


class UserProgressListCreateAPIView(ListAPIView, CreateAPIView):
    serializer_class = UserProgressSerializer
    queryset = UserProgress.objects.all()
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(user=self.request.user)

    def perform_create(self, serializer):
        try:
            algorithm = Algorithm.objects.get(slug=self.request.data.get('slug'))
            serializer.save(user=self.request.user, algorithm=algorithm)
        except IntegrityError:
            pass
