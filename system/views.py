from django.http import HttpResponse
from django.contrib.auth.hashers import make_password

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view
from .read_test import get_final_answer
from .speech_to_text import speech_to_text

from .serializers import PatientSerializer,MentorSerializer,UserSerializer,ScoreSerializer
from .models import Patient,Mentor,ScoreBoard
from difflib import SequenceMatcher

import base64


def similar(a, b):
    return SequenceMatcher(None, a, b).ratio()

# Create your views here.
def index(request):
    return HttpResponse("Server Working!!!")

class UserRegistrationView(APIView):
    # Edit Doctor Serializers and Patient Serializers for Validation
    def post(self, request):
        user_serializer = UserSerializer(data = request.data)
        if request.data.get('password') is None: 
            return Response({"message" : "Password Missing!!"},status = status.HTTP_400_BAD_REQUEST)
        password = request.data['password']
        password = make_password(password = password)

        if user_serializer.is_valid():
            if request.data.get("is_patient") is True: 
                parent_serializer = PatientSerializer(data = request.data)
            elif request.data.get("is_mentor") is True: 
                parent_serializer = MentorSerializer(data = request.data)
            else: 
                return Response({"message" : "Type of User in Request Missing"},status = status.HTTP_400_BAD_REQUEST)
            

            if parent_serializer.is_valid():
                if request.data.get("is_patient") is True: 
                    user = user_serializer.save(password = password)
                    parent_serializer.save(patient = user)
                    return Response(parent_serializer.data, status = status.HTTP_201_CREATED)
                else: 
                    user = user_serializer.save(password = password)
                    parent_serializer.save(mentor = user)
                    return Response(parent_serializer.data, status = status.HTTP_201_CREATED)
            else: 
                return Response(parent_serializer.errors, status = status.HTTP_400_BAD_REQUEST)

        else: 
            return Response(user_serializer.errors, status = status.HTTP_400_BAD_REQUEST)

class SpecificPatientView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def get(self, request):
        user = self.request.user 
        if user.is_patient:
            patient = Patient.objects.get(patient = user)
            serializer = PatientSerializer(patient)
            return Response(serializer.data, status = status.HTTP_200_OK)
        
        elif user.is_mentor:
            if request.data.get("id") is None: 
                return Response({"message" : "Patient ID is required"},status = status.HTTP_400_BAD_REQUEST)
            try:
                patient = Patient.objects.get(id = request.data.get("id"))
                serializer = PatientSerializer(patient)
                return Response(serializer.data, status = status.HTTP_200_OK)
            except: 
                return Response({
                    "message" : "Invalid Patient ID"
                },status = status.HTTP_404_NOT_FOUND)
            
        return Response({
            "message" : "User not Authorized!!"
        },status = status.HTTP_401_UNAUTHORIZED)

class SpecificMentorView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def get(self, request):
        user = self.request.user 
        if user.is_mentor:
            mentor = Mentor.objects.get(mentor = user)
            serializer = MentorSerializer(mentor)
            return Response(serializer.data, status = status.HTTP_200_OK)
        
        elif user.is_patient:
            if request.data.get("id") is None: 
                return Response({"message" : "Doctor ID is required"},status = status.HTTP_400_BAD_REQUEST)
            try:
                patient = Mentor.objects.get(id = request.data.get("id"))
                serializer = MentorSerializer(patient)
                return Response(serializer.data, status = status.HTTP_200_OK)
            except: 
                return Response({
                    "message" : "Invalid Patient ID"
                },status = status.HTTP_404_NOT_FOUND)
            
        return Response({
            "message" : "User not Authorized!!"
        },status = status.HTTP_401_UNAUTHORIZED)

class ScoreBoardView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def get(self, request):
        user = self.request.user 
    
        if request.GET["type"] not in ["Rapid Color Naming","Reading Comprehension Test","Handwriting Recognition Test","Object Classification Test"]: 
            return Response({"message" : "Type Misssing!!"},status = status.HTTP_400_BAD_REQUEST)

        if user.is_patient: 
            patient = Patient.objects.get(patient = user)
            score_data = ScoreBoard.objects.filter(patient = patient,type_of_test = request.GET["type"])
            serializer = ScoreSerializer(score_data,many = True)
            return Response(serializer.data, status = status.HTTP_200_OK)
        elif user.is_mentor: 
            if request.data.get("id") is None : 
                return Response({"message" : "Patient ID is required"},status = status.HTTP_400_BAD_REQUEST)
            else: 
                try:
                    patient = Patient.objects.get(id = request.data.get("id"))
                    score_data = ScoreBoard.objects.filter(patient = patient,type_of_test = request.GET["type"])
                    serializer = ScoreSerializer(score_data,many = True)
                    return Response(serializer.data, status = status.HTTP_200_OK)
                except:
                    return Response({"message" : "Patient Not Found in the database"},status = status.HTTP_400_BAD_REQUEST)
            
        else: 
            return Response({"message" : "You are not Authorized to view this page"},status = status.HTTP_401_UNAUTHORIZED)

    def post(self, request):
        user = self.request.user
        if user.is_patient: 
            request.data.update({'patient' : Patient.objects.get(patient = user).id})
            serializer = ScoreSerializer(data = request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status = status.HTTP_200_OK)
            else: 
                return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)
        return Response({"message" : "Only Patient can add score"},status = status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def get_read_score(request):
    if request.data.get("text") is None: 
        return Response({
            "message" : "Reference Text not Specified"
        },status = status.HTTP_400_BAD_REQUEST)
    elif request.data.get("audio") is None:
        return Response({
            "message" : "Audio file is missing"
        })

    return Response(get_final_answer(request.data.get("text"),
    request.data.get("audio")),status = status.HTTP_200_OK)

@api_view(['POST'])
def rapid_color_naming(request):
    if request.data.get("reference") is None: 
        return Response({
            "message" : "Reference Text is Missing !!! "
        })
    if request.data.get("audio") is None: 
     
        
        return Response({
            "message" : "Audio File is missing"
        },status = status.HTTP_400_BAD_REQUEST)
    message = speech_to_text(request.data.get("audio"))["DisplayText"]
    get_string_key = ''.join([elem[0].upper() for elem in message.split()])

    return Response({
        "score" : similar(request.data.get("reference"),get_string_key)
    },status = status.HTTP_200_OK)



