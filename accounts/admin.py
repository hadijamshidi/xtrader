from django.contrib import admin
from .models import Profile, Subscribe, Membership
from userena.admin import UserenaAdmin
from django.contrib.auth.models import User


class ProfileAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'first_name', 'last_name', 'cellPhone', 'email', 'last_login', 'expire','have_subscribe')

    # list_filter = ['gender','people_type','level_type','personwith','interstToCoaoprat']
    # ('user__first_name', 'user__last_name', 'user__username',)
    def email(self, obj):
        return obj.user.email

    email.short_description = 'ایمیل'

    def make_published(modeladmin, request, queryset):
        print(queryset)
        # return queryset.order_by('-user__last_login')
        # actions = [formfield_for_foreignkey]


class SubscribeAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'value','vip')


admin.site.unregister(Profile)
admin.site.register(Profile, ProfileAdmin)
admin.site.register(Subscribe, SubscribeAdmin)
admin.site.register(Membership)
