"""
Both processes are defined in objects referred to as serializers.
DRF offers developers with a convenient class to create serializers
for Django models easily, so we have to provide only some basic information such
as the model that will be served in the serializer and
the fields to which we want to give access.
"""

from rest_framework import serializers
from . import models
from django.contrib.auth.models import User

class ExamSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Exam
        fields = "__all__"


class QuestionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Questions
        fields = "__all__"


class OptionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Options
        fields = "__all__"


class CandidateSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Candidate
        fields = "__all__"



class CandidateResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.CandidateResponse
        fields = "__all__"



#for the oautho2
class CreateUserSerializer(serializers.ModelSerializer):

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user

    class Meta:
        model = User
        fields = ('id', 'username', 'password')
        extra_kwargs = {
            'password': {'write_only': True}
        }
