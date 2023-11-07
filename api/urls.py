from django.urls import path

from . import views

#app_name = 'polls'
urlpatterns = [
    path("test/", views.test),
    path("get/", views.get_all_users, name="get_all_users"),
    path("add/", views.add_users, name="add_users"),
    path("get/<int:pk>/", views.get_user_by_id, name="Get_User_By_Id"),
    path("update/<int:pk>/", views.update_user, name="Update_User"),
    path("delete/<int:pk>/", views.delete_user, name="Delete_User"),
]