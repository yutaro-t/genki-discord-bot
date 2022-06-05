from discord import Message
from typing import List
from . import Component
import shlex
class ComponentList:
    def __init__(self, prefix: str, components: List[Component]):
        self.components = components
        self.prefix = prefix

    async def on_message(self, message: Message, content: str):

        splitted = shlex.split(content.replace("　", " "))
        command = splitted[0].lower()

        if command == "help" or command == "h":
            await self.send_help(message)
            return

        for component in self.components:
            if component.prefix == command or command in component.alias:
                await component.on_message(message, splitted[1:])
                return

        raise Exception(f"コマンドが見つかりませんでした: {command}")

    async def send_help(self, message: Message):
        res = [
            f"おはようございます、{message.author.mention}!元気があっていいですね!",
            ""
        ]
        for component in self.components:
            help = component.get_help()
            res.extend([
                f"__**{component.label}**__",
                f"```{self.prefix}{component.prefix} {component.command}```",
                f"(エイリアス:{'、'.join(component.alias)})",
                help,
                "",
            ])
            print
            if help[-3:] != "```":
                res.append("")

        res.extend([
            f"__**ヘルプ**__",
            f"```{self.prefix}help```",
            f"(エイリアス:h)",
            "コマンドのヘルプを表示します"
        ])


        await message.channel.send("\n".join(res))