from bs4 import BeautifulSoup
import requests

page = requests.get( "http://zarul.kz/pdd/znaki" ).text
soup = BeautifulSoup( page, "html.parser" )

unordered_list = soup.find( name = "div", attrs = { "id" : "book-navigation-11",
                                                    "class" : "book-navigation" } )
unordered_list = unordered_list.ul
all_links = unordered_list.find_all( name = "a" )
links = [i["href"] for i in all_links]

main_url = "http://zarul.kz/"
images = []
labels = []

print( "Getting images links and labels names..." )
for i in range( len( links ) ):
    url = main_url + links[i]
    page = requests.get( url ).text
    soup = BeautifulSoup( page, "html.parser" )

    table = soup.find( name = "table", class_ = "znaki" ).tbody
    for col in table.find_all( "th", class_ = "col_1" ):
        if col.img is None:
            continue
        image = col.img
        # print( image["src"] )
        images.append( image["src"] )

    for col in table.find_all( "th", class_ = ["col_2", "col_2 rowspan"] ):
        labels.append( col.p.text )

# print( images )
# print( labels )
# Some labels contain '\xa0' characters, so I need to delete them.
labels_final = [string.replace( '\xa0', ' ' ).replace( '«', '"' ).replace( '»', '"' ) for string in labels]

print( "Downloading images..." )
for i, image_link in enumerate( images ):
    url = main_url + image_link
    response = requests.get( url )
    image_name = "data/" + "img_" + str( i ) + ".png"
    with open( image_name, "wb" ) as file:
        file.write( response.content )

print( "Download successful!" )

print( "Setting labels..." )

with open( "labels.txt", "w", encoding = "utf8" ) as file:
    file.write( ','.join( labels_final ) )

print( "Everything complete!" )
