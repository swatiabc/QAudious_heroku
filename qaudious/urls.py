"""qaudious URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from transcribe_audio.views import( upload_page, local_page, drive_page,home_view,)
from question_answer.views import(question_page,qa_display_page,qa_saved_page,post_question,
            qa_delete_confirm_page, qa_deleted_page,use_ajax_for_session, )


urlpatterns = [
    path('upload.html', upload_page),
    path('local.html', local_page),
    path('', home_view),
    path('drive.html', drive_page),
    path('post_question.html', post_question),
    path('question_2.html',question_page),
    path('qa_display.html',qa_display_page),
    path('qa_saved.html',qa_saved_page),
    path('qa_deleted.html',qa_deleted_page),
    path('qa_delete_confirm.html',qa_delete_confirm_page),
    path('qa_data', use_ajax_for_session ),
    path('admin/', admin.site.urls),
]

