from discord import Message, Embed
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

        embed = Embed(
            title="長野誠校長のトリセツ"
        )
        for component in self.components:
            help = component.get_help()
            name = f"{component.label} (エイリアス:{'、'.join(component.alias)})" if len(component.alias) > 0 else component.label
            embed.add_field(name=name, value=f'''
                ```{self.prefix}{component.prefix} {component.command}```
                {help}
            ''', inline=False)

        embed.add_field(name="ヘルプ (エイリアス:h)", value=f"```{self.prefix}help```\nコマンドのヘルプを表示します")

        await message.channel.send(f"おはようございます、{message.author.mention}!元気があっていいですね!", embed=embed)