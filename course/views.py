from django.shortcuts import render
from django.conf import settings
from culture_content.models import *
from culture_content.views import get_scenario_results
from .models import Course
from django.contrib.auth.decorators import login_required
from .forms import SignUpForm
from django.shortcuts import render
import random
import string
from django.contrib.auth.hashers import make_password
from django.http import HttpResponse, HttpResponseRedirect
from django.core.mail import send_mail
from django.http import JsonResponse
from django.views.generic.edit import CreateView



def request_user(request):
		letters = string.ascii_lowercase
		passw = ''.join(random.choice(letters) for i in range(10))
		if (request.method == 'POST') and request.user.is_anonymous==True:
				form = SignUpForm(request.POST)
				if form.is_valid():
					if User.objects.filter(username = form.cleaned_data['email']).exists():
						return render(request, 'course/details.html', {'message': 'The email is currently in use. Please provide another email address.'})
					else:
						try:
								email = form.cleaned_data['email']
								data = form.save(commit=False)
								data.username = email
								data.password = make_password(passw)
								data.save()
								'''send_mail(
									'Culture app new account',
									'A request has been received to create an account with your email. The password associated with your email is: ' + data.password,
									'llcit@hawaii.edu',
									[email],
									settings.EMAIL_HOST_USER, settings.EMAIL_HOST_PASSWORD
								)'''
								return render(request, 'course/details.html', {'user': email, 'passw': passw})

						except:
								HttpResponse('The email is currently in use. Please provide another email address.')
		else:
				form = SignUpForm()
		return render(request, 'course/signup.html', {'form': form})


@login_required
def get_user_data(request):
		user_profile = Profile.objects.get(user=request.user)

		if user_profile.type=='I':
				courses = Course.objects.filter(instructor=request.user)
				return render(request, 'course/instructor.html', {'courses': courses, 'user_language':user_profile.language})
		elif user_profile.type=='S':
				courses = Course.objects.filter(participants__in=[user_profile])
				user_scenarios = Response.objects.filter(user=request.user).values('answer__task__scenario')
				scenarios =set([scenario['answer__task__scenario'] for scenario in user_scenarios])
				statistics=[]
				for scene in scenarios:
						if scene is not None:
								options_stats, scenario_stats = get_scenario_results(scene)
								scenario = Scenario.objects.get(id=scene)
								statistics.append([scenario, scenario_stats])

				return render(request, 'course/student.html', {'results': statistics, 'user_language':user_profile.language, 'courses':courses})


@login_required
def get_courses(request):
	profile = Profile.objects.get(user=request.user)
	courses = Course.objects.exclude(participants__in=[profile])
	return render(request, 'course/courses.html', {'courses': courses})


@login_required
def enroll_course(request):
	if request.POST.get('action') == 'post':
		course = request.POST.get('course')
		key = request.POST.get('key')
		course = Course.objects.get(id=course)
		if course.enrollment_key == key:
			profile = Profile.objects.get(user=request.user)
			course.participants.add(profile)
			return JsonResponse({'message':'You have been successfully enrolled in the course', 'response':1})
		else:
			return JsonResponse({'message':'Invalid key', 'response':0})


@login_required
def remove_user_from_course(request):
	if request.POST.get('action') == 'post':
		course = request.POST.get('course')
		student = request.POST.get('student')
		profile = Profile.objects.get(id=student)
		print(profile)
		course = Course.objects.get(id=course)
		print(course)
		course.participants.remove(profile)
		return JsonResponse({'message': 'Student has been removed from the course'})
	else:
		return JsonResponse({'message': 'Student is not part of this course'})


class CourseCreate(CreateView):
		model = Course
		success_url ='/profile'
		fields = ['name', 'enrollment_key']

		def form_valid(self, form):
			self.object = form.save()
			self.object.instructor.add(self.request.user)
			return HttpResponseRedirect(self.get_success_url())




