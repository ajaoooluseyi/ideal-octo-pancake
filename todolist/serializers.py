from rest_framework import serializers
from .models import TodoItem

class TodoItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = TodoItem
        fields = '__all__'

    def validate_title(self, value):
        # Add validation logic for the title field
        if len(value) > 100:
            raise serializers.ValidationError("Title cannot exceed 100 characters.")
        return value

    def validate_description(self, value):
        # Add validation logic for the description field
        if len(value) > 1000:
            raise serializers.ValidationError("Description cannot exceed 1000 characters.")
        return value