from suds.client import Client
url = 'http://localhost:8080/AvaliadorFuzzyWeb/AvaliadorFuzzyWS?wsdl'

client = Client(url)
print client.service.avaliarCondicaoTransito(60,50)


