
#from django.http import HttpResponse
from django.http import HttpResponse, HttpResponseRedirect
from .models import Question
from django.template import loader
from django.shortcuts import render, get_object_or_404
from django.http import Http404
from django.urls import reverse

from .models import Choice, Question

def index(request):
	#latest_question_list = Question.objects.order_by('-pub_date')[:5]
	#context = {'latest_question_list':latest_question_list}
	#return render(request, 'polls/index.html', context)

	#Code without Render
	latest_question_list = Question.objects.order_by('pub_date')[:5]
	template = loader.get_template('polls/index.html')
	context = {'latest_question_list':latest_question_list,}
	return HttpResponse(template.render(context, request))

	#Code without the template
    #latest_question_list = Question.objects.order_by('-pub_date')[:5]
	#output = ', '.join([q.question_text for q in latest_question_list])
	#return HttpResponse(output)

def detail(request, question_id):
	try:
		question = Question.objects.get(pk=question_id)
	except Question.DoesNotExist:
		raise Http404("Question does not exist")
	return render(request, 'polls/detail.html', {'question':question})

def results(request, question_id):
	#response = "Results of question %s."
	#return HttpResponse(response % question_id)
	question = get_object_or_404(Question, pk=question_id)
	#if question_id < 3:
	next = question_id + 1
	#else:
	#next = question_id
	number_of_questions = question.choice_set.count
	return render(request, 'polls/results.html', {'question':question, 'next':next, 'number_of_questions':number_of_questions,})

def vote(request, question_id):
	question = get_object_or_404(Question, pk=question_id)
	try:
		selected_choice = question.choice_set.get(pk=request.POST['choice'])
	except (KeyError, Choice.DoesNotExist):
		#render(arg1: request obj, arg2: template name, arg3(opt): dict). Returns a HttpResponse obj of the given template
		#with the given context {'name on the template1':python name1, 'name on the template2':python name2, 'Name on the templ_n':python name_n}.
		return render(request, 'polls/detail.html', {'question': question, 'error_message': "You didn't select a choice.",})
	else:
		selected_choice.votes += 1
		selected_choice.save()
		#args=questio.id will be passed to def results as arg: question_id
		return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))

def results_all(request):
	results = Choice.objects.all()
	return render(request, 'polls/results_all.html', {'results':results},)