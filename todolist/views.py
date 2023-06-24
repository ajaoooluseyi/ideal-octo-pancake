from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions
from .models import TodoItem
from .serializers import TodoItemSerializer

# Create your views here.
class TodoListApiView(APIView):
    permission = [permissions.IsAuthenticated]

    # Read all todo items 
    def get(self, request, *args, **kwargs):
        todos = TodoItem.objects.all() 
        serializer = TodoItemSerializer(todos, many = True)
        return Response(serializer.data, status = status.HTTP_200_OK)


    # Create a todo item
    def post(self, request, *args, **kwargs):
        data = {
            'title': request.data.get('title'),
            'description' : request.data.get('description'),
            'due_date': request.data.get('due_date'),
            'tags': request.data.get('tags'),
            'status':request.data.get('status'),
        }

        serializer =  TodoItemSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status = status.HTTP_201_CREATED)

        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)


class TodoDetailApiView(APIView):
    permission = [permissions.IsAuthenticated]

    def object(self, todo_id):
        try:
            return TodoItem.objects.get(id=todo_id)
        except TodoItem.DoesNotExist:
            return None

    # Read one todo item
    def get(self, request, todo_id):
        todo_instance = self.object(todo_id)
        if not todo_instance:
            return Response(
                {'res':'Object does not exist'},
                status = status.HTTP_400_BAD_REQUEST
            )
        serializer = TodoItemSerializer(todo_instance)
        return Response(serializer.data, status = status.HTTP_200_OK)

    # Update a todo item
    def put(self, request, todo_id):
        todo_instance = self.object(todo_id)
        if not todo_instance:
            return Response(
                {'res':'Object does not exist'},
                status = status.HTTP_400_BAD_REQUEST
            )
        data = {
            'title': request.data.get('title'),
            'description' : request.data.get('description'),
            'due_date': request.data.get('due_date'),
            'tags': request.data.get('tags'),
            'status':request.data.get('status'),
        }

        serializer = TodoItemSerializer(instance = todo_instance, data = data, partial = True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status = status.HTTP_201_CREATED)

        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)

    #Delete a todo item
    def delete(self, request, todo_id):
        todo_instance = TodoItem.objects.get(id=todo_id)
        if not todo_instance:
            return Response(
                {'message':'Object does not exist'},
                status = status.HTTP_400_BAD_REQUEST
            )
        todo_instance.delete()
        return Response(
            {'message':'Object deleted!'},
            status = status.HTTP_200_OK
        )

