from django.shortcuts import render
from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Post
from .serializers import PostSerializer, UploadCsvSerializer


class PostView(APIView):
    def get(self, request):
        id = request.query_params.get('id', None)
        if id:
            try:
                post = Post.objects.get(id=id)
                serializer = PostSerializer(post)
                return Response(serializer.data)
            except Post.DoesNotExist:
                raise ValidationError({"detail": 'No Post Found against id'})
        else:
            post = Post.objects.all()
            serializer = PostSerializer(post, many=True)
            return Response(serializer.data)

    def post(self, request):
        serializer = PostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request):
        id = request.data.get('id')
        obj = Post.objects.filter(id=id).first()
        if obj is not None:
            post = Post.objects.filter(id=id).first()
        else:
            return Response({'detail': ' Post Does not Exists!'})
        serializer = PostSerializer(post, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def delete(self, request):
        id = request.query_params.get('id')
        post = Post.objects.filter(id=id).first()
        if post:
            post.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response({'Detail': 'Post Already Deleted!'})


class UploadCSV(APIView):
    def post(self, request):
        serializer = UploadCsvSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return  Response({'detail': 'uploaded!'})
