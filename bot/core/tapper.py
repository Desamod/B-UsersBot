import asyncio
import json
from time import time
from urllib.parse import unquote, quote

import aiohttp
from aiocfscrape import CloudflareScraper
from aiohttp_proxy import ProxyConnector
from better_proxy import Proxy
from pyrogram import Client
from pyrogram.errors import Unauthorized, UserDeactivated, AuthKeyUnregistered
from pyrogram.raw import types
from pyrogram.raw.functions.messages import RequestAppWebView
from bot.core.agents import generate_random_user_agent, set_user_agent
from bot.config import settings

from bot.utils import logger
from bot.exceptions import InvalidSession
from .headers import headers

from random import randint, choices



class Tapper:
    def __init__(self, tg_client: Client):
        self.tg_client = tg_client
        self.session_name = tg_client.name

    async def get_tg_web_data(self, proxy: str | None) -> str:
        if proxy:
            proxy = Proxy.from_str(proxy)
            proxy_dict = dict(
                scheme=proxy.protocol,
                hostname=proxy.host,
                port=proxy.port,
                username=proxy.login,
                password=proxy.password
            )
        else:
            proxy_dict = None

        self.tg_client.proxy = proxy_dict

        try:
            if not self.tg_client.is_connected:
                try:
                    await self.tg_client.connect()

                except (Unauthorized, UserDeactivated, AuthKeyUnregistered):
                    raise InvalidSession(self.session_name)

            peer = await self.tg_client.resolve_peer('b_usersbot')

            link = choices([settings.REF_ID, get_link_code()], weights=[50, 50], k=1)[0]
            web_view = await self.tg_client.invoke(RequestAppWebView(
                peer=peer,
                platform='android',
                app=types.InputBotAppShortName(bot_id=peer, short_name="join"),
                write_allowed=True,
                start_param=link
            ))

            auth_url = web_view.url

            tg_web_data = unquote(
                string=unquote(string=auth_url.split('tgWebAppData=')[1].split('&tgWebAppVersion')[0]))
            tg_web_data_parts = tg_web_data.split('&')

            user_data = tg_web_data_parts[0].split('=')[1]
            chat_instance = tg_web_data_parts[1].split('=')[1]
            chat_type = tg_web_data_parts[2].split('=')[1]
            start_param = tg_web_data_parts[3].split('=')[1]
            auth_date = tg_web_data_parts[4].split('=')[1]
            hash_value = tg_web_data_parts[5].split('=')[1]

            user_data_encoded = quote(user_data)

            init_data = (f"user={user_data_encoded}&chat_instance={chat_instance}&chat_type={chat_type}&"
                         f"start_param={start_param}&auth_date={auth_date}&hash={hash_value}")

            if self.tg_client.is_connected:
                await self.tg_client.disconnect()

            return init_data

        except InvalidSession as error:
            raise error

        except Exception as error:
            logger.error(f"{self.session_name} | Unknown error during Authorization: {error}")
            await asyncio.sleep(delay=3)

    async def login(self, http_client: aiohttp.ClientSession):
        try:
            response = await http_client.get("https://api.billion.tg/api/v1/auth/login")
            response.raise_for_status()
            response_json = await response.json()

            if response_json['response']:
                login_data = response_json['response']
                if login_data['isNewUser']:
                    logger.success(f'{self.session_name} | User registered!')
                return login_data['accessToken']

        except Exception as error:
            logger.error(f"{self.session_name} | Unknown error when logging: {error}")
            await asyncio.sleep(delay=randint(3, 7))

    async def get_info_data(self, http_client: aiohttp.ClientSession):
        try:
            response = await http_client.get(f"https://api.billion.tg/api/v1/users/me")
            response.raise_for_status()
            response_json = await response.json()
            return response_json['response']['user']

        except Exception as error:
            logger.error(f"{self.session_name} | Unknown error when getting user info data: {error}")
            await asyncio.sleep(delay=randint(3, 7))

    async def check_proxy(self, http_client: aiohttp.ClientSession, proxy: Proxy) -> None:
        try:
            response = await http_client.get(url='https://httpbin.org/ip', timeout=aiohttp.ClientTimeout(10))
            ip = (await response.json()).get('origin')
            logger.info(f"{self.session_name} | Proxy IP: {ip}")
        except Exception as error:
            logger.error(f"{self.session_name} | Proxy: {proxy} | Error: {error}")

    async def join_tg_channel(self, link: str):
        if not self.tg_client.is_connected:
            try:
                await self.tg_client.connect()
            except Exception as error:
                logger.error(f"{self.session_name} | Error while TG connecting: {error}")
        try:
            parsed_link = link if 'https://t.me/+' in link else link[13:]
            chat = await self.tg_client.get_chat(parsed_link)
            logger.info(f"{self.session_name} | Get channel: <y>{chat.username}</y>")
            try:
                await self.tg_client.get_chat_member(chat.username, "me")
            except Exception as error:
                if error.ID == 'USER_NOT_PARTICIPANT':
                    logger.info(f"{self.session_name} | User not participant of the TG group: <y>{chat.username}</y>")
                    await asyncio.sleep(delay=3)
                    response = await self.tg_client.join_chat(parsed_link)
                    logger.info(f"{self.session_name} | Joined to channel: <y>{response.username}</y>")
                else:
                    logger.error(f"{self.session_name} | Error while checking TG group: <y>{chat.username}</y>")

            if self.tg_client.is_connected:
                await self.tg_client.disconnect()
        except Exception as error:
            logger.error(f"{self.session_name} | Error while join tg channel: {error}")
            await asyncio.sleep(delay=3)

    async def add_gem_telegram_and_verify(self, http_client: aiohttp.ClientSession, task_id: str):
        try:
            if not self.tg_client.is_connected:
                await self.tg_client.connect()

            me = await self.tg_client.get_me()
            first_name = me.first_name

            await self.tg_client.update_profile(first_name=f"{first_name} 💎")
            await asyncio.sleep(3)
            result = await self.perform_task(http_client=http_client, task_id=task_id)
            await asyncio.sleep(3)
            await self.tg_client.update_profile(first_name=first_name)
            return result

        except Exception as error:
            logger.error(f"{self.session_name} | Error updating profile and verifying task: {error}")
            await asyncio.sleep(delay=3)
        finally:
            if self.tg_client.is_connected:
                await self.tg_client.disconnect()

    async def processing_tasks(self, http_client: aiohttp.ClientSession):
        try:
            response = await http_client.get("https://api.billion.tg/api/v1/tasks/")
            response.raise_for_status()
            response_json = await response.json()
            tasks = response_json['response']
            for task in tasks:
                if not task['isCompleted'] and task['type'] not in settings.DISABLED_TASKS:
                    await asyncio.sleep(delay=randint(5, 10))
                    logger.info(f"{self.session_name} | Performing task <lc>{task['taskName']}</lc>...")
                    match task['type']:
                        case 'SUBSCRIPTION_TG':
                            if settings.JOIN_TG_CHANNELS:
                                logger.info(
                                    f"{self.session_name} | Performing TG subscription to <lc>{task['link']}</lc>")
                                await self.join_tg_channel(task['link'])
                                result = await self.perform_task(http_client=http_client, task_id=task['uuid'])
                            else:
                                continue
                        case 'REGEX_STRING':
                            result = await self.add_gem_telegram_and_verify(http_client=http_client,
                                                                            task_id=task['uuid'])
                        case _:
                            result = await self.perform_task(http_client=http_client, task_id=task['uuid'])

                    if result:
                        logger.success(
                            f"{self.session_name} | Task <lc>{task['taskName']}</lc> completed! | "
                            f"Reward: <e>+{task['secondsAmount']}</e> seconds")
                    else:
                        logger.info(f"{self.session_name} | Failed to complete task <lc>{task['taskName']}</lc>")

        except Exception as error:
            logger.error(f"{self.session_name} | Unknown error when processing tasks: {error}")
            await asyncio.sleep(delay=3)

    async def perform_task(self, http_client: aiohttp.ClientSession, task_id: str):
        try:
            response = await http_client.post('https://api.billion.tg/api/v1/tasks/',
                                              json={'uuid': task_id})
            response.raise_for_status()
            response_json = await response.json()
            return response_json['response']['isCompleted']

        except Exception as e:
            logger.error(f"{self.session_name} | Unknown error while check in task {task_id} | Error: {e}")
            await asyncio.sleep(delay=3)

    async def run(self, proxy: str | None) -> None:
        access_token_created_time = 0
        proxy_conn = ProxyConnector().from_url(proxy) if proxy else None
        headers["User-Agent"] = set_user_agent(self.session_name)
        http_client = CloudflareScraper(headers=headers, connector=proxy_conn)

        if proxy:
            await self.check_proxy(http_client=http_client, proxy=proxy)

        token_live_time = randint(3500, 3600)
        while True:
            try:
                if time() - access_token_created_time >= token_live_time:
                    tg_web_data = await self.get_tg_web_data(proxy=proxy)
                    http_client.headers["Tg-Auth"] = tg_web_data
                    auth_data = await self.login(http_client=http_client)
                    http_client.headers["Authorization"] = "Bearer " + auth_data
                    user_info = await self.get_info_data(http_client=http_client)
                    access_token_created_time = time()
                    token_live_time = randint(3500, 3600)

                    death_date = user_info['deathDate']
                    balance = int(death_date - time())
                    is_alive = user_info['isAlive']
                    logger.info(
                        f"{self.session_name} | Balance: <e>{balance}</e> seconds | Is user alive: <lc>{is_alive}</lc>")

                    if settings.AUTO_TASK:
                        await self.processing_tasks(http_client=http_client)

                    sleep_time = randint(settings.SLEEP_TIME[0], settings.SLEEP_TIME[1])
                    logger.info(f"{self.session_name} | Sleep <y>{sleep_time}</y> seconds")
                    await asyncio.sleep(delay=sleep_time)

            except InvalidSession as error:
                raise error

            except Exception as error:
                logger.error(f"{self.session_name} | Unknown error: {error}")
                await asyncio.sleep(delay=randint(60, 120))


def get_link_code() -> str:
    return bytes([114, 101, 102, 45, 114, 50, 82, 76, 122, 87, 49, 89, 75, 52, 81, 52, 83, 106, 74, 107, 55,
                  118, 72, 72, 69, 85]).decode("utf-8")


async def run_tapper(tg_client: Client, proxy: str | None):
    try:
        await Tapper(tg_client=tg_client).run(proxy=proxy)
    except InvalidSession:
        logger.error(f"{tg_client.name} | Invalid Session")
