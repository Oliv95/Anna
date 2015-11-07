import urllib.request,re

def image_urls(msg):
    '''returns a list of filenames for all cards that appear in the msg'''
    #get all of the potential card names
    card_names = re.findall('\[\[(.*?)\]\]',msg)
    file_names = []
    for card in card_names:
        card = format_card(card)
        url = 'http://magictcgprices.appspot.com/api/images/imageurl.json?cardname='+card
        card_url = urllib.request.urlopen(url).read()
        file_names.append(card_url[2:-2].decode("utf-8"))
    return file_names,remove_doubles(msg,card_names)

def format_card(card):
        '''puts the card name into the correct form for gather'''
        card = card.strip()
        card = "%20".join(card.split())
        return card.lower()

def remove_doubles(msg,cardnames):
    cardnames = ['[['+card+']]' for card in cardnames]
    for card in cardnames:
        msg = msg.replace(card,'')
    return msg
