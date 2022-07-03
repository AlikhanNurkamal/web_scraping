import requests
from bs4 import BeautifulSoup
import json


# Some values in the dict of movie info contain \n instead of a list of values and
# there are characters such as \xa0, so I define a function to handle these:
def get_content_value( row ):
    if row.find( "li" ):
        return [li.text.strip( ).replace( "\xa0", ' ' ) for li in row.find_all( "li" )]
    else:
        return row.text.replace( "\xa0", ' ' )


page = requests.get( "https://en.wikipedia.org/wiki/List_of_Walt_Disney_Pictures_films" ).text
soup_main = BeautifulSoup( page, "html.parser" )
tables = soup_main.find_all( class_ = "wikitable sortable" )
tables = tables[:-2] # I do not need the last 2 tables.

links = []
for table in tables:
    for i in table.find_all( "i" ):
        if i.a is not None: # There is some italic data that does not have a link, so I
                            # need to check it for None
            links.append( i.a.get( "href" ) )

url = "http://en.wikipedia.org"
movies = list( )

for i, link in enumerate( links ):
    html_page = requests.get( url + link ).text
    soup = BeautifulSoup( html_page, "html.parser" )
    info_box = soup.find( name="table", class_ = "infobox vevent" )

    one_movie = dict( )
    for index, row in enumerate( info_box.find_all( "tr" ) ):
        # print( row )
        if index == 0:
            one_movie["Title"] = row.find( "th" ).text
        elif index == 1 or row is None or row.th is None or row.td is None:
            continue
        else:
            one_movie[row.find( "th" ).get_text( ' ' )] = get_content_value( row.find( "td" ) )

    movies.append( one_movie )

# First way
# with open( "data.json", "w", encoding = "utf-8" ) as file:
#     file.write( json.dumps( movies ) )

# Second way
with open( "data.json", "w", encoding = "utf-8" ) as file:
    json.dump( movies, file, ensure_ascii = False, indent = 4 )
