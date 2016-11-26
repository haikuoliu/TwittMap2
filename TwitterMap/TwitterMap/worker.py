import json
import boto3
from snsPrep import create_topic
from elasticsearch import Elasticsearch,RequestsHttpConnection
from multiprocessing import Pool
import httplib, urllib, base64
from watson_developer_cloud import AlchemyLanguageV1
from requests_aws4auth import AWS4Auth
import requests
import urllib2

headers = {
    # Request headers
    'Content-Type': 'application/json',
    'Ocp-Apim-Subscription-Key': '{511759357b824ccc8b8336b6ebba9ad7}',
}

sqs = boto3.resource('sqs')
queue = sqs.get_queue_by_name(QueueName='Erinyes')
sns = boto3.resource('sns')
topic = create_topic()

alchemy_language = AlchemyLanguageV1(api_key='6de8f373d9e238ea73e7c2d737cc0ab4effb0079')
url = 'https://gateway-a.watsonplatform.net/calls'

host = 'search-twitter-1-kf5qeriqw5iu6uasbyv6dmwfbq.us-west-2.es.amazonaws.com'
awsauth = AWS4Auth('AKIAIJZRV3JVJ5SIFUXQ', 'IZmZqgDYeE8wn2Onu7y7UNf3WnHDdV8AQzA+SUeS', 'us-west-2', 'es')

es = Elasticsearch(
    hosts=[{'host': host, 'port': 443}],
    http_auth=awsauth,
    use_ssl=True,
    verify_certs=True,
    connection_class=RequestsHttpConnection
)
print(es.info())
try:
    es.indices.create(index='sentitwitter', ignore=400)
except Exception, e:
    pass

def worker(_):
    while True:
        for message in queue.receive_messages(MaxNumberOfMessages = 10, WaitTimeSeconds = 20):
            try:
                tweet = json.loads(message.body)
                response = json.dumps(alchemy_language.sentiment(text=tweet['text']), indent = 2)
                responseDict = json.loads(response)
                if responseDict['status'] == 'OK':
                    tweet['sentiment'] = responseDict['docSentiment']['type']
                    #json_message = json.dumps(tweet)
                    json_message  = json.dumps(tweet, ensure_ascii = False)
                    #topic.publish(Message = json_message)
                    es.index(index = 'sentitwitter', doc_type = 'tweet', body = tweet)

            finally:
                message.delete()

if __name__ == '__main__':
    pool = Pool(3)
    pool.map(worker, range(3))

