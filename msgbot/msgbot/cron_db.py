from fb_bot.parser.parser import fill_db


def timed_job():
	fill_db()
	print("Flushing and filling the database")