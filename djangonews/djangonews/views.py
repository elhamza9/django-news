from django.shortcuts import redirect

def welcome(request):
    return redirect('list_topics')