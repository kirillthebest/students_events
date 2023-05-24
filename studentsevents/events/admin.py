from django.contrib import admin
from .models import *
from django.contrib.admin import AdminSite
from django.contrib.auth.models import Group, User
from django.contrib.auth.admin import GroupAdmin, UserAdmin


class MyAdminSite(AdminSite):

    def get_app_list(self, request):
        """
        Return a sorted list of all the installed apps that have been
        registered in this site.
        """
        app_dict = self._build_app_dict(request)

        # Sort the apps alphabetically.
        app_list = sorted(app_dict.values(), key=lambda x: x['name'].lower())

        # Sort the models alphabetically within each app.
        #for app in app_list:
        #    app['models'].sort(key=lambda x: x['name'])

        return app_list


admin.site = MyAdminSite()
admin.site.site_header = 'Мероприятия факультета'
admin.site.index_title = 'Администрирование'
admin.site.site_title = 'Мероприятия факультета'


# admin.site.unregister(User)
# admin.site.register(CustomUser, UserAdmin)

admin.site.register(StudentGroup)

admin.site.register(EventType)


class EventAdmin(admin.ModelAdmin):
    list_display = ('name', 'event_type', 'event_date')


admin.site.register(Event, EventAdmin)


class UserTypeFilter(admin.SimpleListFilter):
    # Human-readable title which will be displayed in the
    # right admin sidebar just above the filter options.
    title = 'Пользователь'

    # Parameter for the filter that will be used in the URL query.
    parameter_name = "user_type"

    def lookups(self, request, model_admin):
        return [
            ("student", 'студент'),
            ("teacher", 'преподаватель'),
        ]

    def queryset(self, request, queryset):
        if self.value() == "student":
            return queryset.filter(user__is_superuser=False)
        if self.value() == "teacher":
            return queryset.filter(user__is_superuser=True)


class EventInline(admin.StackedInline):
    model = ProfileEvent
    extra = 0


class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'group')
    list_filter = (UserTypeFilter, )

    def get_list_display(self, request):
        if 'user_type' in request.GET:
            if request.GET['user_type'] == 'teacher':
                return ('user',)
        return ('user', 'group')

    def get_fields(self, request, obj=None):
        if obj.user.is_superuser:
            return ('user', )
        return ('user', 'group')

    def get_inlines(self, request, obj):
        if not obj.user.is_superuser:
            return [EventInline]
        return []


admin.site.register(Profile, ProfileAdmin)

admin.site.register(Group, GroupAdmin)
admin.site.register(User, UserAdmin)

