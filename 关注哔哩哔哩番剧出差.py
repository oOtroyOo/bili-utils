# 哔哩哔哩番剧出差, uid:11783021

from init import credential, GetUser
from bilibili_api import user, ResponseCodeException
import asyncio


async def main() -> None:
    my_user = await GetUser()
    u = user.User(uid=11783021, credential=credential)
    await u.modify_relation(user.RelationType.SUBSCRIBE)


asyncio.run(main())
