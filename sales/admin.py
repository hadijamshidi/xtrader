from django.contrib import admin
from .models import Payment


class payment_admin(admin.ModelAdmin):
    list_display = (
        'membership',
        'amount',
        'success',
    )

# Register your models here.
admin.site.register(Payment,payment_admin)