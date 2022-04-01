from gnews import GNews
from newspaper import Article

def get_google_results(keyword, number_of_results):
    # Initialize the parameters for the Google News handler.
    chosen_country = 'United States'
    chosen_language = 'english'
    results_to_return = number_of_results
    chosen_period = '3d'

    # Change the paramters of the GNews object.
    news_handler = GNews()
    news_handler.country = chosen_country
    news_handler.language = chosen_language
    news_handler.max_results = results_to_return
    news_handler.period = chosen_period
    news_return = news_handler.get_news(keyword)

    temp_list_results = []

    for news in news_return:
        dict_results = {}
        dict_results['keyword'] = keyword
        dict_results['title'] = news['title']
        dict_results['url'] = news['url']
        dict_results['published_date'] = news['published date']
        dict_results['publisher'] = news['publisher']['title']
        dict_results['description'] = news['description']
        temp_list_results.append(dict_results)
    return temp_list_results
