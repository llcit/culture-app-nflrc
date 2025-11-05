import json, string
from .models import *
from django.contrib.auth.models import User

user = User.objects.get(username='ADMIN USERNAME')
content_path = 'PATH TO CONTENT FILES/'

def load_module_content(file_name, LANGUAGE_CODE):
  print(f"Loading content from {file_name}...")

  with open(content_path+file_name, 'r', newline='') as f:
    data = json.load(f)  
    for module in data:

      # Create Module object
      learning_objectives = LearningObjectives.objects.create(
          name = module['module_title'] + " Learning Objectives",
          objectives=' '.join([i for i in module['module_learning_objectives']]),
          language=LANGUAGE_CODE,
      )

      module_obj = Module.objects.create(
          name=module['module_title'],
          module_number=module['module_number'],
          introduction="<p>"+module['module_introduction']+"</p>",
          blurb="<p>"+module['blurb']+"</p>",
          objectives=learning_objectives,
          language=LANGUAGE_CODE,
          author=user,   
      )

      for topic in module['topics']:
        topic_learning_objectives = LearningObjectives.objects.create(
          name = topic['title'] + " Topic Learning Objectives",
          objectives='<br>'.join([i for i in topic['learning_objectives']]),
          language=LANGUAGE_CODE,
        )

        topic_obj = Topic.objects.create(
          name=topic['title'],
          objectives=topic_learning_objectives,
          language=LANGUAGE_CODE,
          author=user,
          order=topic['topic_number'],
        )
        module_obj.topics.add(topic_obj)

        for scenario_data in topic['scenarios']:
          judgement_task_obj = JudgmentTask.objects.create(
            name=scenario_data['title'] + " Judgment Task",
            description=scenario_data['task'],          
          )

          for answer_data in scenario_data['opinions']:
            rating=answer_data['rating_range'].split('-'),
            answer_obj = Answer.objects.create(
              task=judgement_task_obj,
              content=answer_data['statement'],
              feedback_final=answer_data['feedback'],
              rating_from=float(rating[0][0]),
              rating_to=float(rating[0][1]),
            )

          context_data = scenario_data['context']
          context = ''
          for key, value in context_data.items():
            pkey = "<strong>"+string.capwords(key)+"</strong>" 
            context += f"{pkey}: {context_data[key]}<br>"

          cnote = scenario_data.get('culture_note', '')
          if cnote:
              cnote = "<p>" + cnote + "</p>"
          lnote = scenario_data.get('language_note', '')
          if lnote:
              lnote = "<p>" + lnote + "</p>"
          rnote=scenario_data.get('reflection_task', '')
          if rnote:
              rnote = "<p>" + rnote + "</p>"
          enote=scenario_data.get('extension_task', '')
          if enote:
              enote = "<p>" + enote + "</p>"
          
          scenario_obj = Scenario.objects.create(
              name=scenario_data['title'],
              description="<p>"+scenario_data['description']+"</p>",
              initial_information="<p>"+context+"</p>",
              judgment_task=judgement_task_obj,
              language_note=lnote,
              culture_note=cnote,
              reflection_task=rnote,
              extension_task=enote,
              author=user,
              order=scenario_data['scenario_number'],
          )
          topic_obj.scenarios.add(scenario_obj)
          

# CLEANUP DURING TESTING (Deletes all on cascade)       

          judgement_task_obj.delete()
        topic_learning_objectives.delete()
      learning_objectives.delete()          
      




""" Running in the interactive django shell:
from culture_content import content_loader

jfiles = ["jpn-mod-1.json", "jpn-mod-2.json", "jpn-mod-3.json", "jpn-mod-4.json", "jpn-mod-5.json"]
nfiles = ["jpn-mod-1-jpn.json", "jpn-mod-2-jpn.json", "jpn-mod-3-jpn.json", "jpn-mod-4-jpn.json", "jpn-mod-5-jpn.json"]

for i in jfiles:
  content_loader.load_module_content(i, 'J')

for i in nfiles:
  content_loader.load_module_content(i, 'N')

"""

