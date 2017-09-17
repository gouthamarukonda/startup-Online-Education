import json

from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.utils.dateparse import parse_datetime
from datetime import datetime
from django.contrib.admin.views.decorators import staff_member_required

from question.models import Question
from paper.models import Paper, Mapping, PM_CHOICES, PAPER_CHOICES
from userprofile.decorators import admin_teacher_required, teacher_required
from program.models import Program
from institute.models import Institute

@csrf_exempt
@teacher_required
def paper_create(request):
	if request.method == 'POST':

		try:
			if not request.POST.get("paper_name"):
				return JsonResponse({"status": False, "msg": "Paper Name shouldn't be empty"})

			institutes_list = json.loads(request.POST.get("institute_id"))["institute_list"]

			if not Program.objects.filter(program_id = request.POST.get("program_id")).exists():
				return JsonResponse({"status": False, "msg": "Program ID does not exist"})

			for i in range(len(institutes_list)):
				if not Institute.objects.filter(institute_id = institutes_list[i]).exists():
					return JsonResponse({"status": False, "msg": "Institute ID " + institutes_list[i] +" does not exist"})

			if request.POST.get("paper_type") not in [choice[0] for choice in PAPER_CHOICES]: 
				return JsonResponse({"status": False, "msg": "Invalid Paper Type"})

			if request.POST.get("partial_marking") not in [choice[0] for choice in PM_CHOICES]: 
				return JsonResponse({"status": False, "msg": "Invalid Partial Marking Scheme"})
			
			paper = Paper()
			paper.paper_name = request.POST.get("paper_name")
			paper.program = Program.objects.get(program_id = request.POST.get("program_id"))
			paper.paper_type = request.POST.get("paper_type")
			paper.teacher_id = request.user.userprofile.teacherprofile
			paper.start_time = datetime.now()
			paper.end_time = datetime.now()
			paper.duration = request.POST.get("duration")
			paper.partial_marking = request.POST.get("partial_marking")

			try:
				paper.save()
				for i in range(len(institutes_list)):
					paper.institutes.add(institutes_list[i])

				return JsonResponse({"status": True, "msg": "Paper Registered Successfully"})
			except:
				paper.delete()
				return JsonResponse({"status": False, "msg": "Internal Server Error"})

		except:
			return JsonResponse({"status": False, "msg": "Internal Server Error"})

@csrf_exempt
@teacher_required
def mapping_create(request):
	if request.method == 'POST':

		try:
			if not Paper.objects.filter(paper_id = request.POST.get("paper_id")).exists():
				return JsonResponse({"status": False, "msg": "Paper ID doesn't exist"})
			if not Question.objects.filter(question_id = request.POST.get("question_id")).exists():
				return JsonResponse({"status": False, "msg": "Question ID doesn't exist"})

			mapping = Mapping()
			mapping.paper = Paper.objects.get(paper_id = request.POST.get("paper_id"))
			mapping.question = Question.objects.get(question_id = request.POST.get("question_id"))
			mapping.save()
			return JsonResponse({"status": True, "msg": "Question Successfully added to Paper"})

		except:
			return JsonResponse({"status": False, "msg": "Internal Server Error"})
