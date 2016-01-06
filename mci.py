import urllib.request,re

def image_urls(msg):
    '''returns a list of filenames for all cards that appear in the msg'''
    #get all of the potential card names
    card_names = re.findall('\[\[(.*?)\]\]',msg)
    exact_names = re.findall(r'(?<!\[)\[(.*?)\](?!\])', msg)
    f = lambda x: not x.startswith('[')
    exact_names = list(filter(f,exact_names))
    exact_names = ['!'+s for s in exact_names]
    file_names = []
    for card in card_names:
        get_card(card,file_names)
    for card in exact_names:
        get_card(card,file_names)
    return file_names

def get_card(card,file_names):
    basics = ['forest','island','plains','swamp','mountain']
    card = format_card(card)
    url = 'http://magictcgprices.appspot.com/api/images/imageurl.json?cardname='+card
    card_url = urllib.request.urlopen(url).read()[2:-2]
    card_url = card_url.decode("utf-8")
    print('fetching card: '+card)
    if not card_url:
        return
    print('@ url : '+card_url)
    file_names.append(card_url)
    if (not card in basics) and is_doubleface(card_url):
        file_names.append(otherside(card_url))

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

def is_doubleface(card_url):
    return str(card_url[-5]).isalpha()

def otherside(card_url):
    side = ""
    if card_url[-5] == 'a':
        side = 'b.jpg'
    else:
        side = 'a.jpg'
    return card_url[:-5:]+side
