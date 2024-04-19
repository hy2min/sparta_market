from django.urls import path
from . import views

app_name = "products"
urlpatterns = [
    path("", views.list, name = "list"),
    path("<int:product_id>/", views.detail, name = "detail"),
    path("create/", views.create, name = "create"),
    path("update/<int:product_id>/", views.update, name = "update"),
    path("delete/<int:product_id>/", views.delete, name = "delete"),
    path("comments/<int:product_id>/", views.comment_create, name = "comment_create"),
    path("comments/<int:product_id>/delete/", views.comment_delete, name = "comment_delete"),
    
]

