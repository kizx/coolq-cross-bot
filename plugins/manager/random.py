from nonebot import on_command, CommandSession
from random import randint, randrange


async def get_rand_num(paras):
    try:
        paras = paras.split()
        paras = [int(i) for i in paras]
        rmin = paras[0]
        rmax = paras[1]
        a = randint(rmin, rmax)
    except Exception as e:
        return e, 0
    else:
        return a, 1


@on_command('random_num', only_to_me=False, aliases=('随机数',))
async def random_num(session):
    paras = session.get('paras', prompt='请输入随机数范围\n如：1 10')
    num, ok = await get_rand_num(paras)
    if ok:
        msg = f'幸运数字为：{num}'
    else:
        msg = f'错误：{num}'
    msg = f"[CQ:at, qq = {session.event.get('user_id')}]" + msg
    await session.send(msg)


@random_num.args_parser
async def _(session):
    stripped_arg = session.current_arg_text.strip()
    if session.is_first_run:
        if stripped_arg:
            session.state['paras'] = stripped_arg
        return
    if not stripped_arg:
        session.pause('不能为空呢，请重新输入')
    session.state[session.current_key] = stripped_arg
