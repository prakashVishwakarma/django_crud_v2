from django.http import JsonResponse
from django.views import View
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
import json

from rest_framework.views import APIView

from .models import Task, CrudUser, UserProfile


@method_decorator(csrf_exempt, name='dispatch')
class CreateTaskView(APIView):
    def post(self, request, *args, **kwargs):
        try:
            # Parse the JSON request body
            data = json.loads(request.body)
            title = data.get('title')
            description = data.get('description')

            # Validate data
            if not title or not description:
                return JsonResponse({'error': 'Title and description are required.'}, status=400)

            # Create a new task
            task = Task.objects.create(title=title, description=description)

            # Respond with the created task's ID and message
            return JsonResponse({
                'message': 'Task created successfully!',
                'task_id': task.id
            }, status=201)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON format.'}, status=400)

    def get(self, request):
        # Fetch all tasks from the database
        tasks = Task.objects.all()

        # Prepare the data without using a serializer
        task_list = []
        for task in tasks:
            task_list.append({
                'id': task.id,
                'title': task.title,
                'description': task.description,
                'created_at': task.created_at.strftime('%Y-%m-%d %H:%M:%S')  # Format datetime
            })
        # Check if there are no tasks in the database
        if not tasks.exists():
            return JsonResponse({'message': 'No tasks found'}, status=200)

        # Return a Response with the list of tasks
        return JsonResponse(task_list, safe=False)

class CreateTaskViewGetById(View):

    def get(self, request, task_id):
        try:
            # Fetch task by ID or raise 404 if not found
            task = Task.objects.get(id=task_id)
        except Task.DoesNotExist:
            # Return custom 404 response when the task is not found
            return JsonResponse({'error': f'Task with id {task_id} not found'}, status=404)

        # Prepare the response manually without using a serializer
        task_data = {
            'id': task.id,
            'title': task.title,
            'description': task.description,
            'created_at': task.created_at.strftime('%Y-%m-%d %H:%M:%S')  # Format datetime
        }

        # Return the task data as JSON
        return JsonResponse(task_data, status=200)

# Delete task by ID
class TaskDeleteView(APIView):
    def delete(self, request, pk):
        try:
            task = Task.objects.get(pk=pk)
            task.delete()
            return JsonResponse({'message': 'Task deleted successfully'}, status=200)
        except Task.DoesNotExist:
            return JsonResponse({'error': 'Task not found'}, status=404)

    def put(self, request, pk):
        try:
            # Get the task by primary key
            task = Task.objects.get(pk=pk)

            # Parse the incoming JSON data
            body_unicode = request.body.decode('utf-8')
            body_data = json.loads(body_unicode)

            # Update task fields
            title = body_data.get('title', task.title)
            description = body_data.get('description', task.description)

            task.title = title
            task.description = description
            task.save()  # Save the updated task

            # Return success response
            return JsonResponse({
                'message': 'Task updated successfully',
                'task': {
                    'id': task.id,
                    'title': task.title,
                    'description': task.description,
                    'created_at': task.created_at
                }
            }, status=200)

        except Task.DoesNotExist:
            return JsonResponse({'error': 'Task not found'}, status=404)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)


@method_decorator(csrf_exempt, name='dispatch')
class UserProfileCurdView(View):
    def post(self, request, *args, **kwargs):
        try:
            # Parse JSON data
            data = json.loads(request.body)
            username = data.get('username')
            email = data.get('email')
            bio = data.get('bio')
            website = data.get('website')

            # Create the User
            user = CrudUser.objects.create(username=username, email=email)

            # Create the UserProfile
            user_profile = UserProfile.objects.create(user=user, bio=bio, website=website)

            # Success Response
            return JsonResponse({
                "message": "User and Profile created successfully",
                "user_id": user.id,
                "profile_id": user_profile.id
            }, status=201)

        except Exception as e:
            # Error Response
            return JsonResponse({"error": str(e)}, status=400)