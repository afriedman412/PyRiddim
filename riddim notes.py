
from bs4 import BeautifulSoup
import pandas as pd
import requests
import urllib3
import certifi

"""PyRiddim.py: Unofficial Python API for accessing data from riddimbase.org."""

__author__     = "Andy Friedman"
__license__    = "n/a"
__maintainer__ = "Andy Friedman"
__email__      = "afriedman412@gmail.com"

HEADERS = {
	'User-Agent': 'PyRiddim.py (https://github.com/afriedman412/PyRiddim)'
}

http = urllib3.PoolManager(cert_reqs='CERT_REQUIRED', ca_certs=certifi.where())

def riddim_search(q, q_type='riddim'):
	q1 = ('+').join(q.split())
	url = f'http://www.riddimbase.org/riddimbase/prequery.php?category={q_type}&name={q1}&page=1'

	r = http.request('GET', url)

	if r.status == 200:
		soup = BeautifulSoup(r.data, 'lxml')
		q2 = soup.find('td', {'class':'info-cell'}).find('a')['href']
		url2 = f'http://www.riddimbase.org/riddimbase/{q2}'
		return url2

	else:
		print(f'bad status: {r.status}')
		return

def  riddim_scrape(q, q_type='riddim', track=False):
	url = riddim_search(q, q_type)
	if track:
		print(url)

	r = http.request('GET', url)

	if r.status == 200:
		soup = BeautifulSoup(r.data, 'lxml')

		# initialize outut
		dicto = {
			'artist':[],
			'tune':[],
			'riddim':[],
			'label':[],
			'year':[],
			'producer':[],
			'album':[]
		}

		cats = ['artist','tune','riddim','label','year','producer','album']

		# get page number
		if soup.find('table', {'class':'base'}).find('select', {'class':'formfield'}) is None:
			p = 1
			tr_class = 'info-cell'
		else:
			p = int(soup.find('table', {'class':'base'}).find('select', {'class':'formfield'}).find_all('option')[-1].text)
			tr_class = None

		if track:
			print(f'{p} pages')
			print(tr_class)

		# iterate through pages and scrape
		for page in range(1, p+1):

			# pull address
			url2 = f'{url[:-1]}{page}'
			if track:
				print(url2)

			# set call
			r2 = http.request('GET', url2)
			soup2 = BeautifulSoup(r2.data, 'lxml')

			if r2.status == 200:
				for row in soup2.find('table', {'class':'base'}).find_all('tr', {'class':tr_class}):
					if row.find('td', {'colspan':8}) is None:
						for cat, cell in zip(cats, row.find_all('td')):
							if cell.find('a') is not None:
								a = []
								for c in cell.find_all('a'):
									a.append(c.text)
								d = ' & '.join(a)
							else:
								a = cell.text
								d = None if a == '&nbsp' else a
							dicto[cat].append(d)

	df = pd.DataFrame(dicto)
	return df[['artist', 'tune', 'riddim', 'label', 'year', 'producer' , 'album']]




