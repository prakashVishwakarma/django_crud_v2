from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views import View
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
import json

from rest_framework.generics import UpdateAPIView
from rest_framework.views import APIView
from .models import Task, CrudUser, UserProfile, Author, Book, Student, Course, Enrollment


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


    def get(self, request, user_id):
        # Get the CrudUser instance
        user = get_object_or_404(CrudUser, id=user_id)

        # Fetch associated UserProfile if it exists
        try:
            profile = user.userprofile
            profile_data = {
                'bio': profile.bio,
                'website': profile.website,
            }
        except UserProfile.DoesNotExist:
            profile_data = {
                'bio': None,
                'website': None,
            }

        # Manually construct the response
        response_data = {
            'username': user.username,
            'email': user.email,
            'profile': profile_data
        }

        return JsonResponse(response_data)

    def get(self, request):
        try:
            # Get all CrudUser instances
            users = CrudUser.objects.all()

            # Create a list to store user data
            users_data = []

            # Loop through all users and extract the needed information
            for user in users:
                # Get the associated user profile
                user_profile = user.userprofile

                # Create a dictionary for each user
                user_data = {
                    'id': user.id,
                    'username': user.username,
                    'email': user.email,
                    'profile': {
                        'bio': user_profile.bio,
                        'website': user_profile.website,
                    }
                }

                # Add the user data to the list
                users_data.append(user_data)

            # Return the list as JSON response
            return JsonResponse(users_data,safe=False )
        except Exception as e:
            # Error Response
            return JsonResponse({"error": str(e)}, status=400)

class UpdateUserProfile(UpdateAPIView):
    def put(self, request, user_id):
        try:
            # Get user by id
            user = CrudUser.objects.get(pk=user_id)
            user_profile = UserProfile.objects.get(user=user)

            # Get data from the request
            data = request.data

            # Update user fields
            user.username = data.get('username', user.username)
            user.email = data.get('email', user.email)
            user.save()

            # Update profile fields
            user_profile.bio = data.get('bio', user_profile.bio)
            user_profile.website = data.get('website', user_profile.website)
            user_profile.save()

            return JsonResponse({'message': 'User profile updated successfully'}, status=200)

        except CrudUser.DoesNotExist:
            return JsonResponse({'error': 'User not found'}, status=404)
        except UserProfile.DoesNotExist:
            return JsonResponse({'error': 'User profile not found'}, status=404)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)

@method_decorator(csrf_exempt, name='dispatch')
class AuthorCreateView(View):
    def post(self, request):
        try:
            # Parse the incoming JSON data
            data = json.loads(request.body)

            # Extract author details
            author_name = data.get('author_name')
            author_bio = data.get('author_bio')
            books = data.get('books', [])  # Get the list of books or default to an empty list

            # Check if author_name and books are provided
            if not author_name or not books:
                return JsonResponse({'error': 'Author name and books are required'}, status=400)

            # Create the Author
            author = Author.objects.create(name=author_name, bio=author_bio)

            # Create each book associated with the author
            for book_data in books:
                book_name = book_data.get('book_name')
                content = book_data.get('content')

                # Ensure both title and published_date are present for each book
                if book_name and content:
                    Book.objects.create(author=author, book_name=book_name, content=content)
                else:
                    return JsonResponse({'error': 'Each book must have a title and a published date'}, status=400)

            # Return a success response
            return JsonResponse({'message': 'Author and books created successfully'}, status=201)

        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)

@method_decorator(csrf_exempt, name='dispatch')
class OnlyAuthorCreateView(View):
    def post(self, request, *args, **kwargs):
        try:
            # Parse the incoming JSON data
            data = json.loads(request.body)

            # Extract author details
            author_name = data.get('author_name')
            author_bio = data.get('author_bio')

            # Validate that required fields are present
            if not author_name:
                return JsonResponse({'error': 'Author name is required'}, status=400)

            # Create the Author
            author = Author.objects.create(name=author_name, bio=author_bio)

            # Return a success response
            return JsonResponse({
                'message': 'Author created successfully',
                'author': {
                    'id': author.id,
                    'name': author.name,
                    'bio': author.bio
                }
            }, status=201)

        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)


@method_decorator(csrf_exempt, name='dispatch')
class BookCreateView(View):
    def post(self, request, author_id):
        try:
            # Find the author by ID
            try:
                author = Author.objects.get(id=author_id)
            except Author.DoesNotExist:
                return JsonResponse({'error': 'Author not found'}, status=404)

            # Parse the incoming JSON data
            data = json.loads(request.body)
            book_list = []

            for book_data in data:
                book_name = book_data.get('book_name')
                content = book_data.get('content')

                # Ensure both book_name and content are present for each book
                if book_name and content:
                    book = Book.objects.create(author=author, book_name=book_name, content=content)

                    # Collect book details for the response
                    book_dict = {
                        'author_id': book.author.id,  # Use author id or name instead of the whole object
                        'author_name': book.author.name,
                        'book_name': book.book_name,
                        'content': book.content,
                    }
                    book_list.append(book_dict)

                else:
                    return JsonResponse({'error': 'Each book must have a book name and content'}, status=400)

            # Return a success response with the created book list
            return JsonResponse({
                'message': 'Books created successfully',
                'books': book_list
            }, status=201)

        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)

class GetAllAuthorsView(APIView):
    def get(self, request):
        try:
            # Query all authors
            authors = Author.objects.all()

            # Create a list to store the response
            data = []

            for author in authors:
                # For each author, get their books
                books = Book.objects.filter(author=author)

                # Create a list to store the books for each author
                books_list = []

                for book in books:
                    # Append each book's details to the books_list
                    books_list.append({
                        "id": book.id,
                        "book_name": book.book_name,
                        "content": book.content,
                        "created_at": book.created_at
                    })

                # Construct the author and books information
                author_data = {
                    "id": author.id,
                    "author_name": author.name,
                    "bio": author.bio,
                    "books": books_list
                }

                # Append the author data to the response list
                data.append(author_data)
            # Return the response as JSON
            return JsonResponse(data, safe=False)

        except Exception as e:
            # Error Response
            return JsonResponse({"error": str(e)}, status=400)


class AuthorDetailByIdAPIView(APIView):
    def get(self, request, author_id):
        # Get the author by ID or return a 404 if not found
        author = get_object_or_404(Author, id=author_id)

        # Get all books for the specified author
        books = Book.objects.filter(author=author)

        # Create a list to store the books for the author
        books_list = []

        for book in books:
            # Append each book's details to the books_list
            books_list.append({
                "book_name": book.book_name,
                "content": book.content,
                "created_at": book.created_at
            })

        # Construct the author and books information
        author_data = {
            "author_name": author.name,
            "bio": author.bio,
            "books": books_list
        }

        # Return the response as JSON
        return JsonResponse(author_data, safe=False)


@method_decorator(csrf_exempt, name='dispatch')  # To exempt CSRF for testing purposes, not recommended for production
class UpdateBookView(View):

    def put(self, request, pk):
        try:
            book = Book.objects.get(pk=pk)
        except Book.DoesNotExist:
            return JsonResponse({'error': 'Book not found'}, status=404)

        # Parse the request body
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)

        # Update book details
        book_name = data.get('book_name')
        content = data.get('content')
        author_id = data.get('author_id')

        if book_name:
            book.book_name = book_name
        if content:
            book.content = content
        if author_id:
            try:
                author = Author.objects.get(pk=author_id)
                book.author = author
            except Author.DoesNotExist:
                return JsonResponse({'error': 'Author not found'}, status=404)

        # Save the updated book
        book.save()

        return JsonResponse({
            'message': 'Book updated successfully',
            'book': {
                'id': book.id,
                'book_name': book.book_name,
                'content': book.content,
                'author': book.author.name,
                'created_at': book.created_at
            }
        }, status=200)

@method_decorator(csrf_exempt, name='dispatch')  # Exempt CSRF for testing purposes
class DeleteAuthorView(View):

    def delete(self, request, pk):
        try:
            # Fetch the author instance by primary key
            author = Author.objects.get(pk=pk)
        except Author.DoesNotExist:
            return JsonResponse({'error': 'Author not found'}, status=404)

        # Delete the author, which will also delete all related books due to CASCADE
        author.delete()

        return JsonResponse({'message': 'Author and all related books deleted successfully'}, status=200)

@method_decorator(csrf_exempt, name='dispatch')  # Exempt CSRF for testing purposes
class DeleteBookView(View):

    def delete(self, request, author_id, book_id):
        try:
            # Fetch the book instance by book_id and author_id
            book = Book.objects.get(pk=book_id, author_id=author_id)
        except Book.DoesNotExist:
            return JsonResponse({'error': 'Book not found for this author'}, status=404)

        # Delete the book instance
        book.delete()

        return JsonResponse({'message': 'Book deleted successfully'}, status=200)

@method_decorator(csrf_exempt, name='dispatch')
class EnrollmentCreateView(View):
    def post(self, request):
        data = json.loads(request.body)
        student_data = data.get("student")
        course_data = data.get("course")
        grade = data.get("grade")

        # Check if the student exists; create if not
        student = Student.objects.filter(
            name=student_data["name"],
            email=student_data["email"]
        ).first()
        if not student:
            student = Student.objects.create(
                name=student_data["name"],
                email=student_data["email"]
            )

        # Check if the course exists; create if not
        course = Course.objects.filter(
            title=course_data["title"],
            description=course_data["description"],
            start_date=course_data["start_date"]
        ).first()
        if not course:
            course = Course.objects.create(
                title=course_data["title"],
                description=course_data["description"],
                start_date=course_data["start_date"]
            )

        # Check if the enrollment exists; create if not
        enrollment = Enrollment.objects.filter(student=student, course=course).first()
        if not enrollment:
            enrollment = Enrollment.objects.create(
                student=student,
                course=course,
                grade=grade
            )
            response = {
                "message": "Enrollment created successfully",
                "student": student.name,
                "course": course.title,
                "enrollment_date": enrollment.enrollment_date,
                "grade": enrollment.grade,
            }
            return JsonResponse(response, status=201)
        else:
            return JsonResponse({"message": "Enrollment already exists"}, status=400)

    def get(self, request):
        # Get all enrollment records
        enrollments = Enrollment.objects.all()

        # Format enrollment data into the specified structure
        enrollment_data = []
        for enrollment in enrollments:
            enrollment_data.append({
                "student": {
                    "id": enrollment.student.id,
                    "name": enrollment.student.name,
                    "email": enrollment.student.email,
                },
                "course": {
                    "id": enrollment.course.id,
                    "title": enrollment.course.title,
                    "description": enrollment.course.description,
                    "start_date": enrollment.course.start_date,
                },
                "grade": enrollment.grade,
                "id": enrollment.id,
            })

        # Return data as JSON response
        return JsonResponse(enrollment_data, safe=False)

class EnrollmentGetByIdView(APIView):
    def get(self, request, id):
        try:
            # Retrieve the specific enrollment by ID
            enrollment = Enrollment.objects.get(id=id)

            # Structure the response data
            enrollment_data = {
                "student": {
                    "name": enrollment.student.name,
                    "email": enrollment.student.email,
                },
                "course": {
                    "title": enrollment.course.title,
                    "description": enrollment.course.description,
                    "start_date": enrollment.course.start_date,
                },
                "grade": enrollment.grade,
            }

            # Return data as JSON response
            return JsonResponse(enrollment_data, status=200)
        except Enrollment.DoesNotExist:
            # Return a 404 error if the enrollment is not found
            return JsonResponse({"error": "Enrollment not found"}, status=404)

    def delete(self, request, id):
        try:
            # Retrieve and delete the specific enrollment by ID
            enrollment = Enrollment.objects.get(id=id)
            enrollment.delete()

            # Return a success response
            return JsonResponse({"message": "Enrollment deleted successfully"}, status=200)
        except Enrollment.DoesNotExist:
            # Return a 404 error if the enrollment is not found
            return JsonResponse({"error": "Enrollment not found"}, status=404)

    def put(self, request, id):
        try:
            enrollment = Enrollment.objects.get(id=id)
            data = json.loads(request.body)

            # Update student information if provided
            student_data = data.get("student")
            if student_data:
                enrollment.student.name = student_data.get("name", enrollment.student.name)
                enrollment.student.email = student_data.get("email", enrollment.student.email)
                enrollment.student.save()

            # Update course information if provided
            course_data = data.get("course")
            if course_data:
                enrollment.course.title = course_data.get("title", enrollment.course.title)
                enrollment.course.description = course_data.get("description", enrollment.course.description)
                enrollment.course.start_date = course_data.get("start_date", enrollment.course.start_date)
                enrollment.course.save()

            # Update grade if provided
            grade = data.get("grade")
            if grade:
                enrollment.grade = grade

            enrollment.save()

            # Prepare the response data in the specified format
            updated_data = {
                "student": {
                    "name": enrollment.student.name,
                    "email": enrollment.student.email,
                },
                "course": {
                    "title": enrollment.course.title,
                    "description": enrollment.course.description,
                    "start_date": enrollment.course.start_date,
                },
                "grade": enrollment.grade,
            }
            return JsonResponse(updated_data, status=200)
        except Enrollment.DoesNotExist:
            return JsonResponse({"error": "Enrollment not found"}, status=404)