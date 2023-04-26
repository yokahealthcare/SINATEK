# -*- coding: utf-8 -*-
"""
Created on Tue Nov 15 12:04:27 2022

WiZ CONNECTED - CENTRAL CONTROL
@author: Erwin
"""

import asyncio
from functools import wraps
from typing import Any, Callable, Coroutine, TypeVar

from rich.console import Console

console = Console()

from pywizlight import PilotBuilder, discovery, wizlight

async def discover(b: str) -> None:
    """Discovery bulb in the local network."""
    console.print("Search for bulbs in {} ... ".format(b))

    bulbs = await discovery.find_wizlights(broadcast_address=b)
    index = 1
    for bulb in bulbs:
        console.print("[{}] IP ADDRESS : {}".format(index, bulb['ip_address']))
        index += 1

