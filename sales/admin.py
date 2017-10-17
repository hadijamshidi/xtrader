from django.contrib import admin
from .models import Payment


class payment_admin(admin.ModelAdmin):
    list_display = (
        'membership',
        'amount',
        'success',
    )

admin.site.register(Payment,payment_admin)