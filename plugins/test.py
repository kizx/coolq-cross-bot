from nonebot import on_command, CommandSession
from nonebot import on_natural_language, NLPSession, IntentCommand

__plugin_name__ = '测试'
__plugin_usage__ = '测试 命令'


@on_command('test', aliases=('测试',), only_to_me=False)
async def test(session: CommandSession):
    ctx = session.ctx
    await session.send(str(ctx))


@on_natural_language(only_to_me=False)
async def repeat(session: NLPSession):
    msg = session.ctx["message"]
    await session.send(msg)
