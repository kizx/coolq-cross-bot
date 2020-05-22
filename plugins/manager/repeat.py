from nonebot import on_natural_language, NLPSession, IntentCommand
from nonebot import on_command, CommandSession
import random

__plugin_name__ = '复读机'
__plugin_usage__ = '会概率参与复读或打断复读,目前不分群'


@on_command('repeat')
async def repeat(session: NLPSession):
    msg = session.state.get('message')
    # print('[当前消息]', msg)
    # print('[前一条消息]', session.bot.config.repeat['msg_bf'])
    if msg == session.bot.config.repeat['msg_bf']:
        session.bot.config.repeat['counter'] += 1
    else:
        session.bot.config.repeat['counter'] = 1
        session.bot.config.repeat['is_rp'] = False
    session.bot.config.repeat['msg_bf'] = msg
    if session.bot.config.repeat['counter'] >= 2:
        num = random.randint(1, 10)
        if num < session.bot.config.repeat['counter']:
            if random.random() < 0.2:
                msg = '打断复读[CQ:face,id=38]'
            if not session.bot.config.repeat['is_rp']:
                await session.send(msg)
                session.bot.config.repeat['counter'] = 1
                session.bot.config.repeat['is_rp'] = True
    # print('[计数]', session.bot.config.repeat['counter'])
    # print('[复读]', session.bot.config.repeat['is_rp'])


@on_natural_language(only_to_me=False)
async def _(session: NLPSession):
    return IntentCommand(60.0, 'repeat', args={'message': session.msg})
