# Project-03 CSCI 40

## Webscrapping ebay

The ebay-dl.py file utilizes the bs4, argparse, and requests libraries in order to loop through ebay's HTML files for a user-inputted search term. Using CSS selectors, specific pieces of listing information are pulled into dictionary entries (e.g. price, shipping, items sold, etc). Afterwards, Each respective dictionary is appended into a list called 'items'. To see the instructions, follow this [link](https://github.com/mikeizbicki/cmc-csci040/tree/2022fall/project_03). 

## How to run the code on the ebay-dl.py file
In terms of running this file with any search term, the code you need to type in the terminal would be:
```
$python ebay-dl.py "search term"
```
(Keep in mind that search terms with spaces have to be in quotaions.)
 <br />
 <br />
To run the specific search terms I have selected for this project, the code would be:
```
$python ebay-dl.py screwdriver
```
```
$python ebay-dl.py "pokemon card"
```
```
$python ebay-dl.py "porsche 911"
```

By default, the code will download the first 10 pages of your search term. However, By adding `--page_number` infront of your search term, you may select the specific number of pages you want to download to your JSON file.

