from rest_framework import serializers
from .models import *


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ["id", "post", "author", "content", "created_at"]


class PostSerializer(serializers.ModelSerializer):
    comment = CommentSerializer(many=True, read_only=True)
    scraps_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Post
        fields = [ 
            "id",
            "title",
            "painter",
            "drawing_technique",
            "work_year",
            "content",
            "type_choices",
            "type",
            "scraps",
            "scraps_count",
            "comment",
            
        ]
    def get_scraps_count(self, obj):
        return obj.scraps.count()
