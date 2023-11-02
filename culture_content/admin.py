from django import forms
from django.contrib.admin.widgets import FilteredSelectMultiple
from django.db.models import Q
from django.contrib import admin
from .models import *
from tinymce.widgets import TinyMCE
from django.urls import reverse
from django.utils.html import format_html
from django.urls import reverse
from django.utils.html import format_html

'''
class TextMedia:
    js = [
         '/static/grappelli/tinymce/jscripts/tiny_mce/tiny_mce.js',
        '/static/grappelli/tinymce_setup/tinymce_setup.js',
        ]
'''

class AnswerInline(admin.TabularInline):
    model = Answer
    exclude = ['feedback_initial']
    extra=4
    formfield_overrides = {

        models.TextField: {'widget': TinyMCE()}

    }


class MCQuestionAdmin(admin.ModelAdmin):
    class Meta:
        model = JudgmentTask
        exclude = []
    list_display = ('name', )
    list_filter = ('name',)
    fields = ('name', 'description')
    formfield_overrides = {

        models.TextField: {'widget': TinyMCE()}

    }
    search_fields = ('name', )
    inlines = [AnswerInline]

class ModuleAdmin(admin.ModelAdmin):
    class Meta:
        model = Module
        exclude = []

    formfield_overrides = {

        models.TextField: {'widget': TinyMCE()}

    }

    filter_horizontal = ('topics',)


class TopicAdmin(admin.ModelAdmin):
    class Meta:
        model = Topic
        exclude = []

    search_fields = ('name',)
    list_display = ('id', 'name', 'display_learning_obj',)
    list_display_links = ('name',)
    list_filter = ('name',)

    def display_learning_obj(self, obj):
        link = reverse("admin:culture_content_learningobjectives_change", args=[obj.objectives.id])
        return format_html('<a href="{}">{}</a>', link, obj.objectives)
    display_learning_obj.short_description = "Related Learning Objective"

    scenarios = forms.ModelMultipleChoiceField(queryset=Topic.objects.all(),
                                               required=True,
                                               widget=FilteredSelectMultiple(
                                                   verbose_name='Scenarios',
                                                   is_stacked=True)
                                               )
    formfield_overrides = {

        models.TextField: {'widget': TinyMCE()}

    }
    filter_horizontal = ('scenarios',)

    def get_queryset(self, request):
        profile = Profile.objects.get(user = request.user)
        if profile.language == 'L':
            return Topic.objects.all()
        elif profile.language == 'O':
            return Topic.objects.filter(Q(language__in=['P', 'D'])|Q(author=profile.user))
        elif profile.language == 'C':
            return Topic.objects.filter(Q(language__in=['C', 'Z'])|Q(author=profile.user))
        elif profile.language == 'I':
            return Topic.objects.filter(Q(language__in=['I'])|Q(author=profile.user))
        elif profile.language == 'H':
            return Topic.objects.filter(Q(language__in=['H'])|Q(author=profile.user))
        elif profile.language == 'U':
            return Topic.objects.filter(Q(language__in=['U'])|Q(author=profile.user))
        elif profile.language == 'S':
            return Topic.objects.filter(Q(language__in=['A', 'B'])|Q(author=profile.user))
        elif profile.language == 'T':
            return Topic.objects.filter(Q(language__in=['T'])|Q(author=profile.user))
        else:
            return Topic.objects.filter(Q(language= profile.language)|Q(author=profile.user))


class ScenarioAdmin(admin.ModelAdmin):
    class Meta:
        model = Scenario
        exclude = []

    search_fields = ('name',)
    list_display = ('name',)
    formfield_overrides = {

        models.TextField: {'widget': TinyMCE()}

    }

    def get_queryset(self, request):
        profile = Profile.objects.get(user = request.user)
        if profile.language == 'L':
            return Scenario.objects.all()
        elif profile.language == 'O':
            scenarios_topics = Topic.objects.filter(Q(language__in=['P', 'D'])|Q(author=profile.user))
            scenario_ids = [scenario.pk for topic in scenarios_topics for scenario in topic.scenarios.all()]
            return Scenario.objects.filter(id__in=scenario_ids)
        elif profile.language == 'I':
            scenarios_topics = Topic.objects.filter(Q(language__in=['I'])|Q(author=profile.user))
            scenario_ids = [scenario.pk for topic in scenarios_topics for scenario in topic.scenarios.all()]
            return Scenario.objects.filter(id__in=scenario_ids)
        elif profile.language == 'C':
            scenarios_topics = Topic.objects.filter(Q(language__in=['C', 'Z'])|Q(author=profile.user))
            scenario_ids = [scenario.pk for topic in scenarios_topics for scenario in topic.scenarios.all()]
            return Scenario.objects.filter(id__in=scenario_ids)
        elif profile.language == 'H':
            scenarios_topics = Topic.objects.filter(Q(language__in=['H'])|Q(author=profile.user))
            scenario_ids = [scenario.pk for topic in scenarios_topics for scenario in topic.scenarios.all()]
            return Scenario.objects.filter(id__in=scenario_ids)
        elif profile.language == 'U':
            scenarios_topics = Topic.objects.filter(Q(language__in=['U'])|Q(author=profile.user))
            scenario_ids = [scenario.pk for topic in scenarios_topics for scenario in topic.scenarios.all()]
            return Scenario.objects.filter(id__in=scenario_ids)
        elif profile.language == 'T':
            scenarios_topics = Topic.objects.filter(Q(language__in=['T'])|Q(author=profile.user))
            scenario_ids = [scenario.pk for topic in scenarios_topics for scenario in topic.scenarios.all()]
            return Scenario.objects.filter(id__in=scenario_ids)
        elif profile.language == 'S':
            scenarios_topics = Topic.objects.filter(Q(language__in=['A', 'B'])|Q(author=profile.user))
            scenario_ids = [scenario.pk for topic in scenarios_topics for scenario in topic.scenarios.all()]
            return Scenario.objects.filter(id__in=scenario_ids)
        else:
            scenarios_topics = Topic.objects.filter(Q(language= profile.language)|Q(author=profile.user))
            scenario_ids = [scenario.pk  for topic in scenarios_topics for scenario in topic.scenarios.all()]
            return Scenario.objects.filter(id__in =scenario_ids)


class ProfileAdmin(admin.ModelAdmin):
    class Meta:
        model = Profile
        exclude = []
    search_fields = ['user__username']

class LearningObjectiveAdmin(admin.ModelAdmin):
    class Meta:
        model = LearningObjectives
        exclude = []
    search_fields = ['name']

    formfield_overrides = {

        models.TextField: {'widget': TinyMCE()}

    }


admin.site.register(Module, ModuleAdmin)
admin.site.register(Scenario,  ScenarioAdmin)
admin.site.register(JudgmentTask, MCQuestionAdmin)
admin.site.register(Topic, TopicAdmin)
admin.site.register(Response)
admin.site.register(LearningObjectives, LearningObjectiveAdmin)
admin.site.register(Profile, ProfileAdmin)
