from django.conf.urls import include, url
from .views import BotView
from fb_bot.parser import portal_const

urlpatterns = [
	url(r'^'+portal_const.webhook_url+'/?$', BotView.as_view(), name='bot')
]
