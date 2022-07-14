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

for i in range( len( links ) ):
    url = main_url + links[i]
    page = requests.get( url ).text
    soup = BeautifulSoup( page, "html.parser" )

    table = soup.find( name = "table", class_ = "znaki" ).tbody
    for image in table.find_all( "img" ):
        images.append( image["src"] )

# print( images )

for i, image_link in enumerate( images ):
    url = main_url + image_link
    response = requests.get( url )
    image_name = "data/" + "img" + str( i + 1 ) + ".png"
    with open( image_name, "wb" ) as file:
        file.write( response.content )

print( "Images are downloaded!" )
