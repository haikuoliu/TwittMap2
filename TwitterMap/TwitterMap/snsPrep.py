import boto3

sns = boto3.resource('sns')


# When called repeatedly, the existing topic will be returned
def create_topic():
    # Creates a topic to which notifications can be published.
    topic = sns.create_topic(Name='SentimentTwitterMap_Test')
    return topic


def subscribe(topic):
    # Subscribe end-point to the topic we just created.
    topic.subscribe(Protocol='http', Endpoint='http://54.165.79.233:5000/sns')
    #   Change the endpoint ip address if not run on localhost


if __name__ == '__main__':
    topic = create_topic()
    subscribe(topic)
