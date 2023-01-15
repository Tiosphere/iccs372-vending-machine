from django.urls import path
from myapp import views


app_name = "myapp"

urlpatterns = [
    path("machine/", views.machine_views, name="machine"),
    path("machine/<int:id>/", views.machine_instance, name="machine_instance"),
    path("snack/", views.snack_views, name="snack"),
    path("snack/<int:id>/", views.snack_instance, name="snack_instance"),
]
