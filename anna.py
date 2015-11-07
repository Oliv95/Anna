import discord,logging,re,subprocess,magic,sys,os,mci

admins = []
email = ""
password = ""

def read_conf():
    global admins
    global email
    global password 
    f = open('anna.conf')
    for line in f.readlines():
        if line.startswith('admins='):
            admins.extend(line[7:-1].split(','))
        elif line.startswith('login='):
            login = line[6:-1].split(',')
            print(str(login))
            email = login[0]
            password = login[1]
    f.close()

read_conf()
client = discord.Client()
# if the logging to discord fails, exit
client.login(email,password)
if not client.is_logged_in:
    sys.exit(2)

logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

@client.event
def on_message_edit(before,after):
    if '[' in after.content:
        fetch_card_cmd(after)

@client.event
def on_message(message):
    if message.author.name == 'Anna':
        return
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
        sys.exit(100)

    #echo command
    elif content.startswith('!echo'):
        client.send_message(message.channel, content[5::])

    #help command
    elif content.startswith('!help'):
        help_text = r"""
                    The following commands and features are available:
                    Echo command will echo back what you typed, example !echo hello Anna
                    Reboot command will cause me to attempt a reboot, example !reboot
                    Exit command will cause me to become very turned off, example !exit (admins only)
                    ------------------------------------------------------------------
                    You can also type the name of a magic card withing square brackets 
                    and have me fetch an image of that card, example [forest]
                    You can also use double square brackets for a search using magiccards.info syntax,
                    example [[o:flashback]] see website for more info. 
                    -------------------------------------------------------------------
                    My source code and licence is available on github.com/Oliv95/Anna"""
        client.send_message(message.channel,help_text)

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
    print("admins are: " + str(admins))
    print("logged in as")
    print(client.user.name)
    print(client.user.id)
    print('--------')

def fetch_card_cmd(message):
        '''sends all the cards that appear in the message to discord'''
        (img_urls,msg) = mci.image_urls(message.content)
        for url in img_urls:
            client.send_message(message.channel,url)
        (file_names,failed) = magic.get_filenames(msg)
        for file_name in file_names:
            client.send_file(message.channel, file_name)
            os.remove(file_name)
            print('done with file: ' + file_name + ' will now delete it')
        for card in failed:
            client.send_message(message.channel, 'Could not find: '+card)

def exit_cmd(admins,message,logout_msg='killing myself, goodbye cruel world',error_msg = 'fuck off'):
    '''If the author of the message is a admin, the bot will logout of discord otherwise print error msg'''
    if str(message.author.id) in admins:
        client.send_message(message.channel,logout_msg)
        client.logout()
        return True
    else:
        client.send_message(message.channel, error_msg)
        return False

def add_admin(id,user_id):
    global admins
    if id in admins and not user_id in admins:
        with open('anna.conf','a') as f:
            f.write('admins='+user_id)
        return True
    else:
        return False

client.run()
