from django.db import models
image = models.ImageField(
    upload_to="paintings/",
    default="paintings/default.jpg"
)

class Painting(models.Model):
    title = models.CharField("نام اثر", max_length=200)
    artist_name = models.CharField("نام هنری", max_length=200, default="")  # برای اینکه migration گیر نده
    description = models.TextField("توضیح اثر", blank=True)
    year_created = models.CharField("سال خلق", max_length=10, blank=True)
    image = models.ImageField("عکس اثر", upload_to="paintings/")
    is_available = models.BooleanField("نمایش داده شود", default=True)

    def __str__(self):
        return f"{self.title} - {self.artist_name}"


# models.py

class Order(models.Model):
    customer_name = models.CharField(max_length=100)
    customer_phone = models.CharField(max_length=20)
    customer_description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.customer_name
