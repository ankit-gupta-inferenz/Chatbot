from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static
from .views import chat_view, send_message, feedback, chat_screen_view,setcookie,getUserInfo,getFeedbackForm,updateProduct,index

urlpatterns = [
    path('', chat_view, name='chat'),
    path('screen/', chat_screen_view, name='chat_screen'),
    # path("get/<str:query>", views.getData, name = 'getData'),
    path('screen/send_message/', send_message, name='send_message'),
    path('screen/feedback/', feedback, name='feedback'),
    path('screen/updateProduct/', updateProduct, name='feedback'),
    # path('screen/mic/', recordVoice, name='mic'),
    path('scookie/<key>/<name>/',setcookie),
    path('getuserinfo',getUserInfo),
    path('feedback',getFeedbackForm)
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
