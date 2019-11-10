from nonebot import on_command, CommandSession
from nonebot import on_natural_language, NLPSession, IntentCommand

__plugin_name__ = '测试'
__plugin_usage__ = '测试 命令'


@on_command('test', aliases=('测试',), only_to_me=False)
async def test(session: CommandSession):
    text = session.get('text', prompt='请继续输入')
    print(text)
    print(session.current_arg)
    print(session.current_arg_images)
    await session.send(str(text))


@test.args_parser
async def _(session: CommandSession):
    stripped_arg = session.current_arg.strip()
    if session.is_first_run:
        if stripped_arg:
            session.state['text'] = stripped_arg
        return
    if not stripped_arg:
        session.pause('测试的内容不能为空呢，请重新输入')
    session.state[session.current_key] = stripped_arg

# @on_natural_language(only_to_me=False)
# async def repeat(session: NLPSession):
#     msg = session.ctx["message"]
#     await session.send(msg)
