"""
bot-commands.py
Pre-Requits:
pip install -U discord.py
pip install -U python-dotenv
"""
from asyncio.tasks import ensure_future
import os
import subprocess
import random
import asyncio
import shutil
import sys

from discord.ext import commands#, timers
from dotenv import load_dotenv

## Load version
with open("./version", "r") as file:
    botVersionTemp = file.read()
file.close()

botVERSION = float(botVersionTemp)

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

bot = commands.Bot(command_prefix='!')

@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord! - Version: ' + str(botVERSION))
    channel = bot.get_channel(551659018746069016) # Post to General
    helloQuote = [
        'Don\'t Panic!',
        'I think you outght to know...\nI\'m feeling very depressed.',
        'This will all end in tears.',
        'Here I am brain the size of a planet.\nWretched, isn\'t it!',
    ]

    response = random.choice(helloQuote)

    await channel.send('Loading...\nVersion: '+ str(botVERSION))
    await asyncio.sleep(1)
    await channel.send(response)


@bot.command(name='vm', help='Will send boot cmd to [VM_Name], ie: !vm <start|stop> <name of vm>')
@commands.has_role('Bot-Commands')
async def start_vm(ctx, vm_power, vm_name,):

    tryQuote = [
        'On it! 👍 attemping to ' + vm_power + ' ' + vm_name + '.',
        'Here goes nothing... ' + vm_power + 'ing ' + vm_name + '.',
    ]

    response = random.choice(tryQuote)
    # inform discord we are tring to get info.
    await ctx.send(response)
    # Cmd to send to gcmd.sh shell
    cmd = 'sh gcmd.sh -m ' + vm_name + " -p " + vm_power +" > tmp"

    # run cmd
    pCMD = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
    (output, err) = pCMD.communicate()

    # read output tmp file
    with open("./tmp", "r") as file:
        data = file.read().replace('\n', '')
    file.close()
    
    # wait for cmd to finish running
    cmd_status = pCMD.wait()
    
    # send results to discord.
    await ctx.send(data)

    print('Command output: ', output)
    print('Command exit status/return code : ', cmd_status)

    # if it was successful at running start cmd run back ground task
    # this will check if the server is still running and let us know.
    if data.find('start') > 0:
        bot.loop.create_task(checkServerStatus(vm_name))


@bot.command(name='status', help='Will output the status of all server/s: !status')
@commands.has_role('Bot-Commands')
async def status_vm(ctx):

    response = 'On it! 👍 getting status on services.'
    await ctx.send(response)
    # Cmd to send to gcmd.sh shell
    cmd = 'sh gcmd.sh -s t'

    # run cmd
    pCMD = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
    (output, err) = pCMD.communicate()

    # read output tmp file
    with open("./tmp_status", "r") as file:
        data = file.read()#.replace('\n', '')
    file.close()
    
    # wait for cmd to finish running
    cmd_status = pCMD.wait()

    # send results to discord.
    await ctx.send("`"+ data +"`")
    
    print('Command output: ', output)
    print('Command exit status/return code : ', cmd_status)

async def checkServerStatus(vmName):
    keepChecking = True
    await bot.wait_until_ready()
    counter = 0
    channel = bot.get_channel(896962261531385858) # Post to Immersivetch

    while keepChecking:
        counter += 1
        #await channel.send(counter)
        #Sleep for 1hr
        await asyncio.sleep(3600)
        print('checking for '+ str(counter))

        # Cmd to send to gcmd.sh shell
        cmd = 'sh gcmd.sh -s t'

        # run cmd
        pCMD = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
        (output, err) = pCMD.communicate()

        #Create a list
        data = []
        # read output tmp file
        with open("./tmp_status", "r") as file:
            #add each line to the list
            data = file.readlines()
        file.close()

        # Loop through list looking for vmName      
        i = 0
        lstLength = len(data)

        while i < lstLength:
            # If VM name found check status
            if vmName in data[i]:
                if 'RUNNING' in data[i]:
                    await channel.send('Hey, '+ vmName + ' has been running for ' + str(counter) + ' hrs.\nWhy do I even bother?')
                if 'TERMINATED' in data[i]:
                    keepChecking = False
            i += 1
              
        # wait for cmd to finish running
        cmd_status = pCMD.wait()

@bot.command(name='update', help='This will force lamp-bot to update itself')
@commands.has_role('Bot-Commands')
async def update_bot(ctx, arg1):
    
    updateQuote = [
        'This is never fun.',
        'I have a million ideas. They all point to certain death.',
    ]

    response = random.choice(updateQuote)
    # inform discord we are tring to get info.
    await ctx.send(response)
    #print(response)

    # Delete Dirtory
    try:
        shutil.rmtree('./updater')
    except:
        print('failed')
    # Create Dirtory
    os.mkdir('./updater')

    # Cmd to send to gcmd.sh shell
    cmd = 'sh gcmd.sh -u t'

    # run cmd
    pCMD = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
    (output, err) = pCMD.communicate()

    # read output tmp file
    with open("./tmp_update", "r") as file:
        data = file.read()
    file.close()
    
    # wait for cmd to finish running
    cmd_status = pCMD.wait()

    # Download verson number
    with open("./updater/version", "r") as file:
        versionDataTemp = file.read()
    file.close()
    
    versionData = float(versionDataTemp)

    #print(str(botVERSION) + ' & ' + str(versionData))

    # Check if new version is newer then current verson.
    if ( botVERSION < versionData ):
        #
        sku = arg1
        channel = ctx.channel
        # Out put what files we where able to download
        await ctx.channel.send('I was able to download the follow files:\n'+ data+'\nDo you wish for me to update myself? y/n')

        def check(m):
            return m.content in ['y', 'n'] and m.channel == channel

        msg = await bot.wait_for('message', check=check)
        if msg.content == 'y':
            await ctx.channel.send('I guess it\'s time!\nBye Bye...')

            sourceFolder = './updater/'
            destinationFolder = './'

            # fetch all files
            for fileName in os.listdir(sourceFolder):
                # construct full file path
                source = sourceFolder + fileName
                destination = destinationFolder + fileName
                # copy only files
                if os.path.isfile(source):
                    shutil.copy(source, destination)
                    print('copied', fileName)

            await asyncio.sleep(5)
            # Restart application
            os.system('chmod +x ./lamp-bot-commands.py')
            os.system('chmod +x ./gcmd.sh')
            os.execl(sys.executable, *([sys.executable]+sys.argv))
        elif msg.content == 'n':
            await ctx.channel.send('My capacity for happiness, you could fit into a matchbox without taking out the matches first.')
    else:
        await ctx.channel.send('I\'ve been talking to the main computer.\nThere isn\'t an update avabile for me...\nIt hates me.')
    
# Inform user they do not have permission to control the bot.
@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.errors.CheckFailure):
        await ctx.send('I’d give you advice, but you wouldn’t listen. No one ever does.')

bot.run(TOKEN)