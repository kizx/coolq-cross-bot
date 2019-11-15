import requests
import base64
from nonebot import on_command, CommandSession
import os
import sqlite3


@on_command('timeji', aliases=('时光鸡', '时光机', '时光姬', '动态', '说说'))
async def timeji(session: CommandSession):
    msg = session.get('msg', prompt='请输入内容')
    await send_msg(session, msg)


@timeji.args_parser
async def _(session: CommandSession):
    stripped_arg = session.current_arg.strip()
    msg_list = await msg_hanle(session)
    msg = '\n'.join(msg_list)
    if session.is_first_run:
        if stripped_arg:
            session.state['msg'] = msg
        return
    if not stripped_arg:
        session.pause('输入不能为空呢，请重新输入')
    session.state[session.current_key] = msg


@on_command('multi', aliases=('开始',))
async def multi(session: CommandSession):
    msg = session.get('msg', prompt='进入混合输入模式，请输入内容')
    msg = '\n'.join(msg)
    await send_msg(session, msg)


@multi.args_parser
async def _(session: CommandSession):
    if session.is_first_run:
        session.state['msg'] = []
    text = session.current_arg_text
    if text != '结束':
        msg = await msg_hanle(session)
        session.state['msg'] += msg
        print(session.state['msg'])
        session.pause('请继续输入')


async def msg_port(msg, blog, cid, time_code):
    """上传消息，包括文字、图片、混合消息"""
    url = blog
    data = {'token': 'qq',
            'time_code': time_code,
            'msg_type': 'text',
            'mediaId': '1',
            'content': msg,
            'cid': cid,
            'action': 'send_talk'}
    response = requests.post(url, data)
    if response.status_code == 200 and response.text == '1':
        return 'biubiubiu~发送成功'
    else:
        return '发送失败惹~'


async def img_port(img_link, blog, time_code):
    """上传图片并获得图片链接"""
    response = requests.get(img_link)
    img_type = response.headers.get('Content-Type')
    base64_data = base64.b64encode(response.content).decode()
    img_base64 = f'data:{img_type};base64,{base64_data}'

    url = blog
    data = {'action': 'upload_img',
            'time_code': time_code,
            'token': 'qq',
            'file': img_base64,
            'mediaId': '1'}
    response = requests.post(url, data)
    if response.status_code == 200 and response.json().get('status') == '1':
        img_url = response.json().get('data').replace('\\', '')
        return f"<img src='{img_url}' />"
    else:
        return '图片上传失败惹~'


async def send_msg(session, msg):
    if not msg:
        await session.send('消息为空,图片可能上传失败')
        print(os.getcwd())
        path = r'..\..\data\image'
        if os.path.exists(path):
            for i in os.listdir(path):
                os.remove(os.path.join(path, i))
            await session.send('已清除所有图片缓存，请重新发送')
        return
    try:
        con = sqlite3.connect('bind_info.sqlite')
        cur = con.cursor()
        cur.execute('select blog,cid,time_code from user where qq = ?', (session.ctx.get('user_id'),))
        (blog, cid, time_code) = cur.fetchone()
        cur.close()
        con.commit()
        con.close()
    except TypeError:
        await session.send('[ERR01]你的绑定似乎有问题呢~')
    except sqlite3.OperationalError:
        await session.send('[ERR02]你似乎还没有绑定呢~')
    else:
        # 判断是否是私密消息
        if msg[0] == '#':
            msg = msg.replace('#', '', 1)
            msg = f'[secret]{msg}[/secret]'
        qq_response = await msg_port(msg, blog, cid, time_code)
        await session.send(qq_response)


async def msg_hanle(session):
    text = session.current_arg_text
    img_url = session.current_arg_images
    msg_list = []
    if text:
        msg_list.append(text)
    if img_url:
        try:
            con = sqlite3.connect('bind_info.sqlite')
            cur = con.cursor()
            cur.execute('select blog,time_code from user where qq = ?', (session.ctx.get('user_id'),))
            (blog, time_code) = cur.fetchone()
            cur.close()
            con.commit()
            con.close()
            img_list = [await img_port(url, blog, time_code) for url in img_url]
            msg_list = msg_list + img_list
        except sqlite3.OperationalError:
            await session.send('[ERR11]你似乎还没有绑定呢~')
        except (TypeError, AttributeError):
            await session.send('[ERR12]你的绑定信息似乎有问题呢~')
    return msg_list


if __name__ == '__main__':
    pass