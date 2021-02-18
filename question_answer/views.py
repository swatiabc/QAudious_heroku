from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.views.decorators.http import require_http_methods

from . import model_answer
from . import models
from transcribe_audio.models import AudioDataModel

# Create your views here.
def question_page(request):
    print("-------------question_2-----------------------")
    return render(request,"question_2.html")


@require_http_methods(['GET', 'POST'])
def qa_display_page(request):
    if 'question' not in request.session:
        return HttpResponseRedirect("post_question.html")

    if request.method == 'GET':
        return render(request,"qa_display.html")
    
    qa_data = models.QADataModel()
    qa_data.question = request.session["question"]
    try:
        qa_data.transcript = AudioDataModel.objects.get(id=request.session['transcript'])
    except (KeyError, AudioDataModel.DoesNotExist):
        qa_data.transcript = None
    
    qa_data.answer = request.session["answer"]
    qa_data.save()

    return render(request,"qa_saved.html")



def qa_delete_confirm_page(request):
    if 'question' not in request.session:
        return HttpResponseRedirect("post_question.html")
    return render(request, "qa_delete_confirm.html")


def qa_deleted_page(request):
    if 'question' not in request.session:
        return HttpResponseRedirect("post_question.html")
    del request.session["question"]
    del request.session["answer"]
    return render(request,"qa_deleted.html")

def qa_saved_page(request):
    return render(request,"qa_saved.html")


@require_http_methods(['GET', 'POST'])
def post_question(request):

    if 'transcript' not in request.session:
        return HttpResponseRedirect("upload.html")

    if request.method == 'GET': 
        return render(request,"post_question.html")

    uploaded_question = request.POST['uploaded_question']
    request.session["question"]=uploaded_question
    request.session["answer"]=model_answer.get_answer()
    #abstract = None
    try:
        abstract = AudioDataModel.objects.get(id=request.session['transcript'])
    except (KeyError, AudioDataModel.DoesNotExist):
        abstract = None
    print(type(abstract),abstract,"-0-0-0-0-0-0-0-0--0-0--0-0-0-0-0-0-0-")
    print(type(uploaded_question),uploaded_question,"9-9090909-0-90--090-098")
    request.session["answer"] = model_answer.answer_question(uploaded_question,abstract.transcript)

    return HttpResponseRedirect("qa_display.html")


def use_ajax_for_session(request):
    qa_data = { "question" : request.session["question"],
                "answer" : request.session["answer"] }
    return JsonResponse(data=qa_data ,status=200)