import requests
import urllib3
from lxml import etree
from nonebot import on_command, CommandSession
import asyncio

'''
根据游戏id从https://steamdb.info/爬取数据
暂时不能直接输入游戏名，只能输入游戏id
需要先更改cookie
偶尔会抽风
'''
steamdb_cookie = '__cfduid=d97664c7d4b36da8b415925000caf28401573131878; ' \
                 '_ga=GA1.2.2033167086.1573131896; ' \
                 'cf_clearance=d4317cb87ce2a81b74ae638895d9686d50aa8a85-1573476694-0-250; ' \
                 '_gid=GA1.2.2025674706.1573476701; _gat=1'


@on_command('steam', aliases=('史低',), only_to_me=False)
async def price(session: CommandSession):
    user_id = session.ctx.get('user_id')
    game_id = session.get('game_id', prompt='请输入游戏id')
    msg = await get_price(game_id)
    msg = f'[CQ:at, qq = {user_id}]' + '\n' + msg
    await session.send(msg)


@price.args_parser
async def _(session: CommandSession):
    stripped_arg = session.current_arg_text.strip()
    if session.is_first_run:
        if stripped_arg:
            session.state['game_id'] = stripped_arg
        return
    if not stripped_arg:
        session.pause('要查询的游戏id不能为空呢，请重新输入')
    session.state[session.current_key] = stripped_arg


async def get_price(game_id):
    url = f'https://steamdb.info/app/{game_id}/'
    headers = {'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
               'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36',
               'Cookie': steamdb_cookie}
    urllib3.disable_warnings()
    response = requests.get(url, headers=headers, verify=False)

    try:
        root = etree.HTML(response.text)
        path = "//table[@class='table table-bordered table-hover table-dark table-responsive-flex']//td"
        name = root.xpath(path)[5].text

        path = "//table[@class='table table-fixed table-prices table-hover table-sortable']//td[text()='Base Price']"
        current_price = root.xpath(path + "/preceding-sibling::td/text()")[-1]
        cheap_price = root.xpath(path + "/following-sibling::td/text()")[0]
    except IndexError:
        return '输入的游戏id不对哟'
    except Exception:
        return '发生未知错误'
    else:
        return f"游戏名称：{name}\n当前价格：{current_price}\n史低价格：{cheap_price}"


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    result = loop.run_until_complete(get_price(203160))
    print(result)
    loop.close()
