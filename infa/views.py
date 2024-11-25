from django.shortcuts import render
from infa.serializers import UserSerializer,PostSerializer,CommentSerializer
from infa.models import Post
from rest_framework.views import APIView
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import authentication,permissions
from rest_framework.generics import CreateAPIView
from rest_framework import serializers
# Create your views here.

class SignUpApiView(APIView):
    serializer_class=UserSerializer
    def post(self,request,*args,**kwargs):
        serializer_instance=self.serializer_class(data=request.data)
        if serializer_instance.is_valid():
            serializer_instance.save()
            return Response(data=serializer_instance.data)
        return Response(data=serializer_instance.errors)

class PostViewSetView(ViewSet):

    serializer_class=PostSerializer
    authentication_classes=[authentication.TokenAuthentication]
    permission_classes=[permissions.IsAuthenticated]


    def list(self,request,*args,**kwargs):
        qs=Post.objects.all()
        serializer_instance=self.serializer_class(qs,many=True)
        return Response(data=serializer_instance.data)
    

    def create(self,request,*args,**kwargs):
        serializer_instance=self.serializer_class(data=request.data)
        if serializer_instance.is_valid():

            serializer_instance.save(owner=request.user) #integrity error not null constraint failed infa_models_post_owner
            return Response(data=serializer_instance.data)
        return Response(data=serializer_instance.errors)
    
    def retrieve(self,request,*args,**kwargs):
        id =kwargs.get('pk')
        qs=Post.objects.get(id=id)
        serializer_instance=self.serializer_class(qs)
        return Response(data=serializer_instance.data)
    
    def update(self,request,*args,**kwargs):
        id=kwargs.get('pk')
        post_object=Post.objects.get(id=id)
        serializer_instance=self.serializer_class(data=request.data,instance=post_object)
        if serializer_instance.is_valid():
            if not post_object.owner==request.user:
               raise serializers.ValidationError('Owner permission required')
                
            serializer_instance.save()
            return Response(data=serializer_instance.data)
        return Response(data=serializer_instance.errors)
    
    def destroy(self,request,*args,**kwargs):
        id=kwargs.get('pk')
        Post.objects.get(id=id).delete()
        return Response(data={'message':'deleted successfully'})


class CommentCreateView(CreateAPIView):
    serializer_class=CommentSerializer
    authentication_classes=[authentication.TokenAuthentication]
    permission_classes=[permissions.IsAuthenticated]

    def perform_create(self, serializer):
        id=self.kwargs.get('pk')
        post_obj=Post.objects.get(id=id)
        serializer.save(owner=self.request.user,post_object=post_obj)

class AddLikeView(APIView):
    authentication_classes=[authentication.TokenAuthentication]
    permission_classes=[permissions.IsAuthenticated]
    def post(self,request,*args,**kwargs):
        id=kwargs.get('pk')
        post_object=Post.objects.get(id=id)
        post_object.liked_by.add(request.user)
        return Response(data={'message':'liked'})