from init import credential, GetUser
from bilibili_api import user, ResponseCodeException
import asyncio

global my_user


async def main() -> None:
    global my_user
    my_user = await GetUser()

    await start_remove()


async def start_remove() -> None:
    if not my_user:
        raise

    follower_counts = 0
    page = 1
    total_followers = (await my_user.get_relation_info())["follower"]

    # 因为请求一次 get_followers 只能获取 20 个粉丝，所以要做一个检查
    while follower_counts < total_followers:
        # 获取当前页数的粉丝列表
        followers = None
        while True:
            try:
                print(f"获取第{page}页粉丝")
                followers = await my_user.get_followers(pn=page)
                # 防止触发 412 错误
                await asyncio.sleep(1)
                break
            except ResponseCodeException as e:
                print(f"  [API异常 code={e.code}] -> {e.msg}")
                if e.code == -352 or e.code == -412 or e.code == 412:
                    await asyncio.sleep(10)
                    continue
                else:
                    raise

        # 循环当前页数的粉丝列表
        for i in followers["list"]:
            follower_counts += 1

            uid = int(i["mid"])
            name = i["uname"]
            u = user.User(uid=uid, credential=credential)
            is_banned = False
            is_cancelled = False
            while True:
                try:
                    u_info = await u.get_user_info()
                    name = u_info.get("name", name)
                    sign = u_info.get("sign", "")
                    if "账号已注销" in name or "账号已注销" in sign:
                        is_cancelled = True
                    if u_info.get("silence") == 1:
                        is_banned = True

                    break
                except ResponseCodeException as e:
                    if e.code == -404:
                        is_cancelled = True
                    print(f"  [API异常 code={e.code}] {name}, uid:{uid} -> {e.msg}")
                    if e.code == -352 or e.code == -412 or e.code == 412:
                        await asyncio.sleep(10)
                        continue
                    else:
                        break

            if not is_banned and not is_cancelled:
                continue

            status = "已注销" if is_cancelled else "封禁"
            print(f"Removing [{status}] {name}, uid:{uid}. Count: {follower_counts}")
            while True:
                try:

                    await u.modify_relation(relation=user.RelationType.REMOVE_FANS)
                    # 防止触发 412 错误
                    await asyncio.sleep(1)
                    break
                except ResponseCodeException as e:
                    print(f"  [API异常 code={e.code}] {name}, uid:{uid} -> {e.msg}")
                    if e.code == -352 or e.code == -412 or e.code == 412:
                        await asyncio.sleep(10)
                        continue
                    else:
                        raise
            # 防止触发 412 错误
            await asyncio.sleep(1)

        # 下一页
        page += 1


if __name__ == "__main__":
    asyncio.run(main())
