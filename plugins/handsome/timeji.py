from nonebot import on_command, CommandSession
import requests
import base64
import sqlite3
import aiohttp


@on_command('timeji', aliases=('时光鸡', '时光机', '时光姬', '动态', '说说'))
async def timeji(session: CommandSession):
    msg = session.get('msg', prompt='请输入内容')
    await send_msg(session, msg)


@timeji.args_parser
async def _(session: CommandSession):
    stripped_arg = session.current_arg.strip()
    text, img_list = await msg_handle(session)
    msg = []
    if text:
        msg.append(text)
    if img_list:
        imgs = ''.join(img_list)
        if len(img_list) != 1:
            imgs = f'[album]{imgs}[/album]'
        msg.append(imgs)
    msg = '\n'.join(msg)
    if session.is_first_run:
        if stripped_arg:
            session.state['msg'] = msg
        return
    if not stripped_arg:
        session.pause('输入不能为空呢，请重新输入')
    session.state[session.current_key] = msg


@on_command('multi', aliases=('开始',))
async def multi(session: CommandSession):
    session.state['texts'] = []
    session.state['imgs'] = []
    msg = session.get('msg', prompt='进入混合输入模式，请输入内容')
    await send_msg(session, msg)


@multi.args_parser
async def _(session: CommandSession):
    stripped_arg = session.current_arg.strip()
    if session.is_first_run:
        return
    if not stripped_arg:
        session.pause('输入不能为空呢，请重新输入')
    text = session.current_arg_text
    if text != '结束' and text != '取消':
        text, img_list = await msg_handle(session)
        if text:
            session.state['texts'].append(text)
        if img_list:
            session.state['imgs'] += img_list
        session.pause('请继续输入，或发送「取消」or「结束」')
    elif text == '结束':
        img_list = session.state['imgs']
        imgs = []
        if img_list:
            imgs = ''.join(img_list)
            if len(img_list) != 1:
                imgs = f'[album]{imgs}[/album]'
            imgs = [imgs]
        msg = session.state['texts'] + imgs
        msg = '\n'.join(msg)
        session.state[session.current_key] = msg
        return
    elif text == '取消':
        session.state[session.current_key] = ''
        return


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
    """上传图片到博客服务器并获得图片链接，由于不是异步的仅留作测试"""
    print('[图片下载]...')
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
    print('[图片上传]...')
    response = requests.post(url, data)
    if response.status_code == 200 and response.json().get('status') == '1':
        img_url = response.json().get('data').replace('\\', '')
        return f'<img src="{img_url}"/>'
    else:
        return '图片上传失败'


async def asyimg_port(img_link, blog, time_code):
    """异步下载QQ发来的图片并上传到博客空间"""
    print('[图片下载]...')
    async with aiohttp.ClientSession() as sess:
        async with sess.get(img_link) as response:
            img_type = response.headers.get('Content-Type').split('/')[1]
            base64_data = base64.b64encode(await response.read()).decode()
            img_base64 = f'data:{img_type};base64,{base64_data}'

        url = blog
        data = {'action': 'upload_img',
                'time_code': time_code,
                'token': 'qq',
                'file': img_base64,
                'mediaId': '1'}
        print('[图片上传]...')
        async with sess.post(url, data=data) as response:
            if response.status == 200:
                text = await response.text()
                text = eval(text)
                if text.get('status') == '1':
                    img_url = text.get('data').replace('\\', '')
                    return f'<img src="{img_url}"/>'
                else:
                    return '图片上传失败'


async def send_msg(session, msg):
    """消息发送前处理"""
    print('[输出]', msg)
    if not msg:
        await session.send('已取消上传')
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


async def msg_handle(session):
    """提取消息中的文字和图片"""
    text = session.current_arg_text
    img_url = session.current_arg_images
    img_list = []
    if img_url:
        try:
            con = sqlite3.connect('bind_info.sqlite')
            cur = con.cursor()
            cur.execute('select blog,time_code,setting from user where qq = ?', (session.ctx.get('user_id'),))
            (blog, time_code, setting) = cur.fetchone()
            cur.close()
            con.commit()
            con.close()
            if setting == 0:
                img_list = [f'<img src="{url}"/>' for url in img_url]
            elif setting == 1:
                img_list = [await asyimg_port(url, blog, time_code) for url in img_url]
            elif setting == 9:
                img_list = [await img_port(url, blog, time_code) for url in img_url]
        except sqlite3.OperationalError:
            await session.send('[ERR11]你似乎还没有绑定呢~')
        except (TypeError, AttributeError):
            await session.send('[ERR12]你的绑定信息似乎有问题呢~')
    return [text, img_list]


if __name__ == '__main__':
    pass
