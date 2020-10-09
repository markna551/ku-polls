"""Use to redirect to any page in ku-polls."""
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic
from django.utils import timezone
from django.contrib import messages
from .models import Choice, Question


class IndexView(generic.ListView):
    """Redirect to index page."""

    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        """Return the last five published questions."""
        return Question.objects.filter(
            pub_date__lte=timezone.now()
        ).order_by('-pub_date')


def vote_for_poll(request, pk):
    """
    Redirect to detail page.

    If this question can't vote will redirect to index page.
    """
    question = Question.objects.get(pk=pk)
    if not (question.can_vote()):
        messages.warning(request, "This question is expired.")
        return HttpResponseRedirect(reverse('polls:index'))
    return render(request, 'polls/detail.html', {"question": question})


class ResultsView(generic.DetailView):
    """Redirect to results page."""

    model = Question
    template_name = 'polls/results.html'


def vote(request, question_id):
    """Redirect to vote page."""
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        if not (question.can_vote()):
            messages.warning(request, "This question is expired.")
            return HttpResponseRedirect(reverse('polls:index'))
        selected_choice.votes += 1
        selected_choice.save()
        return HttpResponseRedirect(reverse('polls:results',
                                            args=(question.id,)))
