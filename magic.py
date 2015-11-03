import json,requests,subprocess,shlex,re

def get_url(card_name):
    '''returns file name of the card image file'''
    #puts the name into correct form
    card_name = card_name.strip()
    card_name = card_name.replace("'","")
    card_name = card_name.replace(",","")
    card_name = re.sub(r'\s+',' ',card_name)
    name = card_name.replace(' ','-').lower()
    url = 'https://api.deckbrew.com/mtg/cards/' + name
    img_url = 'http://gatherer.wizards.com/Handlers/Image.ashx?multiverseid='
    data = None
    valid_card = False
    data = requests.get(url).json()
    editions = data['editions']
    m_id = 0
    #get the first multiverse id
    m_id = editions[0]
    #try and find a better one
    for edition in editions:
        if edition['multiverse_id'] > 10000:
            m_id = edition['multiverse_id']
            break
    m_id = str(m_id) + '&type=card'
    file_name = 'image/' + m_id + '.jpg'
    img_url += m_id
    shell_cmd = './dwnMagic.sh ' + file_name + ' ' + img_url
    subprocess.call(shlex.split(shell_cmd))
    print('Done fetching ' + card_name)
    return file_name
