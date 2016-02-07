#Using Flask, see flask.pocoo.org
from flask import Flask, request
app = Flask(__name__)
import threading
import time
import subprocess

anxiety_level = 0 #Yeah it's a "global"
anxlock = threading.Lock() #Synchronisation for anxiety_level

@app.route('/', methods=['GET','POST'])
def anxietyscore():
	'''If GET: return the level, if POST: raise level by one and return it'''
	global anxiety_level
	if request.method == 'GET':
		return str(anxiety_level)
	elif request.method == 'POST':
		anxlock.acquire()
		anxiety_level +=1
		reactToAnxiety(anxiety_level) 
		anxlock.release()
		return str(anxiety_level)

def reactToAnxiety(anxiety_level):
	'''A simple test with the OS X text-to-speech command say'''
	if anxiety_level > 20:
		t = threading.Thread(target=subprocess.call,
			args=[['say', "You need a break"]]) 
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
			anxlock.release()


if __name__ == "__main__":
	anxietyremover = AnxietyRemover()
	anxietyremover.start()
	app.run(host="0.0.0.0")

