from django.test import TestCase
from fb_bot.models import Movie
from fb_bot.views import post_facebook_message
from fb_bot.parser.portal_const import test_id


class BotTestCase(TestCase):

	def setUp(self):
		self.new_movie = Movie.objects.create(
			already_out=1,
			film_id=255,
			title="Test Movie",
			all_shows_today="12:25",
			show_start="31.05.2018",
			show_end="20.06.2018",
			country="Ukraine",
			director="Junior Developer",
			format="2D",
			genres="Test Genre",
			year="2018",
			duration="133",
			actors="Developer Actor, Developer Actor 2, Third Developer",
			trailer="https://www.youtube.com/",
			poster="https://www.google.com/images/branding/googlelogo/2x/googlelogo_color_272x92dp.png",
		)
		self.new_announcement = Movie.objects.create(
			already_out=0,
			film_id=512,
			title="Test Announcement",
			all_shows_today="none",
			show_start="31.05.2018",
			show_end="20.06.2018",
			country="Ukraine",
			director="Junior Developer",
			format="",
			genres="Test Genre",
			year="2018",
			duration="",
			actors="Developer Actor, Developer Actor 2, Third Developer",
			trailer="https://www.youtube.com/",
			poster="https://www.google.com/images/branding/googlelogo/2x/googlelogo_color_272x92dp.png",
		)

	def test_bot_can_send_movie_list(self):
		response = post_facebook_message(test_id, "films")
		self.assertIs(response, 200)

	def test_bot_can_send_announcement_list(self):
		response = post_facebook_message(test_id, "announcements")
		self.assertIs(response, 200)

	def test_bot_can_send_specific_movie(self):
		response = post_facebook_message(test_id, "info " + str(self.new_movie.film_id))
		self.assertIs(response, 200)

	def test_bot_can_send_specific_announcement(self):
		response = post_facebook_message(test_id, "info " + str(self.new_announcement.film_id))
		self.assertIs(response, 200)

	def test_bot_can_send_start_menu(self):
		response = post_facebook_message(test_id, "start")
		self.assertIs(response, 200)
