import newspaper
from newspaper import Article


def data_scrapping(url):
    article = Article(url)
    article.download()
    article.parse()
    print('article parse')
    text = article.text
    print('text var created')
    list_of_par = list(map(str, text.split('\n')))
    print('list made')
    final = []
    for par in list_of_par:
        if len(list(map(str, par.split()))) <= 10 or par[:22]=="This article is about ": #wikipedia hardcoding
            pass
        else:
            z=0
            try:
                for i in range(len(par)):
                    if par[i-z]=='[':
                        o=0
                        while par[i-z+o] != "]":
                            o+=1
                        par = par[:i-z] + par[i-z+o+1:]
                        z+=o
            except:
                pass

            z=0
            try:
                for i in range(len(par)):
                    if par[i-z]=='(':
                        o=0
                        while par[i-z+o] != ")":
                            o+=1
                        par = par[:i-z] + par[i-z+o+1:]
                        z+=o
            except:
                pass

            final.append(par)



    total = ""
    for par in final:
        total += par + " "

    return {"output": total}