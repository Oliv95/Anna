import discord,logging,re,subprocess,magic

client = discord.Client()
client.login('disbotdisbot@gmail.com','password')

logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

@client.event
def on_message_edit(before,after):
    content = after.content
    if content.startswith('!card'):
        fetch_card(after)

@client.event
def on_message(message):
    content = message.content

    #log message
    if message.channel.is_default_channel():
        user     = message.author.name + ': '
        log_msg  = content+'\n'
        mentions = ""
        for usr in message.mentions:
            mentions += usr.name + ','
        log_msg  = re.sub(r'<.*>',mentions,log_msg)
        with open('main_log.log','a') as f:
            f.write(user + log_msg)
            print("logging")
            print(user + log_msg)

    #exit command
    if content.startswith('!exit') or content.startswith('!sudoku'):
        client.send_message(message.channel, 'killing myself, goodbye cruel world')
        client.logout()

    #echo command
    elif content.startswith('!echo'):
        client.send_message(message.channel, content[5::])

    #card fetch command
    elif content.startswith('!card'):
        fetch_card(message)

@client.event
def on_ready():
    print("logged in as")
    print(client.user.name)
    print(client.user.id)
    print('--------')

def fetch_card(message):
        card_name = message.content[5::]#.strip()
        #card_name = card_name.replace("'","")
        #card_name = card_name.replace(",","")
        #card_name = re.sub(r'\s+',' ',card_name)
        try:
            file_name = magic.get_url(card_name)
            client.send_file(message.channel, file_name)
        except KeyError:
            print(message.channel, 'failed to find card: ' + card_name)
            client.send_message(message.channel, 'failed to find card: ' + card_name)

client.run()
