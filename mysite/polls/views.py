import time

from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views import generic
from django.utils import timezone
from django.http import JsonResponse,HttpResponse
from django.views.decorators.cache import cache_page



from .models import Choice, Question


class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        """
        Return the last five published questions (not including those set to be
        published in the future).
        """
        return Question.objects.filter(
            pub_date__lte=timezone.now()
        ).order_by('-pub_date')[:5]




class DetailView(generic.DetailView):
    model = Question
    template_name = 'polls/detail.html'

    def get_queryset(self):
        """
        Excludes any questions that aren't published yet.
        """
        return Question.objects.filter(pub_date__lte=timezone.now())



class ResultsView(generic.DetailView):
    model = Question
    template_name = 'polls/results.html'


def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))


def json_fun(request):

    # return HttpResponse('HttpResponse')
    # return JsonResponse('JsonResponse',safe=False)
    d={'json':'string'}
    return JsonResponse(d)

# @cache_page(300)
@cache_page(60*10,cache='redis')
# @cache_page(60*10,cache='default')
def page_cache(request):
    from django.core.cache import caches
    time.sleep(3)
    return HttpResponse('cache_page')

from django.core.cache import cache
from django.core.cache import caches
import random
def muti_cache(request):
    # res_key=cache.get('res_key')
    res_key=caches['redis'].get('res_key')
    if not res_key:
        res_key = random.randint(0,100)
        cache.set('res_key','cache_key', 300)

    return HttpResponse(res_key)



