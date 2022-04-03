from flask import Flask, render_template, make_response, request, jsonify
from flask_restful import Api, Resource
from gresults import get_google_results
from bing import get_bing_results
from local_ibm import ibm_get_sentiment
from main_insertion import flask_fetch_data, flask_delete_job
from apscheduler.schedulers.background import BackgroundScheduler
from sql_insertions_main_data.sql_insertion import get_active_schedules, del_active_schedules, insert_keywords_to_db

app = Flask(__name__)
api = Api(app)
sch = BackgroundScheduler()

# Python Restful APIs.
class GetResults(Resource):
    def get(self, keyword, engine):
        print (keyword)
        if engine == 'google':
            return {'google': get_google_results(keyword)}
        elif engine == 'bing':
            return {'bing': get_bing_results(keyword)}
        elif engine == 'both':
            return {'google': get_google_results(keyword), 'bing': get_bing_results(keyword)}
        else:
            return {'error': "Not valid request: Search Engine not mentioned"}

class GetSentiment(Resource):
    def get(self, keyword, url):
        return ibm_get_sentiment(url, keyword)

class PostFetchReq(Resource):
    def post(self):
        data = request.get_json()
        nint = data['interval']
        lkw = data['listKw']
        nres = data['results']
        kwid = data['kwID']
        flask_fetch_data(sch, lkw, nint, nres, kwid)
        return jsonify(
            {
                'message': 'Process has started.'
            },
            201
        )

class GetActiveSchedules(Resource):
    def get(self):
        res = get_active_schedules()
        return jsonify(res)
    
    def post(self):
        data = request.get_json()
        iid = data['jid']
        del_active_schedules(iid)
        flask_delete_job(sch, iid)
        return jsonify(
            {
                'message': 'Schedule Deleted.'
            },
            201
        )

class GetSearchSchedules(Resource):
    def get(self, keyword):
        print (keyword)
        res = get_active_schedules(keyword)
        print (res)
        return jsonify(res)

class GetKeywordIdentifier(Resource):
    def post(self):
        data = request.get_json()
        print (type(data['listKw']))
        print (data)
        insert_keywords_to_db( data['listKw'], data['kwID'] )
        return jsonify(
            {
                'message': 'Stored in Database'
            },
            201
        )
        
# Fetch the results for the given engine.
api.add_resource(GetResults, "/results/<string:keyword>/<string:engine>")
# Fetch the sentiment for a given url.
api.add_resource(GetSentiment, "/sentiment/<string:keyword>/<path:url>")
# Insert the data to the database.
api.add_resource(PostFetchReq, "/fetchdata/")
# Add and remove jobs from the Database.
api.add_resource(GetActiveSchedules, "/activeschedules/")
# Search for running jobs.
api.add_resource(GetSearchSchedules, "/searchschedules/<string:keyword>")
# Insert the keywords into the database with the identifier.
api.add_resource(GetKeywordIdentifier, "/kwpersist/")



if __name__ == "__main__":
    app.run(debug=True)