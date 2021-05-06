import wikipedia

def search_on_wikipedia(keywords, lang):
	websites = []
	tmp = ''

	for i in range(len(keywords)-1):
		tmp = str(keywords[i]) + ' ' + str(keywords[i+1])
		tmp = wikipedia.search(tmp)[:2]
		for c in tmp:
			if c not in websites:
				websites.append(c)

	websites_url = []
	for c in websites:
		article = c
		article = article.replace(' ', '_')
		tmp = "https://" + lang + '.wikipedia.org/wiki/' + article
		websites_url.append(tmp)

	return websites_url