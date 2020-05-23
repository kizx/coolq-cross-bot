from nonebot import on_natural_language, NLPSession, IntentCommand
from nonebot import on_command, CommandSession
import random

__plugin_name__ = '复读机'
__plugin_usage__ = '会概率参与复读或打断复读,目前不分群'


@on_command('repeat')
async def repeat(session: NLPSession):
    msg = session.state.get('message')
    group_id = session.event.get('group_id')
    group_info = session.bot.config.repeat
    # print('原始信息', group_info)
    if group_id not in group_info:
        session.bot.config.repeat[group_id] = {'counter': 1, 'msg_bf': '', 'is_rp': False}

    repeat_info = session.bot.config.repeat.get(group_id)
    if msg == repeat_info['msg_bf']:
        repeat_info['counter'] += 1
    else:
        repeat_info['counter'] = 1
        repeat_info['is_rp'] = False
    repeat_info['msg_bf'] = msg
    if repeat_info['counter'] >= 2:
        num = random.randint(1, 10)
        if num < repeat_info['counter']:
            if random.random() < 0.2:
                msg = '打断复读[CQ:face,id=38]'
            if not repeat_info['is_rp']:
                await session.send(msg)
                repeat_info['counter'] = 1
                repeat_info['is_rp'] = True
    session.bot.config.repeat[group_id] = repeat_info  # python皆对象，不更新也行
    # print('结束消息', session.bot.config.repeat)


@on_natural_language(only_to_me=False)
async def _(session: NLPSession):
    return IntentCommand(60.0, 'repeat', args={'message': session.msg})
