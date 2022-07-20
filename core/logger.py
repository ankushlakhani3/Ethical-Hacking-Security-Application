from core.colors import *
from datetime import datetime

class Logger:

	@classmethod
	def info(self,text):
		print("["+Y+datetime.now().strftime("%H:%M:%S")+N+"] ["+G+"INFO"+N+"] "+text)

	@classmethod
	def warning(self,text):
		print("["+Y+datetime.now().strftime("%H:%M:%S")+N+"] ["+Y+"WARNING"+N+"] "+text)

	@classmethod
	def high(self,text):
		print("["+Y+datetime.now().strftime("%H:%M:%S")+N+"] ["+R+"CRITICAL"+N+"] "+text)
	@classmethod
	def error(self,text):
		print("["+Y+datetime.now().strftime("%H:%M:%S")+N+"] ["+R+"ERROR"+N+"] "+text)