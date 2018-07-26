
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


class PyRiddim:
	""" returns a riddimbase.org search query as a pandas dataframe """

	def __init__(self, q, q_type='riddim', track=False):
		cats = ['artist','tune','riddim','label','year','producer','album']
		self.q = q
		if q_type not in cats:
			print('bad query type')
			return
		self.q_type = q_type
		self.track = track
		self.info = self.r_pull()

	def r_pull(self):
		# search to convert prequery to query
		q1 = ('+').join(self.q.split())
		url0 = f'http://www.riddimbase.org/riddimbase/prequery.php?category={self.q_type}&name={q1}&page=1'

		r = http.request('GET', url0)

		if r.status == 200:
			soup = BeautifulSoup(r.data, 'lxml')
			q2 = soup.find('td', {'class':'info-cell'}).find('a')['href']
			url1 = f'http://www.riddimbase.org/riddimbase/{q2}'

		else:
			print(f'bad status: {r.status}')
			return

		if self.track:
			print(url1)

		# actual search
		r = http.request('GET', url1)

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

			# get page number
			if soup.find('table', {'class':'base'}).find('select', {'class':'formfield'}) is None:
				p = 1
				tr_class = 'info-cell'
			else:
				p = int(soup.find('table', {'class':'base'}).find('select', {'class':'formfield'}).find_all('option')[-1].text)
				tr_class = None

			if self.track:
				print(f'{p} pages')

			# iterate through pages and scrape
			for page in range(1, p+1):

				# pull address
				url2 = f'{url1[:-1]}{page}'
				if self.track:
					print(f'page number: {page}')

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
									d = None if ('&nbsp' in a) else a
								dicto[cat].append(d)

		# converts output to dataframe
		df = pd.DataFrame(dicto)
		return df[['artist', 'tune', 'riddim', 'label', 'year', 'producer' , 'album']]

	def __repr__(self):
		return f'Riddimbase search results for {self.q_type}: \'{self.q}\''