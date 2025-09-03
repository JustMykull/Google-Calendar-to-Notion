import discord 
import asyncio

TOKEN  = "token"

intents = discord.Intents.default()
client = discord.Client(intents=intents)

logFile = "cronRuns.log"

reminderChannelID = 1412581741973082143
loggingChannelID = 1412589036178112724
statusChannelId = 1411001176316575756

@client.event
async def on_ready():
    
    reminderChannel = client.get_channel(reminderChannelID)
    loggingChannel = client.get_channel(loggingChannelID)
    statusChannel = client.get_channel(statusChannelId)

    print(f"Logged in as {client.user}")
    await statusChannel.send("We up.")

    try: 
        with open(logFile, "r") as f:
            logs = [line.strip() for line in f if line.strip()]
    except FileNotFoundError:
        print("Log not found.")
        logs = []

    if loggingChannel:
        for log in logs:
            await loggingChannel.send(log)
    else:
        print("Channel not found.")

    with open(logFile, "w") as f:
        pass 

    await statusChannel.send("We down.")
    await client.close()

def runBot():
    client.run(TOKEN)

#runBot()
