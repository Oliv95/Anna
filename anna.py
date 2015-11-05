import discord,logging,re,subprocess,magic,sys

client = discord.Client()
# if the logging to discord fails, exit
client.login('disbotdisbot@gmail.com','password')
if not client.is_logged_in:
    sys.exit(2)

admins = []

logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

@client.event
def on_message(message):
    content = message.content

    #card fetch command
    if '[' in content:
        fetch_card_cmd(message)

    #exit command
    elif content.startswith('!exit') or content.startswith('!sudoku'):
        if exit_cmd(admins,message):
            sys.exit(0)

    #reboot command
    elif content.startswith('!reboot'):
        client.send_message(message.channel,'attempting to reboot')
        sys.exit(1)

    #echo command
    elif content.startswith('!echo'):
        client.send_message(message.channel, content[5::])

    #log message
    if message.channel.is_default_channel():
        user     = message.author.name + ': '
        log_msg  = content+'\n'
        mentions = ""
        #substitute the users id for their nick in the for the log
        for usr in message.mentions:
            mentions += usr.name + ','
        log_msg  = re.sub(r'<.*>',mentions,log_msg)
        with open('main_log.log','a') as f:
            f.write(user + log_msg)
            print("logging")
            print(user + log_msg)

@client.event
def on_ready():
    read_conf()
    print("admins are: " + str(admins))
    print("logged in as")
    print(client.user.name)
    print(client.user.id)
    print('--------')

def fetch_card_cmd(message):
        '''sends all the cards that appear in the message to discord'''
        file_names = magic.get_filenames(message.content)
        if file_names:
            for file_name in file_names:
                client.send_file(message.channel, file_name)

def exit_cmd(admins,message,logout_msg='killing myself, goodbye cruel world',error_msg = 'fuck off'):
    '''If the author of the message is a admin, the bot will logout of discord otherwise print error msg'''
    if message.author.name.lower() in admins:
        client.send_message(message.channel,logout_msg)
        client.logout()
        return True
    else:
        client.send_message(message.channel, error_msg)
        return False

def read_conf():
    global admins
    f = open('anna.conf')
    admins = f.readline()[7:-1].split(',')
    f.close()

client.run()
