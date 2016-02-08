#Using Flask, see flask.pocoo.org
from flask import Flask, request, Response
app = Flask(__name__)
import threading
import time
import subprocess

anxiety_level = 0 #Yeah it's a "global"
anxlock = threading.Lock() #Synchronisation for anxiety_level
useralerts = ["You need a break", "Seriously, stop.", "You need professional help"]
alertsactivated = [False for alert in useralerts] 

@app.route('/', methods=['GET','POST'])
def anxietyscore():
	'''If GET: return the level, if POST: raise level by one and return it'''
	global anxiety_level
	if request.method == 'GET':
		return Response(str(anxiety_level), mimetype="text/plain")
	elif request.method == 'POST':
		anxlock.acquire()
		anxiety_level +=1
		reactToAnxiety(anxiety_level) 
		anxlock.release()
		return Response(str(anxiety_level), mimetype="text/plain")

def reactToAnxiety(anxiety_level):
	'''A simple test with the OS X text-to-speech command say'''
	for i, alerts in enumerate(useralerts):
		if (anxiety_level > 20+i*10 and not alertsactivated[i]):
			alertsactivated[i] = True
			t = threading.Thread(target=subprocess.call,
				args=[['say', useralerts[i]]]) 
			t.start()

class AnxietyRemover(threading.Thread):
	'''Decrease anxiety_level over time'''
	global anxiety_level
	def __init__(self):
		super(AnxietyRemover,self).__init__()
		self.daemon=True
	def run(self):
		global anxiety_level
		while True:
			time.sleep(0.5)
			anxlock.acquire()
			if anxiety_level > 0:
				anxiety_level -=1
			for i in range(len(useralerts)):
				if (alertsactivated[i] and anxiety_level < 10+i*10):
					alertsactivated[i]=False
			anxlock.release()


if __name__ == "__main__":
	anxietyremover = AnxietyRemover()
	anxietyremover.start()
	app.run(host="0.0.0.0")

