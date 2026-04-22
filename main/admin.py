from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from .models import Profile, Product

# Профильді пайдаланушы бетінің ішінде көрсету үшін
class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = 'Қосымша мәліметтер'

# Стандартты UserAdmin-ді кеңейту
class UserAdmin(BaseUserAdmin):
    inlines = (ProfileInline,)
    # 'is_active' қостық, сонда жасыл белгіше (актив) шығады
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'is_active', 'get_phone')

    def get_phone(self, instance):
        # Пайдаланушыда профиль бар-жоғын тексеру
        if hasattr(instance, 'profile'):
            return instance.profile.phone
        return "-"
    get_phone.short_description = 'Телефон'

# Ескі User тіркеуін өшіріп, жаңасын қосу
admin.site.unregister(User)
admin.site.register(User, UserAdmin)
admin.site.register(Profile)
admin.site.register(Product)