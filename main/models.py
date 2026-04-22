from django.db import models
from django.contrib.auth.models import User

# 1. Пайдаланушы профилі (Қосымша мәліметтер үшін)
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    phone = models.CharField(max_length=20, blank=True, null=True, verbose_name="Телефон")
    image = models.ImageField(upload_to='profiles/', blank=True, null=True, verbose_name="Профиль суреті")

    def __str__(self):
        return f"{self.user.username} профилі"

# 2. Тауарлар кестесі (LUMIÈRE D'OR гүлдері)

class Product(models.Model):
    # Категориялар таңдауы
    CATEGORY_CHOICES = [
        ('mono', 'Моно-букеттер'),
        ('premium', 'Премиум'),
        ('box', 'Қораптағы гүлдер'),
    ]

    name = models.CharField(max_length=255, verbose_name="Букет атауы")
    description = models.TextField(blank=True, verbose_name="Сипаттама") 
    tags = models.CharField(max_length=500, blank=True, help_text="Үтір арқылы жазыңыз: роза, қызыл, сыйлық")
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, verbose_name="Категория")
    price = models.DecimalField(max_digits=10, decimal_places=0, verbose_name="Бағасы (₸)")
    image_url = models.URLField(max_length=500, verbose_name="Сурет сілтемесі") # HTML-дегі дайын сілтемелер үшін
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Букет"
        verbose_name_plural = "Букеттер"