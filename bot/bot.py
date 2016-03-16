import inspect
import traceback
import asyncio
import discord

from .exceptions import CommandError
# from .constants import CONSTANTS_HERE
# from .utils import write_file, OTHER_UTIL_STUFF_HERE
VERSION = '0.0'


class Response(object):
    def __init__(self, content, reply=False, delete_after=0):
        self.content = content
        self.reply = reply
        self.delete_after = delete_after


class Bot(discord.Client):
    def __init__(self):
        super().__init__()
        self.prefix = '!'
        self.email = 'EMAIL HERE'
        self.password = 'PASSWORD HERE'

    # noinspection PyMethodOverriding
    def run(self):
        loop = asyncio.get_event_loop()
        try:
            # HANDLES BACKGROUND TASKS vv
            # task = loop.create_task(self.background_task())
            loop.run_until_complete(self.start(self.email, self.password))
            loop.run_until_complete(self.connect())
        except Exception as e:
            print(e)
            loop.run_until_complete(self.close())
        finally:
            # UNCOMMENT TO HANDLE BACKGROUND TASKS
            # task.cancel()
            # try:
            #     loop.run_until_complete(task)
            # except Exception:
            #     pass
            loop.close()

    async def on_ready(self):
        print('Connected!\n')
        print('Username: %s' % self.user.name)
        print('Bot ID: %s' % self.user.id)

        if self.servers:
            print('--Server List--')
            [print(s) for s in self.servers]
        else:
            print("No servers have been joined yet.")

        print()

    async def _wait_delete_msg(self, message, after):
        await asyncio.sleep(after)
        await self.safe_delete_message(message)

    async def safe_send_message(self, dest, content, *, tts=False, expire_in=0, quiet=False):
        try:
            msg = None
            msg = await self.send_message(dest, content, tts=tts)

            if msg and expire_in:
                asyncio.ensure_future(self._wait_delete_msg(msg, expire_in))

        except discord.Forbidden:
            if not quiet:
                print("Error: Cannot send message to %s, no permission" % dest.name)
        except discord.NotFound:
            if not quiet:
                print("Warning: Cannot send message to %s, invalid channel?" % dest.name)
        finally:
            if msg: return msg

    async def safe_delete_message(self, message, *, quiet=False):
        try:
            return await self.delete_message(message)

        except discord.Forbidden:
            if not quiet:
                print("Error: Cannot delete message \"%s\", no permission" % message.clean_content)
        except discord.NotFound:
            if not quiet:
                print("Warning: Cannot delete message \"%s\", message not found" % message.clean_content)

    async def safe_edit_message(self, message, new, *, expire_in=0, send_if_fail=False, quiet=False):
        try:
            msg = None
            msg = await self.edit_message(message, new)

            if msg and expire_in:
                asyncio.ensure_future(self._wait_delete_msg(msg, expire_in))

        except discord.NotFound:
            if not quiet:
                print("Warning: Cannot edit message \"%s\", message not found" % message.clean_content)
            if send_if_fail:
                if not quiet:
                    print("Sending instead")
                msg = await self.safe_send_message(message.channel, new)
        finally:
            if msg: return msg


    async def handle_restart(self, channel, author):
        """
        Usage: {command_prefix}logout
        Forces a logout
        """
        await self.logout()


    async def handle_command(self, message, author, required_var, optional_var=None):
        """
        Usage {command_prefix}clean amount
        Removes [amount] messages the bot has posted in chat.
        """
        if not optional_var:
            raise CommandError('this is actually not optional')
        return Response('dope', reply=True)
        pass



    async def on_message(self, message):
        if message.author == self.user:
            return

        if message.channel.is_private:
            await self.send_message(message.channel, 'You cannot use this bot in private messages.')
            return

        message_content = message.content.strip()
        if not message_content.startswith(self.prefix):
            return

        command, *args = message_content.split()
        command = command[len(self.prefix):].lower().strip()

        handler = getattr(self, 'handle_%s' % command, None)
        if not handler:
            return

        print("[Command] {0.id}/{0.name} ({1})".format(message.author, message_content))

        argspec = inspect.signature(handler)
        params = argspec.parameters.copy()

        # noinspection PyBroadException
        try:
            handler_kwargs = {}
            if params.pop('message', None):
                handler_kwargs['message'] = message

            if params.pop('channel', None):
                handler_kwargs['channel'] = message.channel

            if params.pop('author', None):
                handler_kwargs['author'] = message.author

            if params.pop('player', None):
                handler_kwargs['player'] = await self.get_player(message.channel)

            args_expected = []
            for key, param in list(params.items()):
                doc_key = '[%s=%s]' % (key, param.default) if param.default is not inspect.Parameter.empty else key
                args_expected.append(doc_key)

                if not args and param.default is not inspect.Parameter.empty:
                    params.pop(key)
                    continue

                if args:
                    arg_value = args.pop(0)
                    handler_kwargs[key] = arg_value
                    params.pop(key)

            if params:
                docs = getattr(handler, '__doc__', None)
                if not docs:
                    docs = 'Usage: {}{} {}'.format(
                        self.prefix,
                        command,
                        ' '.join(args_expected)
                    )

                docs = '\n'.join(l.strip() for l in docs.split('\n'))
                await self.send_message(
                    message.channel,
                    '```\n%s\n```' % docs.format(command_prefix=self.prefix)
                )
                return

            response = await handler(**handler_kwargs)
            if response and isinstance(response, Response):
                content = response.content
                if response.reply:
                    content = '%s, %s' % (message.author.mention, content)

                sentmsg = await self.send_message(message.channel, content)

                if response.delete_after > 0:
                    await asyncio.sleep(response.delete_after)
                    await self.delete_message(sentmsg)
                    # TODO: Add options for deletion toggling

        except CommandError as e:
            await self.send_message(message.channel, '```\n%s\n```' % e.message)

        except:
            await self.send_message(message.channel, '```\n%s\n```' % traceback.format_exc())
            traceback.print_exc()


if __name__ == '__main__':
    bot = Bot()
    bot.run()
