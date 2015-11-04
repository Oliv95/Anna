import json,requests,subprocess,shlex,re

def get_url(msg):
    '''returns file name of the card image file'''
    #puts the name into correct form
    print(msg)
    card_names = re.findall('\[(.*?)\]',msg)
    file_names = []
    for card in card_names:
        card = format_card(card)
        url = 'https://api.deckbrew.com/mtg/cards/' + card
        img_url = 'http://gatherer.wizards.com/Handlers/Image.ashx?multiverseid='
        
        #parse json data from deckbrew
        data = requests.get(url).json()
        editions = []
        try:
            editions = data['editions']
        except KeyError:
            continue
        m_id = 0
        #get the first multiverse id
        m_id = editions[0]
        #try and find a better one
        arbitrary_constant_that_seems_to_work = 10000
        for edition in editions:
            if edition['multiverse_id'] > arbitrary_constant_that_seems_to_work:
                m_id = edition['multiverse_id']
                break
        m_id = str(m_id) + '&type=card'
        file_name = 'image/' + m_id + '.jpg'
        img_url += m_id
        shell_cmd = './dwnMagic.sh ' + file_name + ' ' + img_url
        subprocess.call(shlex.split(shell_cmd))
        print('Done fetching ' + card)
        file_names.append(file_name)
    return file_names


def format_card(card):
        card = card.strip()
        card = card.replace("'","")
        card = card.replace(",","")
        #card = re.sub(r'\s+',' ',card)
        card = " ".join(card.split())
        card = card.replace(' ','-').lower()
        return card
