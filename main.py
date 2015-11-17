import discord,logging,re,subprocess,magic,sys,os,mci,anna
'''
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

    #add a admin
    elif content.startswith('!add'):
        my_id = message.author.id
        to_add = content[4::].strip().split(',')
        ids = []
        for serv in client.servers:
            for user in serv.members:
                if user.name in to_add:
                    if not user.id in ids:
                        ids.append(user.id)
        if add_admins(my_id,ids):
            client.send_message(message.channel, 'admins updated')
        else:
            client.send_message(message.channel, 'not sufficient permissions')

    #remove a admin
    elif content.startswith('!rm'):
        my_id = message.author.id
        to_add = content[3::].strip().split(',')
        ids = []
        for serv in client.servers:
            for user in serv.members:
                if user.name in to_add:
                    if not user.id in ids:
                        ids.append(user.id)
        if rm_admins(my_id,ids):
            client.send_message(message.channel, 'admins updated')
        else:
            client.send_message(message.channel, 'not sufficient permissions')
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
        for l in client.servers:
            for u in l.members:
                print(u.name)

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
'''



def main():
    client = discord.Client()
    bot = anna.Anna(client)

    @client.event
    def on_ready():
        print("admins are: " + str(bot.admins))
        print("head admins are: " + str(bot.head_admins))
        print("logged in as")
        print(client.user.name)
        print(client.user.id)
        print("servers connected to: " + str(client.servers))
        print('--------')

    @client.event
    def on_message(message):
        if message.content.startswith('!echo'):
            client.send_message(message.channel, message.content[5::])

    client.run()

if __name__ == "__main__":
    main()
