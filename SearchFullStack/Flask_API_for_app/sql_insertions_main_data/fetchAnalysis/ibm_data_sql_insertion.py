import sys
import os
from sql_insertions_main_data.fetchAnalysis.local_ibm import ibm_get_sentiment

def get_ibm_sentiment(url, kw):
    raw_res = ibm_get_sentiment(url, kw)
    res = []
    res.append(raw_res['usage']['text_characters'])
    res.append(url)
    res.append(kw)
    if 'sentiment' in raw_res:
        if 'document' in raw_res['sentiment']:
            res.append(raw_res['sentiment']['document']['score'])
            res.append(raw_res['sentiment']['document']['label'])
        else:
            res.append(None)
            res.append(None)
    else:
        res.append(None)
        res.append(None)
    
    if 'emotion' in raw_res:
        if 'document' in raw_res['emotion']:
            res.append(raw_res['emotion']['document']['emotion']['sadness'])
            res.append(raw_res['emotion']['document']['emotion']['joy'])
            res.append(raw_res['emotion']['document']['emotion']['fear'])
            res.append(raw_res['emotion']['document']['emotion']['disgust'])
            res.append(raw_res['emotion']['document']['emotion']['anger'])
        else:
            for i in range(5):
                res.append(None)
    else:
        for i in range(5):
            res.append(None)
    
    if 'keywords' in raw_res:
        tot_kws = len(raw_res['keywords'])
        for i in range(tot_kws):
            temp = raw_res['keywords'][i]
            res.append(temp['text'])
            res.append(temp['sentiment']['score'])
            res.append(temp['relevance'])
        for i in range(5 - tot_kws):
            res.append(None)
            res.append(None)
            res.append(None)
    else:
        for i in range(15):
            res.append(None)
            
    if 'entities' in raw_res:
        tot_ent = len(raw_res['entities'])
        for i in range(tot_ent):
            temp = raw_res['entities'][i]
            res.append(temp['type'])
            res.append(temp['text'])
            res.append(temp['sentiment']['score'])
            res.append(temp['relevance'])
        for i in range(3- tot_ent):
            for j in range(4):
                res.append(None)
    else:
        for i in range(12):
            res.append(None)
    return res   
        
def insert_ibm_sentiment(url, kw, cursor):
    query_insertion = get_ibm_sentiment(url, kw)
    query = (
        "INSERT INTO [search_analysis].[news_sentiment] (total_chars, url, keyword_query, document_sentiment_num, document_sentiment_label, sentiment_sadness, sentiment_joy, sentiment_fear, sentiment_disgust, sentiment_anger, keyword_1, keyword_1_sentiment, keyword_1_relevance, keyword_2, keyword_2_sentiment, keyword_2_relevance, keyword_3, keyword_3_sentiment, keyword_3_relevance, keyword_4, keyword_4_sentiment, keyword_4_relevance, keyword_5, keyword_5_sentiment, keyword_5_relevance, entity_1_type, entity_1_name, entity_1_sentiment, entity_1_relevance, entity_2_type, entity_2_name, entity_2_sentiment, entity_2_relevance, entity_3_type, entity_3_name, entity_3_sentiment, entity_3_relevance)"
        "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"
    )
    cursor.execute(query, query_insertion)
    cursor.execute("SELECT @@IDENTITY AS ID;")
    return cursor.fetchone()[0]