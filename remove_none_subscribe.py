from init import credential, GetUser
from bilibili_api import user, ResponseCodeException
import asyncio

global my_user

white_list = [11783021]  # "哔哩哔哩番剧出差"


async def main() -> None:
    global my_user
    my_user = await GetUser()

    await start_remove()


async def start_remove() -> None:
    if not my_user:
        raise

    following_counts = 0
    page = 1
    relation_info = await my_user.get_relation_info()
    total_followings = relation_info["following"]

    # 因为请求一次 get_followers 只能获取 50 个关注，所以要做一个检查
    while following_counts < total_followings:
        # 获取当前页数的关注列表
        followers = None
        while True:
            try:
                print(f"获取第{page}页关注")
                followers = await my_user.get_followings(pn=page)
                # 防止触发 412 错误
                await asyncio.sleep(1)
                break
            except ResponseCodeException as e:
                print(f"  [API异常 code={e.code}] -> {e.msg}")
                if e.code == -352 or e.code == -412 or e.code == 412:
                    await asyncio.sleep(120)
                    continue
                else:
                    raise

        # 循环当前页数的关注列表
        if not followers or len(followers["list"]) == 0:
            return
        for i in followers["list"]:
            following_counts += 1

            uid = int(i["mid"])
            name = i["uname"]
            u = user.User(uid=uid, credential=credential)
            is_banned = False
            is_cancelled = False

            if uid in white_list:
                continue

            while True:
                try:
                    u_info = await u.get_user_info()
                    name = u_info.get("name", name)
                    sign = u_info.get("sign", "")
                    if "账号已注销" in name or "账号已注销" in sign:
                        is_cancelled = True
                    if u_info.get("silence") == 1:
                        is_banned = True
                    # 防止触发 412 错误
                    await asyncio.sleep(1)
                    break
                except ResponseCodeException as e:
                    if e.code == -404:
                        is_cancelled = True
                    print(f"  [API异常 code={e.code}] {name}, uid:{uid} -> {e.msg}")
                    if e.code == -352 or e.code == -412 or e.code == 412:
                        await asyncio.sleep(120)
                        continue
                    else:
                        break

            # if not is_banned and not is_cancelled:
            if not is_cancelled:
                continue

            status = "已注销" if is_cancelled else "封禁"
            print(f"Removing [{status}] {name}, uid:{uid}. Count: {following_counts}")
            while True:
                try:

                    result = await u.modify_relation(relation=user.RelationType.UNSUBSCRIBE)
                    # 防止触发 412 错误
                    await asyncio.sleep(1)
                    break
                except ResponseCodeException as e:
                    print(f"  [API异常 code={e.code}] {name}, uid:{uid} -> {e.msg}")
                    if e.code == -352 or e.code == -412 or e.code == 412:
                        await asyncio.sleep(120)
                        continue
                    else:
                        raise
            # 防止触发 412 错误
            await asyncio.sleep(1)

        # 下一页
        page += 1


if __name__ == "__main__":
    asyncio.run(main())
