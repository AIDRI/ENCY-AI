import wikipedia

def search_on_wikipedia(keywords):
	websites = []
	tmp = ''

	for i in range(len(keywords)-1):
		tmp = keywords[i][1] + ' ' + keywords[i+1][1]
		tmp = wikipedia.search(tmp)[:2]
		for c in tmp:
			if c not in websites:
				websites.append(c)
	
	return websites