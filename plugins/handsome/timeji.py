import requests
import base64
from nonebot import on_command, CommandSession


@on_command('timeji', aliases=('时光鸡', '时光机', '时光姬', '动态', '说说'), only_to_me=False)
async def timeji(session: CommandSession):
    msg = session.get('msg', prompt='请继续输入')
    print('总输出', msg)
    qq_response = await msg_port(msg)
    await session.send(qq_response)


@timeji.args_parser
async def _(session: CommandSession):
    stripped_arg = session.current_arg.strip()
    text = session.current_arg_text.strip()
    img_url = session.current_arg_images
    img_list = [img_port(url) for url in img_url]
    img = '\n'.join(img_list)
    if session.is_first_run:
        if stripped_arg:
            session.state['msg'] = text + '\n' + img
        return
    if not stripped_arg:
        session.pause('输入不能为空呢，请重新输入')
    session.state[session.current_key] = text + '\n' + img


async def msg_port(msg):
    """发送消息，包括文字、图片、混合消息"""

    url = 'https://www.2bboy.com/'
    data = {'token': 'qq',
            'time_code': 'abbea043c506a9a19b7c1844f373153f',
            'msg_type': 'text',
            'mediaId': '1',
            'content': msg,
            'cid': '32',
            'action': 'send_talk'}
    response = requests.post(url, data)
    if response.status_code == 200:
        return 'biubiubiu~发送成功'
    else:
        return '发送失败惹~'


def img_port(img_link):
    """上传图片并获得图片链接"""

    response = requests.get(img_link)
    img_type = response.headers.get('Content-Type')
    base64_data = base64.b64encode(response.content).decode()
    img_base64 = f'data:{img_type};base64,{base64_data}'

    url = 'https://www.2bboy.com/'
    data = {'action': 'upload_img',
            'time_code': 'abbea043c506a9a19b7c1844f373153f',
            'token': 'qq',
            'file': img_base64,
            'mediaId': '1'}
    response = requests.post(url, data)
    img_url = response.json().get('data').replace('\\', '')
    return f"<img src='{img_url}' />"


if __name__ == '__main__':
    pass
