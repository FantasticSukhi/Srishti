import asyncio
import os
import shlex
from typing import Tuple

from telegraph.aio import Telegraph
from utils import LOGGER


async def post_to_telegraph(is_media: bool, title, content, media=None):
    telegraph = Telegraph()
    LOGGER.info(await telegraph.create_account(short_name='MissKaty'))
    if is_media:
        """Create a Telegram Post Foto/Video"""
        response = await telegraph.upload_file(media)
        return f"https://telegra.ph{response[0]['src']}"
    """Create a Telegram Post using HTML Content"""
    response = await telegraph.create_page(
        title,
        html_content=content,
        author_url="https://t.me/MissKatyPyro",
        author_name="MissKatyBot"
    )
    return response['url']


async def run_subprocess(cmd):
    process = await asyncio.create_subprocess_exec(*cmd, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE)
    return await process.communicate()


async def get_media_info(file_link):
    ffprobe_cmd = [
        "ffprobe",
        "-headers",
        "IAM:''",
        "-i",
        file_link,
        "-v",
        "quiet",
        "-of",
        "json",
        "-show_streams",
        "-show_format",
        "-show_chapters",
        "-show_programs",
    ]
    data, err = await run_subprocess(ffprobe_cmd)
    return data


async def runcmd(cmd: str) -> Tuple[str, str, int, int]:
    """run command in terminal"""
    args = shlex.split(cmd)
    process = await asyncio.create_subprocess_exec(*args, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE)
    stdout, stderr = await process.communicate()
    return (
        stdout.decode("utf-8", "replace").strip(),
        stderr.decode("utf-8", "replace").strip(),
        process.returncode,
        process.pid,
    )


# Solves ValueError: No closing quotation by removing ' or " in file name
def safe_filename(path_):
    if path_ is None:
        return
    safename = path_.replace("'", "").replace('"', "")
    if safename != path_:
        os.rename(path_, safename)
    return safename
