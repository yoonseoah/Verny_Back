from rest_framework import serializers
from .models import *

# class LikeSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Like
#         fields = ("user",)


class RecommentSerializer(serializers.ModelSerializer):
    # recomment_like = LikeSerializer(many=True, read_only=True)
    relikes_count = serializers.SerializerMethodField()

    class Meta:
        model = Recomment
        fields = (
            "id",
            "author",
            "created_at",
            "content",
            "relikes",
            "relikes_count",
        )

    def get_relikes_count(self, obj):
        return obj.relikes.count()


class CommentSerializer(serializers.ModelSerializer):
    # comment_like = LikeSerializer(many=True, read_only=True)
    likes_count = serializers.SerializerMethodField()
    recomments = RecommentSerializer(many=True, read_only=True)

    class Meta:
        model = Comment
        fields = [
            "id",
            "post",
            "author",
            "content",
            "created_at",
            "likes",
            "likes_count",
            "recomments",
        ]

    def get_likes_count(self, obj):
        return obj.likes.count()


class PostSerializer(serializers.ModelSerializer):
    # comment = CommentSerializer(many=True, read_only=True)
    scraps_count = serializers.SerializerMethodField()
    comment_count = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = [
            "id",
            "title",
            "painter",
            # "drawing_technique",
            # "work_year",
            # "content",
            # "type_choices",
            # "type",
            # "scraps",
            "scraps_count",
            # "created_at",
            # "comment",
            "comment_count",
        ]

    def get_scraps_count(self, obj):
        return obj.scraps.count()

    def get_comment_count(self, obj):
        return obj.comment.count()


class PosDetailSerializer(serializers.ModelSerializer):
    # comment = CommentSerializer(many=True, read_only=True)
    scraps_count = serializers.SerializerMethodField()
    comment_count = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = [
            # "id",
            "content",
            "title",
            "painter",
            "drawing_technique",
            "work_year",
            # "type_choices",
            "type",
            "scraps",
            "scraps_count",
            "created_at",
            # "comment",
            "comment_count",
        ]

    def get_scraps_count(self, obj):
        return obj.scraps.count()

    def get_comment_count(self, obj):
        return obj.comment.count()
