
from discord import Client
from typing import List, Dict
import abc
from discord import Message


class Component(metaclass=abc.ABCMeta):
    def __init__(self, prefix: str, label: str, client: Client, alias: List[str] = [], command: str = ""):
        self.prefix = prefix.lower()
        self.label = label
        self.client = client
        self.alias = [a.lower() for a in alias]
        self.command = command

    @abc.abstractmethod
    def on_message(self, message: Message, contents: List[str]):
        pass

    @abc.abstractmethod
    def get_help(self):
        return f"ヘルプメッセージが定義されていません。"

    @staticmethod
    def parse_config(ss: List[str], default: Dict[str, str] = {}) -> Dict[str, str]:
        res = default.copy()

        current = ""
        for s in ss:
            splitted = s.split(':')
            if len(splitted) < 2:
                res[current] = (res[current] + " " + splitted[0]).strip()
            else:
                current = splitted[0].lower()
                res[current] = splitted[1].strip()
    
        return res