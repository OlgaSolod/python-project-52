from django.urls import path
from task_manager.task.views import TasksListView, CreateTaskView, UpdateTaskView, DeleteTaskView

urlpatterns = [
    path('', TasksListView.as_view(), name='tasks_list'),
    path('create/', CreateTaskView.as_view(), name='create_task'),
    path('<int:pk>/update/', UpdateTaskView.as_view(), name='update_task'),
    path('<int:pk>/delete/', DeleteTaskView.as_view(), name='delete_task')
]   