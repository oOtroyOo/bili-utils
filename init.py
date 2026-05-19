import bilibili_api
from typing import Optional
from dotenv import load_dotenv
import os

load_dotenv()


# 实例化 Credential 类
credential = bilibili_api.Credential(
    sessdata=os.environ.get("sessdata", ""),
    bili_jct=os.environ.get("bili_jct", ""),
    buvid3=os.environ.get("buvid3", ""),
    ac_time_value=os.environ.get("ac_time_value", ""),
)


async def GetUser() -> Optional[bilibili_api.user.User]:
    result = await bilibili_api.user.get_self_info(credential=credential)
    if isinstance(result, dict) and "name" in result:
        print(f"Hello {result.get('name')} ({result.get("mid", 0)}) Lv.{result.get('level',0)}")
        return bilibili_api.user.User(result.get("mid", 0), credential)
    raise
