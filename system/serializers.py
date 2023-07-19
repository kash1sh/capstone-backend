from .models import Patient,Mentor,User,ScoreBoard
from rest_framework import serializers




class PatientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Patient
        fields = ['id','name','age','gender','dob']
        extra_kwargs = {
            'password' : {'write_only' : True}
        }

class MentorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Mentor
        fields = ['id','name','age','gender','specialization','experience','consultation_charges']
        extra_kwargs = {
            'password' : {'write_only' : True}
        }

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User 
        fields = ['username','email','is_patient','is_mentor']
        extra_kwargs = {
            'password' : {'write_only' : True} 
        }

class ScoreSerializer(serializers.ModelSerializer):
    class Meta: 
        model = ScoreBoard
        fields = '__all__'