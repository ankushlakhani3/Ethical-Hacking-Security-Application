from core.colors import W
from core import logger
from core import config
import random
payload_level = 6
def check(payload):
	FUNCTION=[
			"prompt(5000/200)",
			"alert(6000/3000)",
			"alert(document.cookie)",
			"prompt(document.cookie)",
			"console.log(5000/3000)"
		]
	if payload == "":
		payload="<script/>"+FUNCTION[random.randint(0,4)]+"<\script\>"
	return payload

def wordlist(payload_list):
	with open(payload_list) as pfile:
		payloads = pfile.read().splitlines()
	return payloads