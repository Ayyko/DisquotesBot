import discord


client = discord.Client(max_messages=1000)

@client.event
async def on_ready():
    global setup
    setup = {}  # TODO: load setup from file(maybe change from setup{} to server{}?
    print("Connected!\n\nServer List\n-----------")
    for server in client.servers():
        # Print serve list
        print("{:>30} | {}".format(server.name[:30], server.id))


@client.event
async def on_server_join(server):
    global setup
    # TODO: add servers to a list probably (saved to file?)

    await client.send_message(server.default_channel, "Hello! I am the official disquotes bot.\nI was invited by {name}"
                                                      " to help your server submit quotes to `discord.es`.\nIf I am not"
                                                      " wanted, simply kick me. Otherwise, a user with 'Manage Role' "
                                                      "permission can say '@Disquotes setup` to set me up for your "
                                                      "server.")  # TODO: figure out a way to replace {name}
    setup[server] = False


@client.event
async def on_message(message):
    global setup
    if client.user in message.mentions and "setup" in message.content and not setup[message.server]:
        setup[message.server] = "progress"
        client.send_message(message.author, "first of all, what would you like to prefix my commands with in this "
                                            "server?(use \s for spaces)\nExamples: '!' would allow commands to be run "
                                            "like '!quote', 'dq/s' wpuld allow 'dq quote'")  # TODO: rest of setup

@client.event
async def on_message_edit(before, after):
    pass  # TODO: save these temporarily? I was thinking ~50 in memory from each server.

@client.event
async def on_message_delete(message):
    pass  # TODO: See on_message_edit

@client.event
async def on_channel_create(channel):
    pass  # TODO: Less pertinent than message changes, was thinking maybe ~10 in memory. Save channel deletes?

@client.event
async def on_channel_update(before, after):
    pass  # TODO: See on_channel_create
@client.event
async def on_member_join(member):
    pass  # TODO: Save ~50 of these in memory?

@client.event
async def on_member_remove(member):
    pass  # TODO: See on_member join

@client.event
async def on_member_update(member):
    pass  # TODO: Save ~50, for things like role changes, name changes, ame status, etc

@client.event
async def on_server_update(before, after):
    pass  # TODO: Save ~10 not much happens here

@client.event
async def on_server_role_create(server, role):
    pass  # TODO: Save ~10 not much happens here

@client.event
async def on_server_role_delete(server, role):
    pass  # TODO: See on_server_role_create

@client.event
async def on_server_role_update(before, after):
    pass  # TODO: See on_server_role_create

@client.event
async def on_voice_state_update(before, after):
    pass  # TODO: save ~10 not much happens here

@client.event
async def on_member_ban(member):
    pass  # TODO: save ~20

@client.event
async def on_member_unban(server, user):
    pass  # TODO: save ~20

# Should we do on_typing?

def get_msg(message):
    return {
        "author": {
            "id": message.author.id,
            "name": message.author.name,
            "discrim": message.author.discriminator,
            "avater": message.author.avater_url,
            "color": ""  # TODO: Are roles in a particular order? or do we have to check perms for likely highest role then get that color?
        },
        "content": message.content,
        "time": message.timestamp  # TODO: datetime.timestamp()?
    }
