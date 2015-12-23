from mw.xml_dump import Iterator
import codecs
import re
from mwtextextractor import get_body_text

#Open wikipedia dump using mw library
dump = Iterator.from_file(codecs.open("skwiki-20151102-pages-articles.xml", encoding="utf-8"))

#Define Article class for easier work with articles
class Article:
    title = ''
    text = ''
    categories = []
    def __init__(self, title, text, categories):
        self.title = title
        self.text = text
        self.categories = categories

#Define article list
articleList = []
#DEBUG: Iterating through pages stops after pageIterate == stops
pageIterate=0
stops = 150

# Iterate through pages
for page in dump:
    #Iterate through revisions
    for revision in page:
        #Obtain text from first revision of wikipedia article
        textRevision = revision.text
        #Convert text from mw library String to python String
        convertTextRevision = str(revision.text);
        #Delete mediawiki coding (e.g [[]], ==, {{}}) from revision text using mwtextextractor library
        deletedMediaWikiText = get_body_text(convertTextRevision)
        #Split cleared text string into array on lines
        splitedLines = deletedMediaWikiText.splitlines()
        #Define string for processing
        articleText = ''
        #Iterate through lines
        for line in splitedLines:
        	#Filter out empty lines (e.g '')
            if len(line) > 1:
            	#Filter out lines with listed categories from article text
                if bool(re.search('\[Kategória\:([^\]]+)\]',line)) == False:
                	#Filter out remaining mediawiki tags (mostly pictures and their descriptions)
                    line = re.sub('\[\[([^\]]+)\]\]', '', line)
                    #Append filtered line into text string
                    articleText+= line
        #Define categories Array
        categories=[]
        #Using regex find all categories
        matches = re.findall('\[Kategória\:([^\]]+)\]',textRevision,re.DOTALL)
        #Iterate through matches from regex
        for match in matches:
        	#Filter out wrong names of categories (some categories contain '|' character)
            if (ord(match[len(match)-1])) == 32:
                match = match[:-2]
                #Append category into array
                categories.append(match)
            else:
            	#Append category into array
                categories.append(match)
        #Check if article contains any categories
        #If there are no categories for article , we ignore article, otherwise the article is appended into article list
        if len(matches) > 0:
            articleList.append(Article(page.title,articleText,categories))
    #DEBUG: If condition controling number of pages from XML dump to process
    if pageIterate > stops:
        break
    pageIterate+=1

#DEBUG: print number of articles and formatted list of articles 
print(len(articleList))
for article in articleList:
    print(article.title)
    print(article.text)
    for category in article.categories:
        print("Kategória:",category)
    print('==========================')
