from nonebot import on_request, RequestSession


@on_request('friend')
async def _(session):
    # 如果在我的群里就同意加好友
    group_id = 642739195
    qq = session.ctx['user_id']
    bot = session.bot
    member_info = await bot.get_group_member_list(group_id=group_id)
    qq_list = [i.get('user_id') for i in member_info]
    if qq in qq_list:
        await session.approve()
    else:
        await session.reject()
