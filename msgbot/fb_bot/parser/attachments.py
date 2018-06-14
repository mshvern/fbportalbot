from fb_bot.models import Movie


start = {
	"type": "template",
	"payload": {
		"template_type": "button",
		"text": "Привіт!\nЦе бот для кінотеатру Портал\n\nАдреса:\nм. Кропивницький (Кіровоград)\nвул. Соборна (50 років Жовтня) 1-А\n\nКонтакти:\n+38 095 25-75-233\n+38 0522 33-26-03\n\nРозроблено в Onix-Systems",
		"buttons": [
			{
				"type": "postback",
				"title": "Фільми",
				"payload": "films"
			},
			{
				"type": "postback",
				"title": "Анонси",
				"payload": "announcements"
			},
			{
				"type": "postback",
				"title": "Про Бота",
				"payload": "about",
			},
		]
	}
}

about = {
	"type": "template",
	"payload": {
		"template_type": "button",
		"text": "За посиланнями нижче Ви зможете перейти на сайт розробників цього боту або залишити свій відгук у нашому чаті в Telegram.",
		"buttons": [
			{
				"type": "web_url",
				"title": "Onix-Systems",
				"url": "https://onix-systems.com/"
			},
			{
				"type": "web_url",
				"title": "Чат для обговорення",
				"url": "https://t.me/portalbotsupport",
			},
			{
				"type": "postback",
				"title": "Меню",
				"payload": "start"
			}
		]
	}
}


def get_shows_today(m):
	if m.all_shows_today == 'none' or m.all_shows_today is None or len(m.all_shows_today) == 0:
		subtitle = "Дати показу: " + m.show_start + '-' + m.show_end
	else:
		subtitle = "Сеанси: " + m.all_shows_today
	return subtitle


def get_list_attachment(already_out):
	all_movies = Movie.objects.all().filter(already_out=already_out)

	films_elements = []

	element_index = -1
	button_index = 0
	buttons_per_page = 1
	for movie in all_movies:
		if button_index > buttons_per_page - 1 or button_index == 0:
			element_index += 1
			films_elements.append(
				{
					"title": movie.title,
					"buttons": [],
					"image_url": movie.poster,
					"subtitle": get_shows_today(movie)
				}
			)
			button_index = 0

		button = {
			"type": "postback",
			"title": "Деталі",
			"payload": "info " + movie.film_id,
		}
		back_button = {
			"type": "postback",
			"title": "Меню",
			"payload": "start"
		}

		films_elements[element_index]['buttons'].append({})
		films_elements[element_index]['buttons'][button_index] = button
		if buttons_per_page == 1:
			films_elements[element_index]['buttons'].append(back_button)
		button_index += 1

	films = {
		"type": "template",
		"payload": {
			"template_type": "generic",
			"elements": films_elements
		}
	}
	return films


def get_info_page(film_id):
	movie = Movie.objects.get(film_id=film_id)

	format = movie.format

	if not format or format == '':
		format = "Скоро в кінотеатрі Портал!"
	if movie.all_shows_today == 'none' or movie.all_shows_today is None:
		show_start_end = ""
	else:
		show_start_end = "Дати показу: " + movie.show_start + '-' + movie.show_end

	if movie.duration:
		duration = "Тривалість: " + movie.duration + " хвилин" + "\n"
	else:
		duration = ""

	if movie.already_out:
		back_button = {
			'title': "Фільми",
			"type": "postback",
			"payload": "films"
		}
	else:
		back_button = {
			'title': "Анонси",
			"type": "postback",
			"payload": "announcements"
		}

	info = {
		"type": "template",
		"payload": {
			"template_type": "list",
			"top_element_style": "large",
			"elements": [
				{
					"title": movie.title,
					"subtitle": get_shows_today(movie),
					"image_url": movie.poster,
					"default_action":
						{
							"type": "web_url",
							"url": movie.poster,
							"messenger_extensions": False,
							"webview_height_ratio": "compact",
						},

				},
				{
					"title": format,
					"subtitle": show_start_end,
					"buttons": [
						{
							'title': "Трейлер",
							"type": "web_url",
							"url": movie.trailer,
							"messenger_extensions": True,
							"webview_height_ratio": "compact",
						}
					]

				},
				{
					"title": "Країна: " + movie.country,
					"subtitle": ("Актори: " + movie.actors + "\n"),
				},

				{
					"title": "Режисер: " + movie.director + "\n",
					"subtitle": ("Жанри: " + movie.genres + "\n" + duration),
					"buttons": [
						back_button
					]
				}

			]
		}
	}

	return info
