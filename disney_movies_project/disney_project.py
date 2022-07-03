import json

with open( "data.json", "r" ) as file:
    data = json.load( file )

print( "No. of scraped movies:", len( data ) )

features = set( )
for dictionary in data:
    for key in dictionary.keys( ):
        features.add( key )

print( "No. of unique dictionary keys:", len( features ) )