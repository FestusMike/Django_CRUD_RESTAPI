from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status, serializers
import datetime
from .models import UserData
from .serializers import UserDataSerializer
from django.shortcuts import get_object_or_404

@api_view(['GET', 'POST'])
def test(request):
    slack_name = request.query_params.get("slack name")
    stack = request.query_params.get("stack")
    today = datetime.datetime.utcnow().strftime('%A')
    utc_date_time = datetime.datetime.now().strftime('%Y:%m:%d %H:%M:%S')
    if not slack_name:
        return Response({'error': 'Kindly Provide your slack name'}, status=status.HTTP_400_BAD_REQUEST)
    if not stack:
        return Response({'error': 'Kindly Provide your stack, backend or frontend'}, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response(
            {
                'slack_name': slack_name,
                'stack': stack,
                'today': today,
                'date and time': utc_date_time
            },
            status=status.HTTP_200_OK
        )

@api_view(['POST'])
def add_users(request):
    users = UserDataSerializer(data=request.data)
    if UserData.objects.filter(**request.data).exists():
        raise serializers.ValidationError('User already exists')
    if users.is_valid():
        users.save()
        response_data = {
            'status' : status.HTTP_200_OK,
            'message' : 'User {} added successfully'.format(users.data['First_name']),
            'data' : users.data
        }
        return Response(response_data)

@api_view(['GET'])
def get_all_users(request):
    if request.query_params:
        data = UserData.objects.filter(**request.query_params.dict())
    else:
        data = UserData.objects.all()
    if data:
        serializer = UserDataSerializer(data, many=True)
        results = {
        "status" : status.HTTP_200_OK,
        "users retrieved" : "{} users retrieved".format(data.count()),
        "data" : serializer.data
            }
        return Response(results)
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def get_user_by_id(request, pk):
    user = UserData.objects.filter(pk=pk)
    if not user:
         raise serializers.ValidationError('User doesn\'t exist')        
    else:
        serializer = UserDataSerializer(user, many=True)
        results = {
        "status" : status.HTTP_200_OK,
        "users retrieved" : "{} user retrieved".format(user.count()),
        "data" : serializer.data
            }
        return Response(results)

@api_view(['PUT'])
def update_user(request, pk):
    user = UserData.objects.get(pk=pk)
    if not user:
        raise serializers.ValidationError('User doesn\'t exist') 
    serializer = UserDataSerializer(instance=user, data=request.data)
    if serializer.is_valid():
        serializer.save()
        results = {
            'message' : 'User\'s data edited successfully',
            'status' : status.HTTP_200_OK,
            'New data' : serializer.data
        }
        return Response(results)

@api_view(['DELETE'])
def delete_user(request, pk):
    user = get_object_or_404(UserData, pk=pk)
    user.delete()
    results = {
        "status" : status.HTTP_202_ACCEPTED,
        "message" : "User {} has been deleted succesfully".format(user.First_name)
    }
    return Response(results)