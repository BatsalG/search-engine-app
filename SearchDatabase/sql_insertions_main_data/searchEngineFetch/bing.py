import requests
from bs4 import BeautifulSoup
from newspaper import Article
from .convert_date_bing import date_bing

def get_bing_results(keyword, number_of_results = 10):
    # Return a list of dict
    # * Title, Url, Description, Search Engine Name, Date
    page = requests.get('https://www.bing.com/news/search?q='+ keyword +'&cc=US')
    soup = BeautifulSoup(page.content, 'html.parser')
    result_title = soup.find_all('div', class_='t_t')
    result_desc = soup.find_all('div', class_='snippet')
    result_link = soup.find_all('a', class_='title')
    result_source = soup.find_all('div', class_='source')
    temp_list_results = []
    
    if len(result_title) > number_of_results:
        ret_nums = number_of_results
    else:
        ret_nums = len(result_title)
    
    for i in range(ret_nums):
        dict_results = {}
        dict_results['keyword'] = keyword
        dict_results['title'] = result_title[i].get_text()
        dict_results['url'] = result_link[i]['href']
        date_ = result_source[i].findChildren("span")[2].get_text()
        date_published = date_bing(date_)
        dict_results['published_date'] = date_published
        dict_results['publisher'] = result_source[i].findChild().get_text()
        dict_results['description'] = result_desc[i].get_text()
        temp_list_results.append(dict_results)
    return temp_list_results