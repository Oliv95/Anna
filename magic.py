import json,requests,subprocess,shlex,re
import urllib.request

def get_filenames(msg):
    '''returns a list of filenames for all cards that appear in the msg'''
    #get all of the potential card names
    card_names = re.findall('\[(.*?)\]',msg)
    file_names = []
    failed_matches = []
    for card in card_names:
        card = format_card(card)
        print(card)
        url = 'https://api.deckbrew.com/mtg/cards/' + card
        img_url = 'http://gatherer.wizards.com/Handlers/Image.ashx?multiverseid='
        m_id = get_m_id(card)
        if not m_id:
            failed_matches.append(card)
            continue
        img_url += m_id
        img_url += '&type=card&.jpg'
        file_name = card+'.jpg'
        dwnl_img(img_url,file_name)
        file_names.append(file_name)
    failed_matches = [s.replace('+',' ') for s in failed_matches]
    return (file_names,failed_matches)

def format_card(card):
        '''puts the card name into the correct form for gather'''
        card = card.strip()
        card = "+".join(card.split())
        return card.lower()

def get_m_id(card_name):
    try:
        page = urllib.request.urlopen("http://gatherer.wizards.com/Pages/Card/Details.aspx?name="+card_name).read()
        m_id = re.search("multiverseid=([0-9]*)", str(page)).group(1)
        return m_id
    except AttributeError:
        return False

def dwnl_img(img_url,file_name):
    shell_cmd = './dwnMagic.sh ' + file_name + ' ' + img_url
    subprocess.call(shlex.split(shell_cmd))
    print('done fetching card')
