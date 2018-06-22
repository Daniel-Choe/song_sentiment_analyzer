import requests
import pprint as pp
import numpy as np

from config import config

# IMPORT GLOBALS
API_KEY = config['API_KEY']
REQUEST_BODY = config['REQUEST_BODY']


def get_sentiment_score(text='', key=None):
	"""This will make a request to the Google Natural Language API to
	determine the sentiment score and magnitude of a given text

	Args:
		text (str): string representing the lyrics/text we want to score
		key (google.oauth2.credentials): api key for Natural Language API
	Returns:
		r (dict/json) : JSON response from Google's Natural Language API
	"""
	REQUEST_BODY['document']['content'] = text.encode('cp1252').decode('utf-8')
	print('-'*80)
	print(text)
	print('-'*80)

	if key is None:
		print('No key configured ')
		return None
	elif text is '':
		print('No text was inputted')
		return None
	else:
		r = requests.post(
			'https://language.googleapis.com/v1/documents:analyzeSentiment',
			params={'key': key},
			json=REQUEST_BODY
		)
		return r.json()


def read_song(file):
	"""This will read the song text file and parse it into a list of strings.
	The function will remove all empty strings, and tags

	Args:
		file (str): str representing file object location.
	Returns:
		lyrics (list of str): ordered list of strings representing the lyrics
	"""

	with open(file, 'r') as f:
		tmp = f.read().split('\n')
		tmp = [val for val in tmp if val != '' and '[' not in val]

	return tmp


if __name__ == '__main__':
	print('-' * 80)
	print('Reading in lyrics for Sky\'s the Limit by Notorious B.I.G.')
	print('-'*80)

	lyrics = read_song('lyrics.txt')
	scores = []
	for line in lyrics:
		resp = get_sentiment_score(line, key=API_KEY)
		scores.append((resp['documentSentiment']['score'],
			resp['documentSentiment']['magnitude']))

	print('From parsing {} lines in this Sky\'s the Limit by Notorious B.I.G.'.
		format(len(scores)))

	avg_score = np.mean([val[0] for val in scores])
	avg_magn = np.mean([val[1] for val in scores])
	print('We determined that the overall average sentiment score was {}'
		.format(avg_score))
	print('and the average sentiment magnitude was {}'.format(avg_magn))
	print('The combined metric is {}'.format(avg_score*avg_magn))
	metric = avg_magn * avg_score
	if metric < 0:
		print('This song expresses negative sentiments')
	elif metric > 0:
		print('This song expresses positive sentiments')
	else:
		print('The results are inconclusive..')

