import requests

def joke():
    response = requests.get("https://geek-jokes.sameerkumar.website/api?format=json")
    jokes = response.json()
    return jokes.get('joke')


def tronalddump():
    response = requests.get("https://api.tronalddump.io/random/quote")
    quotes = response.json()
    #print(quotes)
    return quotes.get('value')

tronalddump()