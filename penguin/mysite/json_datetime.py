import datetime, time


def dt_to_milliseconds(dt):
	return time.mktime(dt.timetuple())*1000

	
def milliseconds_to_dt(milliseconds):
	return datetime.datetime.fromtimestamp(milliseconds/1000.0)
