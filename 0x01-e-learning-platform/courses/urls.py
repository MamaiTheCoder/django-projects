from django.urls import path
from . import views


urlpatterns = [
    path(
        'mine/',
        views.ManageCourseListView.as_view(),
        name='manage_course_list'
    ),
    path(
        'create/',
        views.CourseCreateView.as_view(),
        name='course_create'
    ),
    path(
        '<pk>/edit/',
        views.CourseUpdateView.as_view(),
        name='course_edit'
    ),
    path(
        '<pk>/delete/',
        views.CourseDeleteView.as_view(),
        name='course_delete'
    ),
    path(
        '<pk>/module',
        views.CourseModuleUpdateView.as_view(),
        name='course_module_update'
    ),
    # Create new text, video, image, or file objects
    # and add them to a module.
    path(
        'module/<int:module_id>/content/<model_name>/create/',
        views.ContentCreateUpdateView.as_view(),
        name='module_content_create'
    ),
    # Update an existing text, video, image, or file object.
    path(
        'module/<int:module_id>/content/<model_name>/<id>/s',
        views.ContentCreateUpdateView.as_view(),
        name='module_content_update'
    ),
    path(
        'content/<int:id>/delete/',
        views.ContentDeleteview.as_view(),
        name='module_content_delete'
    ),
    path(
        'module/<int:module_id>/',
        views.ManageCourseListView.as_view(),
        name='module_content_list'
    ),
]