import mechanize
import BeautifulSoup
import logging
logging.basicConfig(level=logging.DEBUG)
logging.debug('This message should go to the log file')
__author__ = 'Adriaan Stander'
#Try and get valid input
try:
    searchQueryText = raw_input('Enter search term: ')
    #Browser define
    br = mechanize.Browser();
    #Add browser options
    br.set_handle_redirect(True)
    br.set_handle_referer(True)
    br.set_handle_robots(True)
    # Follows refresh 0 but not hangs on refresh > 0
    br.set_handle_refresh(mechanize._http.HTTPRefreshProcessor(), max_time=1)
    #Build the search url with the search term
    searchTermFormated = searchQueryText.replace(" ","+")
    #Requirement is to search for titles thus --'&s=tt'
    searchUrl = 'http://www.imdb.com/find?q='+searchTermFormated+'&s=tt'
    try:
        # The site we will navigate into
        br.open(searchUrl)
        # Read the response with a list of titles using BS4
        html = br.response().read()
        soup = BeautifulSoup(html)
        #find the title
        movieTitlesFound = soup.find_all(class_='result_text')
    except ValueError:
        print('Error reading first page response')
    #Use a counter to limit the amount of movie titles to inspect
    i = 0
    #result variable
    topTenTitleList = ''
    for movieTitle in movieTitlesFound:
        title = ''
        releaseDate = ''
        aka = ''
        if i != 10:
            urlToAppend = movieTitle.a['href']
            movieLink = 'http://www.imdb.com'+urlToAppend
            try:
                #follow the movies link
                br.open(movieLink)
                # read the resulting html via BS so we can get
                # details to print
                html = br.response().read()
                soup = BeautifulSoup(html)
                title = soup.find('title').getText()
                inlineBlocks = soup.find_all(class_='txt-block')
            except ValueError:
                print('Error Reading title link page')
            for inlineBlock in inlineBlocks:
                try:
                    if inlineBlock.h4.getText() == 'Release Date:':
                        releaseDate = inlineBlock.getText()
                        break
                except Exception as e:
                        logging.exception(e)

            topTenTitleList = topTenTitleList + ' {\n title: ' + title + ',\n release date: ' + releaseDate + '\n },\n'
            i += 1


except SyntaxError:
    searchQueryText = None
    print('Enter in valid text!')


movieListToPrint = topTenTitleList[:-2]
print('[\n' + movieListToPrint + '\n]')

