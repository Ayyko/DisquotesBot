import discord


client = discord.Client()

@client.event
async def on_ready():
    print("Connected!\n\nServer List\n-----------")
    for server in client.servers():
        # Print serve list
        print("{:>30} | {}".format(server.name[:30], server.id))


@client.event
async def on_server_join(server):
    # TODO: add servers to a list probably

    await client.send_message(server.default_channel, "Hello! I am the official disquotes bot.\nI was invited by {name}"
                                                      " to help your server submit quotes to `discord.es`.\nIf I am not"
                                                      " wanted, simply kick me. Otherwise, a user with 'Manage Role' "
                                                      "permission can say '@Disquotes setup` to set me up for your "
                                                      "server.")  # TODO: figure out a way to replace {name}, actually impliment register command


@client.event
async def on_message(message):
    pass  # TODO: on_message
