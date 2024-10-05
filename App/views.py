from django.http import JsonResponse
from django.views import View
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
import json
from .models import Task

@method_decorator(csrf_exempt, name='dispatch')
class CreateTaskView(View):
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
