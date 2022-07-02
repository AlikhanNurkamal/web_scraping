import pandas as pd
import requests
from bs4 import BeautifulSoup

page = requests.get( "https://github.com/bextens1on" ).text
soup = BeautifulSoup( page, "html.parser" )

article = soup.find( name = "article", class_ = "markdown-body entry-content container-lg f5" )

text = [row.text.strip( ) for row in article.ul if len( row.text.strip( ) ) > 0]
print( text )

# Scraping Apple Stock prices.

import yfinance as yf

apple = yf.Ticker( "AAPL" )
apple_df = apple.history( period = "max" )
apple_df.reset_index( inplace = True )
apple_df.drop( columns = ["Stock Splits"], inplace = True )

print( apple_df.head( ) )
print( apple_df[apple_df["Dividends"] > 0][["Date", "Dividends"]] )
