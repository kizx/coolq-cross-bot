import requests
import base64
from nonebot import on_command, CommandSession
import os


@on_command('timeji', aliases=('时光鸡', '时光机', '时光姬', '动态', '说说'))
async def timeji(session: CommandSession):
    msg = session.get('msg', prompt='请继续输入')
    print('输出', msg)
    if not msg:
        await session.send('消息为空,图片可能获取失败')
        path = r'C:\Users\ZXIN\Desktop\something\酷Q Air_开发\data\image'
        if os.path.exists(path):
            for i in os.listdir(path):
                os.remove(os.path.join(path, i))
            await session.send('已清除所有图片缓存，请重新发送')
        return
    qq_response = await msg_port(msg)
    await session.send(qq_response)


@timeji.args_parser
async def _(session: CommandSession):
    stripped_arg = session.current_arg.strip()
    text = session.current_arg_text.strip()
    img_url = session.current_arg_images
    img_list = [img_port(url) for url in img_url]
    img_list.insert(0, text)
    msg = '\n'.join(img_list)
    if session.is_first_run:
        if stripped_arg:
            session.state['msg'] = msg
        return
    if not stripped_arg:
        session.pause('输入不能为空呢，请重新输入')
    session.state[session.current_key] = msg


async def msg_port(msg):
    """上传消息，包括文字、图片、混合消息"""

    url = 'https://www.2bboy.com/'
    data = {'token': 'qq',
            'time_code': 'abbea043c506a9a19b7c1844f373153f',
            'msg_type': 'text',
            'mediaId': '1',
            'content': msg,
            'cid': '32',
            'action': 'send_talk'}
    response = requests.post(url, data)
    if response.status_code == 200 and response.text == '1':
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
