from django.db import models
from six import python_2_unicode_compatible
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save
import random
import datetime

lang_choices = (
    ('C', 'Chinese'),
    ('R', 'Russian'),
    ('A', 'Arabic'),
    ('L', 'All'),
    ('E', 'Russian-in-English'),
    ('B', 'Arabic-in-Arabic'),
    ('P', 'Portuguese-in-English'),
    ('D', 'Portuguese-in-Portuguese'),
    ('H', 'Hindi'),
    ('I', 'Indonesian'),
    ('T', 'Turkish'),
    ('U', 'Urdu'),
    ('F', 'French'),
    ('W', 'Swahili'),
    ('Z', 'Chinese-in-English')
)

lang_profile = (
    ('C', 'All-Chinese'),
    ('R', 'Russian'),
    ('A', 'Arabic'),
    ('L', 'All'),
    ('E', 'Russian-in-English'),
    ('B', 'Arabic-in-Arabic'),
    ('P', 'Portuguese-in-English'),
    ('D', 'Portuguese-in-Portuguese'),
    ('I', 'All-Arabic'),
    ('O', 'All-Portuguese'),
    ('S', 'All-Indonesian'),
    ('T', 'All-Turkish'),
    ('H', 'All-Hindi'),
    ('U', 'All-Urdu'),
    ('F', 'French'),
    ('W', 'Swahili')
)

user_choices = (
    ('I', 'Instructor'),
    ('S', 'Student')
)


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    language = models.CharField (max_length=1, choices=lang_profile, blank=False)
    type = models.CharField(max_length=1, choices=user_choices, blank=True, default='S')
    def __str__(self):
        return self.user.username


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


class FeedbackLabels(models.Model):
    label_max = models.CharField(verbose_name='Label for maximum level of agreement', max_length=150, blank=False)
    label_min = models.CharField(verbose_name='Label for minimum level of agreement', max_length=150, blank=False)
    language = models.CharField(max_length=1, choices=lang_choices, blank=False)

    def __str__(self):
        return self.get_language_display()


@python_2_unicode_compatible
class Topic(models.Model):
    name = models.CharField(max_length=150, blank=False)
    objectives = models.ForeignKey ('LearningObjectives', on_delete=models.CASCADE, blank=True, null=True)
    activation = models.TextField (verbose_name='Schema Activation', blank=True)
    new_information = models.TextField (blank=True)
    reflection = models.TextField(verbose_name='Reflection Task', blank=True)
    roleplay = models.TextField(verbose_name='Roleplay Task', blank=True)
    extension = models.TextField(verbose_name='Extension Task', blank=True)
    scenarios = models.ManyToManyField('Scenario')
    language = models.CharField (max_length=1, choices=lang_choices, blank=False)
    topic_image = models.ImageField(null=True, blank=True)
    author = models.ForeignKey (User, on_delete=models.CASCADE)
    order = models.IntegerField(blank=True, default=1)

    def __str__(self):
        return self.name+" ("+str(self.get_language_display())+")"


@python_2_unicode_compatible
class Module(models.Model):
    name = models.CharField(max_length=150, blank=False)
    module_number = models.IntegerField(blank=False)
    introduction = models.TextField(verbose_name="Module Introduction", blank=True)
    blurb = models.TextField(blank=True, null=True)
    objectives = models.ForeignKey('LearningObjectives', on_delete=models.CASCADE, blank=True, null=True)
    topics = models.ManyToManyField('Topic')
    language = models.CharField(max_length=1, choices=lang_choices, blank=False)
    image_for_topics = models.ImageField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    def __str__(self):
        return self.name+" ("+str(self.get_language_display())+")"


@python_2_unicode_compatible
class LearningObjectives(models.Model):
    name = models.CharField(max_length=150, blank=False)
    objectives = models.TextField(verbose_name="Learning Objectives", blank=False)
    language = models.CharField(max_length=1, choices=lang_choices, blank=False)
    def __str__(self):
        return self.name + " (" + str(self.get_language_display()) + ")"


@python_2_unicode_compatible
class Scenario(models.Model):
    name = models.CharField(max_length=150, blank=False)
    description = models.TextField(verbose_name="Situation", blank=True)
    initial_information = models.TextField(verbose_name="Context of the Scenario", blank=True)
    context_after_feedback = models.BooleanField (default=False, blank=True)
    context_before_and_after_feedback = models.BooleanField (default=False, blank=True)
    judgment_task = models.ForeignKey('JudgmentTask', on_delete= models.CASCADE)
    language_note = models.TextField(verbose_name="Language Notes", blank=True)
    culture_note = models.TextField(verbose_name="Culture Notes", blank=True)
    language_note_after_feedback = models.BooleanField (default=False, blank=True)
    language_note_before_and_after_feedback = models.BooleanField (default=False, blank=True)
    culture_note_after_feedback = models.BooleanField (default=False, blank=True)
    culture_note_before_and_after_feedback = models.BooleanField (default=False, blank=True)
    reflection_task = models.TextField(verbose_name="Scenario Reflection Task", blank=True)
    extension_task = models.TextField(verbose_name="Scenario Extension Task", blank=True)
    author = models.ForeignKey (User, on_delete=models.CASCADE)
    order = models.IntegerField(blank=True, default=1)

    def get_scenario_language(self):
        topic = Topic.objects.get(scenarios__in=[self.id])
        return topic.language


    def __str__(self):
        return self.name


@python_2_unicode_compatible
class JudgmentTask(models.Model):

    name = models.CharField (max_length=150,
                                    blank=False,
                                    verbose_name=('Name'))
    description = models.TextField(verbose_name="Judgment Task Description", blank=True)

    def get_answers(self):
        answers = Answer.objects.filter(task=self)
        answers = sorted(answers, key=lambda x: random.random ())
        return answers

    def get_answers_list(self):
        return [(answer.id, answer.content) for answer in
                self.order_answers(Answer.objects.filter(question=self))]

    def answer_choice_to_string(self, guess):
        return Answer.objects.get(id=guess).content

    class Meta:
        verbose_name = ("Multiple Choice Question")
        verbose_name_plural = ("Multiple Choice Questions")

    class Meta:
        verbose_name = ("Judgment Task")
        verbose_name_plural = ("Judgment Tasks")

    def __str__(self):
        return self.name


@python_2_unicode_compatible
class Answer(models.Model):
    task = models.ForeignKey(JudgmentTask, verbose_name=("Judgement Task"), on_delete=models.CASCADE)
    content = models.TextField(
                                blank=False,
                                help_text=("Enter the answer text that "
                                             "you want displayed"),
                                verbose_name=("Content"))
    feedback_initial = models.TextField( verbose_name= 'Initial Feedback', blank=True)
    feedback_final = models.TextField(verbose_name='Final Feedback', blank=False)
    rating_from = models.DecimalField(verbose_name='Rating From', max_digits=2, decimal_places=1)
    rating_to = models.DecimalField(verbose_name='Rating To', max_digits=2, decimal_places=1)

    def get_responses(self):
        users = User.objects.exclude(id__in=(1, 2, 3))
        responses = Response.objects.filter(answer=self, user__in=users)
        return responses

    def get_user_responses(self, users):
        responses = Response.objects.filter(answer=self, user__in=users)
        return responses

    def __str__(self):
        return self.content

    class Meta:
        verbose_name = ("Option")
        verbose_name_plural = ("Options")


@python_2_unicode_compatible
class Response(models.Model):
    answer = models.ForeignKey(Answer, verbose_name=("Options"), on_delete=models.CASCADE)
    response = models.DecimalField(verbose_name='Response', max_digits=3, decimal_places=1)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    responded = models.DateTimeField(max_length=100, default=datetime.datetime.now)

    def __str__(self):
        return 'Response to '+self.answer.task.name
