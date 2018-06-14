import requests
import json
import re
from fb_bot.parser import portal_const
from fb_bot.models import Movie


def get_film_ids():
	html = requests.get(portal_const.main_url).text
	pattern = r"load_film_info\((\d+)(?:,\s'(anonce)')?\)"
	found_films = re.findall(pattern, html)
	result = {}
	for film in found_films:
		result[film[0]] = film[1]
	return result


def get_film_info(film_id):
	headers = {
		'Content-type': 'application/x-www-form-urlencoded'
	}
	data = {'film': film_id}
	r = requests.post(portal_const.main_url + portal_const.info_url, headers=headers, data=data)
	return remap(json.loads(r.content))


def join_list(l):
	r = l
	if r is not None:
		r = ''.join(r)
	else:
		r = ''
	return r


def fix_string(s):
	s = s.replace(' ', '%20')
	return s


def get_link(s):
	link = re.findall(r'(?<=src=\").+?(?=\")', s)
	try:
		return link[0]
	except IndexError:
		return ""


def remap(film_info):
	new_film_info = {
		"title": film_info['result']['info']['title'],
		"all_shows_today": film_info['seance'],
		# "closest_show": join_list(film_info['time']),
		"show_start": join_list(film_info['date_anonce']),
		"show_end": join_list(film_info['date_close']),
		"country": film_info['result']['strana'],
		"director": film_info['result']['rezhisser'],
		"format": film_info['result']['format'],
		"genres": ', '.join(film_info['result']['zhanr']),
		"year": film_info['result']['god'],
		"duration": film_info["result"]['dlitelnost_min'],
		"actors": film_info["result"]['aktery'],
		"trailer": get_link(film_info["trejlery"]),
		"poster": fix_string(portal_const.main_url+portal_const.poster_url+film_info['main_photo']),
		"id": film_info['result']['info']['id'],
	}

	# We need the following only if we decide to show the schedule for the whole week
	"""
	try:
		new_film_info["schedule"] = film_info['schedule']
	except KeyError:
		new_film_info["schedule"] = ''
	"""
	if len(new_film_info['all_shows_today']) > 0:
		new_film_info['all_shows_today'] = ', '.join(new_film_info['all_shows_today'])
	else:
		new_film_info['all_shows_today'] = 'none'

	return new_film_info


# Key must be either '' or 'anonce'(sic!)
def parse_films(key):
	film_ids = get_film_ids()
	all_films = {}

	index = 0
	for film_id in film_ids.keys():
		if film_ids[film_id] == key:
			all_films[index] = get_film_info(film_id)
			index += 1
	# pprint(all_films)
	return all_films


def flush_db():
	for movie in Movie.objects.all():
		movie.delete()


def fill_db():

	flush_db()

	film_ids = get_film_ids()

	for film_id in film_ids.keys():
		if film_ids[film_id] == 'anonce':
			already_out = 0
		else:
			already_out = 1
		info = get_film_info(film_id)
		Movie.objects.create(
			already_out=already_out,
			film_id=info['id'],
			title=info['title'],
			all_shows_today=info['all_shows_today'],
			show_start=info['show_start'],
			show_end=info['show_end'],
			country=info['country'],
			director=info['director'],
			format=info['format'],
			genres=info['genres'],
			year=info['year'],
			duration=info['duration'],
			actors=info['actors'],
			trailer=info['trailer'],
			poster=info['poster'],
			# schedule=info['schedule']
		)
