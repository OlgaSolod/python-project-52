from django.urls import path
from task_manager.user.views import UsersListView, CustomUpdateView, CustomDeleteView

urlpatterns = [
    path('', UsersListView.as_view(), name='users_list'),
    path('create/', RegisterView.as_view(), name='create'),
    path('<int:pk>/update/', CustomUpdateView.as_view(), name='update_user'),
    path('<int:pk>/delete/', CustomDeleteView.as_view(), name='delete_user')

]   
