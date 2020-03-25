#import bibliotek
import requests
from bs4 import BeautifulSoup
import json
import pprint

#adres URL przykładowej strony z opiniami
url_prefix = 'https://www.ceneo.pl'
product_id = input('Podaj kod produktu :')
url_postfix = '#tab=reviews'
url = url_prefix + '/' + product_id + url_postfix

while url:
    #pobranie kodu html strony z podanego URL
    page_respons = requests.get(url)
    page_tree = BeautifulSoup(page_respons.text, 'html.parser')

    #wydobycie z kodu HTML strony fragmentów odpowiadających poszczególnym opiniom
    opinions = page_tree.find_all('li', 'review-box')

    #pusta lista na wszystkie opininie o produkcie
    opinions_list = []
    #wydobycie składowych dla pojedyńczej opinii
    for opinion in opinions:

        opinion_id = opinion['data-entry-id']
        author = opinion.find('div', 'reviewer-name-line')
        try:
            recommendation = opinion.find('div', 'product-review-summary').find('em').string
        except AttributeError:
            recommendation = None
        stars = opinion.find('span', 'review-score-count').string
        try:
            purchased = opinion.find('div', 'product-review-pz').find('em').string
        except AttributeError:
            purchased = None
        dates = opinion.find('span', 'review-time').find_all('time')
        review_date = dates.pop(0)['datetime']
        try:
            purchase_date = dates.pop(0)['datetime']
        except IndexError:
            purchase_date = None
        useful = opinion.find('button', 'vote-yes').find('span').string
        useless = opinion.find('button', 'vote-no').find('span').string
        content = opinion.find('p', 'product-review-body').get_text()
        try:
            pros = opinion.find('div', 'pros-cell').find('ul').get_text()
        except AttributeError:
            pros = None
        try:
            cons = opinion.find('div', 'cons-cell').find('ul').get_text()
        except AttributeError:
            cons = None

        opinion_dict = {
            "opinion_id":opinion_id,
            "recommendation":recommendation,
            "stars":stars,
            "content":content,
            "author":author,
            "pros":pros,
            "cons":cons,
            "useful":useful,
            "useless":useless,
            "purchased":purchased,
            "purchase_date":purchase_date,
            "review_date":review_date
        }
        
        opinions_list.append(opinion_dict)



    try: 
        url = url_prefix + page_tree.find('a', 'pagination__next')['href']
    except TypeError:
        url = None
    print(url)
    
with open(product_id+'.json', 'w') as fp:
    json.dump(opinions_list, fp,  ensure_ascii=False, indent=4, separators=(',',': '))

print(len(opinions_list))
    #pprint.pprint(opinions_list)
        