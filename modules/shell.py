#  Moon-Userbot - telegram userbot
#  Copyright (C) 2020-present Moon Userbot Organization
#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program.  If not, see <https://www.gnu.org/licenses/>.

import subprocess
import shlex
import os
from time import perf_counter

from pyrogram import Client, filters
from pyrogram.types import Message
from pyrogram import enums as enums

from utils.misc import modules_help, prefix

#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.

#  You should have received a copy of the GNU General Public License
#  along with this program.  If not, see <https://www.gnu.org/licenses/>.

from subprocess import Popen, PIPE, TimeoutExpired
import os
from time import perf_counter

from pyrogram import Client, filters
from pyrogram.types import Message

from utils.misc import modules_help, prefix


@Client.on_message(filters.command(["shell", "sh"], prefix) & filters.me)
async def shell(_, message: Message):
    if len(message.command) < 2:
        return await message.edit("<b>Specify the command in message text</b>", parse_mode=enums.ParseMode.HTML)
    cmd_text = message.text.split(maxsplit=1)[1]
    cmd_args = shlex.split(cmd_text)
    cmd_obj = subprocess.Popen(
        cmd_args,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )
    try:
        stdout, stderr = cmd_obj.communicate(timeout=60)
    except subprocess.TimeoutExpired:
        cmd_obj.kill()
        text += "<b>Timeout expired (60 seconds)</b>"

    char = "#" if os.getuid() == 0 else "$"
    text = f"<b>{char}</b> <code>{cmd_text}</code>\n\n"

    await message.edit(text + "<b>Running...</b>", parse_mode=enums.ParseMode.HTML)
    try:
        start_time = perf_counter()
        stdout, stderr = cmd_obj.stdout, cmd_obj.stderr
    except subprocess.TimeoutExpired:
        text += "<b>Timeout expired (60 seconds)</b>"
    else:
        stop_time = perf_counter()
        if stdout:
            text += "<b>Output:</b>\n" f"<code>{stdout}</code>\n\n"
        if stderr:
            text += "<b>Error:</b>\n" f"<code>{stderr}</code>\n\n"
        text += f"<b>Completed in {round(stop_time - start_time, 5)} seconds with code {cmd_obj.returncode}</b>"
    await message.edit(text, parse_mode=enums.ParseMode.HTML)
    cmd_obj.kill()


modules_help["shell"] = {"sh [command]*": "Execute command in shell"}