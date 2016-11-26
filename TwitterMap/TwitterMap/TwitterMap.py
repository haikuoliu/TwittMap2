import json
import boto3
from snsPrep import create_topic
from multiprocessing import Pool
import httplib, urllib, base64
from watson_developer_cloud import AlchemyLanguageV1
import requests

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

def worker(_):
    while True:
        for message in queue.receive_messages(MaxNumberOfMessages = 10, WaitTimeSeconds = 20):
            try:
                tweet = json.loads(message.body)
                response = json.dumps(alchemy_language.sentiment(text=tweet['text']),indent=2)
                if response['status'] == 'OK':
                    tweet['sentiment'] = response['docSentiment']['type']
                    json_message  = json.dumps(tweet, ensure_ascii = False)
                    topic.publish(Message = json_message)
            finally:
                message.delete()
                

if __name__ == '__main__':
    pool = Pool(3)
    pool.map(worker, range(3))
                        #es.index(index = 'sentitwitter', doc_type = 'tweet', body = ntweet)
                        #esheaders = {'content-type': 'application/json'}
                    #requests.post(esurl, data = json_message, headers = esheaders)