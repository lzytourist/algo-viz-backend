from rest_framework import serializers

from Algorithm.models import AlgorithmCategory, Algorithm, Comment, UserProgress


class AlgorithmCategorySerializer(serializers.ModelSerializer):
    parent = serializers.SerializerMethodField()

    class Meta:
        model = AlgorithmCategory
        exclude = ('id',)

    @staticmethod
    def get_parent(obj):
        if obj.parent:
            return AlgorithmCategorySerializer(obj.parent).data
        return None


class AlgorithmSerializer(serializers.ModelSerializer):
    category = AlgorithmCategorySerializer(read_only=True)

    class Meta:
        model = Algorithm
        exclude = ('id',)


class CommentSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        exclude = ('id', 'algorithm')
        read_only_fields = ('user', 'algorithm')

    @staticmethod
    def get_user(obj):
        return f"{obj.user.first_name} {obj.user.last_name}"


class UserProgressAlgorithmSerializer(serializers.ModelSerializer):
    category = AlgorithmCategorySerializer(read_only=True)

    class Meta:
        model = Algorithm
        fields = ('name', 'slug', 'category')
        depth = 1


class UserProgressSerializer(serializers.ModelSerializer):
    topic = UserProgressAlgorithmSerializer(read_only=True, source='algorithm')

    def validate(self, attrs):
        slug = self.context['request'].data.get('slug')
        print(slug)
        if not slug:
            raise serializers.ValidationError('Slug is required')
        if not Algorithm.objects.filter(slug=slug).exists():
            raise serializers.ValidationError('Algorithm does not exist')
        return attrs

    class Meta:
        model = UserProgress
        exclude = ('id',)
        read_only_fields = ('user', 'algorithm')
