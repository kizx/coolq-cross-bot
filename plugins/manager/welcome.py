from nonebot import on_notice, NoticeSession


@on_notice('group_increase')
async def _(session: NoticeSession):
    user_id = session.ctx.get('user_id')
    msg = '欢迎新朋友～'
    msg = f'[CQ:at, qq = {user_id}]' + '\n' + msg
    await session.send(msg)


@on_notice('group_decrease')
async def _(session: NoticeSession):
    msg = '/(ㄒoㄒ)/~~又一位群友离我们而去'
    await session.send(msg)
