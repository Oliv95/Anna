import discord,logging,re,subprocess,magic

client = discord.Client()
client.login('disbotdisbot@gmail.com','password')
admins = ['oliv']

logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

@client.event
def on_message(message):
    content = message.content

    #card fetch command is allways tried
    fetch_card_cmd(message)

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
        exit_cmd(message)

    #echo command
    elif content.startswith('!echo'):
        client.send_message(message.channel, content[5::])

@client.event
def on_ready():
    print("logged in as")
    print(client.user.name)
    print(client.user.id)
    print('--------')

def fetch_card_cmd(message):
        #tries to get the image file to send to discord
        #prints error message if card cannot be found
        file_names = magic.get_url(message.content)
        if file_names:
            for file_name in file_names:
                client.send_file(message.channel, file_name)

def exit_cmd(message):
    if message.author.name.lower() in admins:
        client.send_message(message.channel, 'killing myself, goodbye cruel world')
        client.logout()
    else:
        client.send_message(message.channel, 'fuck off')

client.run()
