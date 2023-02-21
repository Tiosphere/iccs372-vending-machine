from django.urls import path
from myapp import views

app_name = "myapp"

urlpatterns = [
    path("machine/", views.machine_views, name="machine"),
    path("machine/<int:id>/", views.machine_instance_view, name="machine_instance"),
    path("machine/<int:id>/log/", views.machine_log_view, name="machine_log"),
    path("snack/", views.snack_views, name="snack"),
    path("snack/<int:id>/", views.snack_instance_view, name="snack_instance"),
    path("snack/<int:id>/log/", views.snack_log_view, name="snack_log"),
    path("stock/<int:machine_id>/<int:snack_id>/", views.stock_view, name="stock"),
]
