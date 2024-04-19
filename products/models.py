from django.db import models
from django.conf import settings


class Product(models.Model) :
    title = models.CharField(max_length=255)
    content = models.TextField()
    price = models.PositiveIntegerField()
    image = models.ImageField(upload_to="image/",blank=True)

    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name = "products", null=True
    )
    
    def __str__(self):
        return self.title
    

class Comment(models.Model) :
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="comments"
        )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE ,related_name="comments", null=True
    )
    content = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) :
        return self.content
