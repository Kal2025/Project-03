import argparse
import requests
from bs4 import BeautifulSoup
import json

def parse_itemssold(text):
    '''
    Takes as input a string and returns the number of items sold, as specified in the string.

    >>> parse_itemssold('38 sold')
    38
    >>> parse_itemssold('14 watchers')
    0
    >>> parse_itemssold('Almost gone')
    0
    '''
    numbers = ''
    t = text.lower()
    for char in text:
        if char in '1234567890':
            numbers += char
    if 'sold' in t:
        return int(numbers)
    else:
        return int(0)

def parse_price(text):
    '''
    >>> parse_price('$8.99')
    899
    >>> parse_price('$7.08')
    708
    >>> parse_price('$11.20')
    1120
    '''
    n = ''
    for c in text:
        if c in '1234567890':
            n += c
    if '$' in text:
        n = int(n)
        return n
    
def parse_shipping(text):
    '''
    >>> parse_shipping('Free shipping')
    0
    >>> parse_shipping('+$2.00 shipping')
    200
    >>> parse_shipping('+$10.80 shipping')
    1080
    '''
    n = ''
    for x in text:
        if x in '1234567890':
            n += x
    if '$' in text:
        n = int(n)
        return n
    elif 'Free' in text:
        return 0

# this if statement says only run the code below whenn the python file is run "normaly"
# where normally means not in the doctests
if __name__ == '__main__':


    # get command line arguments
    parser = argparse.ArgumentParser(description='Download information from ebay and convert to JSON.')
    parser.add_argument('search_term')
    parser.add_argument('--num_pages', default=10)
    args = parser.parse_args()
    print('args.search_term=', args.search_term)

    # list of all items found in all ebay webpages
    items = []

    # loop over the ebay webpages
    for page_number in range(1,int(args.num_pages)+1):

        # build the url
        url = 'https://www.ebay.com/sch/i.html?_from=R40&_nkw=' 
        url += args.search_term
        url += '&_sacat=0&LH_TitleDesc=0&_pgn='
        url += str(page_number)
        url += '&rt=nc'
        #print('url=',url)

        # dowload the html
        r = requests.get(url)
        status = r.status_code
        #print('status=' , status)
        
        html = r.text

        # process the html 
        
        soup = BeautifulSoup(html, 'html.parser')

        # loop over the items in the page
        tags_items = soup.select('.s-item')
        for tag_item in tags_items[1:]: #slice used here to remove 'Shop on Ebay' part
        
            name = None
            tags_name = tag_item.select('.s-item__title')
            for tag in tags_name:
                name = tag.text

            freereturns = False    
            tags_freereturns = tag_item.select('.s-item__free-returns')
            for tag in tags_freereturns:
                freereturns = True

            items_sold = None
            tags_itemssold = tag_item.select('.s-item__hotness')
            for tag in tags_itemssold:
                items_sold = parse_itemssold(tag.text)

            status = False
            tags_status = tag_item.select('.SECONDARY_INFO')
            for tag in tags_status:
                itemstatus = tag.text

            price = None
            tags_price = tag_item.select('.s-item__price')
            for tag in tags_price:
                price = parse_price(tag.text)

            shipping = None
            tags_shipping = tag_item.select('.s-item__shipping')
            for tag in tags_shipping:
                shipping = parse_shipping(tag.text)

            

            item = {
                'name': name, 
                'free_returns': freereturns,
                'items_sold': items_sold,
                'status': itemstatus,
                'price': price,
                'shipping':shipping

            }
            items.append(item)

            for item in items:
                print('item=', item)
                
        #print('len(tag_items)=',len(tags_items))
        #print('len(items)=',len(items))

    # write the json to a file
    filename = args.search_term+'.json'
    with open(filename, 'w', encoding='ascii') as f:
        f.write(json.dumps(items)) 