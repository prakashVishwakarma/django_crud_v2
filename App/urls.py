# api/urls.py

from django.urls import path
from .views import CreateTaskView, CreateTaskViewGetById, TaskDeleteView, UserProfileCurdView, UpdateUserProfile, \
    AuthorCreateView, OnlyAuthorCreateView, BookCreateView, GetAllAuthorsView, AuthorDetailByIdAPIView, UpdateBookView, \
    DeleteAuthorView, DeleteBookView, EnrollmentCreateView, EnrollmentGetByIdView

urlpatterns = [
    path('mymodel/', CreateTaskView.as_view(), name='mymodel'),
    path('getmymodel/', CreateTaskView.as_view(), name='getmymodel'),
    path('getbyid/<int:task_id>/', CreateTaskViewGetById.as_view(), name='getbyid'),
    path('tasks/<int:pk>/delete/', TaskDeleteView.as_view(), name='task-delete'),
    path('put/<int:pk>/', TaskDeleteView.as_view(), name='put'),
    # one_to_one
    path('create/', UserProfileCurdView.as_view(), name='create'),
    path('get_all/', UserProfileCurdView.as_view(), name='get_all'),
    path('get_by_id/<int:user_id>/', UserProfileCurdView.as_view(), name='get_by_id'),
    path('put_one_by_one/<int:user_id>/', UpdateUserProfile.as_view(), name='put'),
    # one_to_many POST
    path('post_one_to_many/', AuthorCreateView.as_view(), name='AuthorCreateView'),
    path('only_author_post_one_to_many/', OnlyAuthorCreateView.as_view(), name='OnlyAuthorCreateView'),
    path('only_book_post_one_to_many/<int:author_id>/', BookCreateView.as_view(), name='BookCreateView'),
    # one_to_many GET
    path('get_all_authors_one_to_many/', GetAllAuthorsView.as_view(), name='GetAllAuthorsView'),
    path('get_author_detail_by_id_one_to_many/<int:author_id>/', AuthorDetailByIdAPIView.as_view(), name='AuthorDetailByIdAPIView'),
    # one_to_many PUT
    path('update_book_one_to_many/<int:pk>/', UpdateBookView.as_view(), name='UpdateBookView'),
    # one_to_many DELETE
    path('delete_author_one_to_many/<int:pk>/', DeleteAuthorView.as_view(), name='DeleteAuthorView'),
    path('delete_book_one_to_many/<int:author_id>/<int:book_id>/', DeleteBookView.as_view(), name='DeleteBookView'),
    # many_to_many POST
    path('create_student_course_many_to_many/', EnrollmentCreateView.as_view(), name='EnrollmentCreateView'),
    path('get_student_course_many_to_many/', EnrollmentCreateView.as_view(), name='EnrollmentCreateViewGet'),
    path('get_student_course_many_to_many/<int:id>/', EnrollmentGetByIdView.as_view(), name='EnrollmentGetByIdView'),
    path('delete_student_course_many_to_many/<int:id>/', EnrollmentGetByIdView.as_view(), name='EnrollmentGetByIdView'),
    path('put_student_course_many_to_many/<int:id>/', EnrollmentGetByIdView.as_view(), name='EnrollmentGetByIdView'),
]
