from django.contrib import admin
from .models import *
from django.contrib.admin.widgets import FilteredSelectMultiple
from django import forms


class CourseAdmin(admin.ModelAdmin):
    class Meta:
        model = Course
        exclude = []

    participants = forms.ModelMultipleChoiceField(queryset=Profile.objects.all(),
                                                required=True,
                                                widget=FilteredSelectMultiple (
                                                    verbose_name='Participants',
                                                    is_stacked=False)
                                                )
    instructor = forms.ModelMultipleChoiceField(queryset=Profile.objects.all (),
                                   required=True,
                                   widget=FilteredSelectMultiple (
                                       verbose_name='Participants',
                                       is_stacked=False)
                                   )
    def get_queryset(self, request):
        profile = Profile.objects.get(user = request.user)
        if profile.language == 'L':
            return Course.objects.all()
        else:
            return Course.objects.filter(language= profile.language)

    filter_horizontal = ('participants', 'instructor')

admin.site.register(Course, CourseAdmin)
