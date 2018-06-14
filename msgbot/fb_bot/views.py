from django.views import generic
from django.http.response import HttpResponse
import json
import requests
from pprint import pprint
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from fb_bot.parser import portal_const
from fb_bot.parser import attachments


class BotView(generic.View):

	@method_decorator(csrf_exempt)
	def dispatch(self, request, *args, **kwargs):
		return generic.View.dispatch(self, request, *args, **kwargs)

	def post(self, request, *args, **kwargs):
		incoming_message = json.loads(self.request.body.decode('utf-8'))
		for entry in incoming_message['entry']:
			if 'messaging' in entry:
				for message in entry['messaging']:
					if 'message' in message:
						post_facebook_message(
							message['sender']['id'],
							"start"
						)
					else:
						try:
							post_facebook_message(
								message['sender']['id'],
								message['postback']['payload']
							)
						except KeyError:
							pprint("Unexpected value")

		return HttpResponse()

	def get(self, request, *args, **kwargs):
		if self.request.GET['hub.verify_token'] == portal_const.verify_token:
			return HttpResponse(self.request.GET['hub.challenge'])
		else:
			return HttpResponse('Invalid Token')


def post_facebook_message(fbid, postback):
	post_message_url = \
		'https://graph.facebook.com/v3.0/me/messages?access_token=' + portal_const.access_token

	if postback == "films":
		attachment = attachments.get_list_attachment(already_out=1)
	elif postback == "announcements":
		attachment = attachments.get_list_attachment(already_out=0)
	elif "info" in postback:
		attachment = attachments.get_info_page(postback[5:])
	elif postback == "about":
		attachment = attachments.about
	else:
		attachment = attachments.start

	response_msg = json.dumps(
		{
			"recipient": {"id": fbid},
			"message": {
				"attachment": attachment
			}
		}
	)
	headers = {"Content-type": "application/json"}
	status = requests.post(post_message_url, headers=headers, data=response_msg)
	pprint(status.json())
	return status.status_code
