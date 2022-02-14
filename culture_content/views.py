from .models import *
from django.shortcuts import render, get_list_or_404, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
import simplejson
from django.http import JsonResponse, HttpResponseForbidden
from course.models import Course
from glob import glob
import random
import os


@login_required
def home(request):
    img_r =[os.path.basename(r) for r in glob(r'/pythonapps/culture-app/static/assets/img/home_ru/*.jpg')]
    img_r_en = [os.path.basename(r) for r in glob(r'/pythonapps/culture-app/static/assets/img/home_ru_en/*.jpg')]
    img_a = [os.path.basename(d) for d in glob(r'/pythonapps/culture-app/static/assets/img/home_ar_en/*.jpg')]
    img_a_ar = [os.path.basename(d) for d in glob(r'/pythonapps/culture-app/static/assets/img/home_ar/*.jpg')]
    img_br_en = [os.path.basename(d) for d in glob(r'/pythonapps/culture-app/static/assets/img/home_br_en/*.jpg')]
    img_br_por = [os.path.basename(d) for d in glob(r'/pythonapps/culture-app/static/assets/img/home_br_por/*.jpg')]
    img_in = [os.path.basename(d) for d in glob(r'/pythonapps/culture-app/static/assets/img/home_in/*.jpg')]
    img_ur = [os.path.basename(d) for d in glob(r'/pythonapps/culture-app/static/assets/img/home_ur/*.jpg')]
    img_tk = [os.path.basename(d) for d in glob(r'/pythonapps/culture-app/static/assets/img/home_tk/*.jpg')]
    img_hi = [os.path.basename(d) for d in glob(r'/pythonapps/culture-app/static/assets/img/home_hi/*.jpg')]
    return render(request, 'culture_content/home.html', {'img_r': 'assets/img/home_ru/'+random.choice(img_r),
                                                         'img_r_en': 'assets/img/home_ru_en/'+random.choice(img_r_en),
                                                         'img_a': 'assets/img/home_ar_en/'+random.choice(img_a),
                                                         'img_a_ar': 'assets/img/home_ar/' + random.choice(img_a_ar),'img_br_en': 'assets/img/home_br_en/'+random.choice(img_br_en),
                                                         'img_br_por':'assets/img/home_br_por/' + random.choice(img_br_por),
                                                         'img_in':'assets/img/home_in/' + random.choice(img_in),
                                                         'img_ur':'assets/img/home_ur/' + random.choice(img_ur),
                                                         'img_tk':'assets/img/home_tk/' + random.choice(img_tk),
                                                         'img_hi':'assets/img/home_hi/' + random.choice(img_hi)})


@login_required
def get_modules(request, lang):
    modules = Module.objects.filter(language=lang).order_by('module_number')
    return render(request, 'culture_content/modules.html', {'modules': modules})


@login_required
def get_topic_scenarios(request, top_id):
    topic = get_object_or_404(Topic, pk=top_id)
    module = Module.objects.get(topics__in=[top_id])
    scenario_results = get_scenarios_responses(top_id, request.user)
    return render(request, 'culture_content/topics.html', {'topic': topic, 'module': module, 'scenario_results': scenario_results})


@login_required
def get_scenario_detail(request, scenario_id):
    scenario = get_object_or_404(Scenario, pk=scenario_id)
    topic = Topic.objects.get(scenarios__in =[scenario_id])
    module = Module.objects.get(topics__in=[topic.id])
    return render(request, 'culture_content/scenario.html', {'scenario': scenario, 'topic':topic, 'module':module})


@login_required
def save_response(request, answer_id, response):
    if request.is_ajax() and request.method=='POST':
        answer = Answer.objects.get(pk=answer_id)
        response = Response.objects.create(answer=answer, response= response, user=request.user)
        expert ={}
        expert['answer_id'] = answer_id
        expert['content'] = answer.content
        expert['feedback'] = answer.feedback_final
        expert['from']=answer.rating_from
        expert['to'] = answer.rating_to
        expert['response_id'] = response.pk
        return JsonResponse(expert, content_type='application/json')


@login_required
def get_user_responses(request, lang):
    statistics = []
    user_profile = Profile.objects.get(user=request.user)
    modules = Module.objects.filter(language=lang)
    topics = Module.objects.filter(id__in=modules).values('topics')
    scenarios = Topic.objects.filter(id__in=topics).values('scenarios')
    scenarios = Scenario.objects.filter(id__in=scenarios)
    for scene in scenarios:
        options_stats, scenario_stats = get_scenario_results(scene.id)
        statistics.append([scene, scenario_stats])
    return render(request, 'culture_content/responses.html', {'stats': statistics, 'user_language': user_profile.language})


@login_required
def get_user_responses_in_course(request, course_id):
    statistics = []
    course = Course.objects.get(id=course_id)
    participants = Course.objects.filter(id=course_id).values_list('participants__user')
    scenarios = Topic.objects.filter(language=course.language).values('scenarios')
    scenarios = Scenario.objects.filter (id__in=scenarios)
    for scene in scenarios:
        options_stats, scenario_stats = get_scenario_results(scene.id, users=participants)
        statistics.append ([scene, scenario_stats])
    return render (request, 'culture_content/responses_course.html',{'stats': statistics, 'course': course})


def get_scenarios_responses(topic_id, current_user):
    statistics = []
    scenarios = Topic.objects.filter(id=topic_id).values('scenarios')
    scenarios = Scenario.objects.filter(id__in=scenarios).order_by('order')
    for scene in scenarios:
        options_stats, scenario_stats = get_scenario_results(scene.id, user=current_user)
        statistics.append([scene, scenario_stats])
    return statistics


@login_required
def get_options_results(request, scenario_id, course_id=None):
    scenario = Scenario.objects.get (id=scenario_id)
    user_profile = Profile.objects.get(user=request.user)
    if course_id is not None:
        participants = Course.objects.filter(id=course_id).values_list('participants__user')
        options_stats, scenario_stats = get_scenario_results(scenario_id, users=participants)
        return render(request, 'culture_content/options_course_responses.html',
                      {'stats': options_stats, 'course_id': course_id, 'user_language': user_profile.language})
    else:
        options_stats, scenario_stats = get_scenario_results(scenario_id)
        return render (request, 'culture_content/options_responses.html', {'stats': options_stats, 'user_language': user_profile.language, 'scenario_language': scenario.get_scenario_language()})


def get_scenario_results(scenario_id, user=None, users=None):
    scenario = Scenario.objects.get(pk=scenario_id)
    options = []
    attempts = []
    stats = []
    for answer in scenario.judgment_task.get_answers():
        options.append(answer)
        results = []
        responses = 0
        if user is not None:
            answer_responses=answer.get_user_responses([user])
        elif users is not None:
            answer_responses=answer.get_user_responses(users)
        else:
            answer_responses=answer.get_responses()
        for res in answer_responses:
            responses += 1
            if res.response >= res.answer.rating_from and res.response <= res.answer.rating_to:
                results.append(1)
            else:
                results.append(0)
        attempts.append(round(len(results)))
        if len(results)>0:
            stats.append(round(100 * (sum (results)/len(results))))
        else:
            stats.append(0)
    output = zip(options, attempts, stats)
    scenario_stats=(attempts[0], round(sum(stats)/len(stats)))
    return(output, scenario_stats)


@login_required
def get_profile(request):
    if request.user.is_staff:
        profile = Profile.objects.get(user=request.user)
        return render(request, 'culture_content/dashboard.html', {'profile': profile})
    else:
        return HttpResponseForbidden()




