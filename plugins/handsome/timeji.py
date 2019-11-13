import requests
import base64
from nonebot import on_command, CommandSession
import os
import sqlite3


@on_command('timeji', aliases=('时光鸡', '时光机', '时光姬', '动态', '说说'))
async def timeji(session: CommandSession):
    msg = session.get('msg', prompt='请继续输入')
    print('总输出', str(msg))
    if not msg:
        await session.send('消息为空,图片可能上传失败')
        path = r'C:\Users\ZXIN\Desktop\something\酷Q Air_开发\data\image'
        if os.path.exists(path):
            for i in os.listdir(path):
                os.remove(os.path.join(path, i))
            await session.send('已清除所有图片缓存，请重新发送')
        return
    try:
        con = sqlite3.connect('bind_info.sqlite')
        cur = con.cursor()
        cur.execute('select blog,cid,time_code from user where qq = ?', (session.ctx.get('user_id'),))
        (blog,cid,time_code) = cur.fetchone()
        cur.close()
        con.commit()
        con.close()
    except TypeError:
        await session.send('[ERR01]你的绑定似乎有问题呢~')
    except sqlite3.OperationalError:
        await session.send('[ERR02]你似乎还没有绑定呢~')
    else:
        qq_response = await msg_port(msg, blog, cid, time_code)
        await session.send(qq_response)


@timeji.args_parser
async def _(session: CommandSession):
    stripped_arg = session.current_arg.strip()
    text = session.current_arg_text.strip()
    img_url = session.current_arg_images
    msg_list = []
    if text:
        msg_list.append(text)
    if img_url:
        try:
            con = sqlite3.connect('bind_info.sqlite')
            cur = con.cursor()
            cur.execute('select blog,time_code from user where qq = ?', (session.ctx.get('user_id'),))
            (blog,time_code) = cur.fetchone()
            cur.close()
            con.commit()
            con.close()
            img_list = [await img_port(url, blog,time_code) for url in img_url]
            msg_list = msg_list + img_list
        except sqlite3.OperationalError:
            await session.send('[ERR11]你似乎还没有绑定呢~')
            return
        except (TypeError, AttributeError):
            await session.send('[ERR12]你的绑定信息似乎有问题呢~')
            return
    msg = '\n'.join(msg_list)
    if session.is_first_run:
        if stripped_arg:
            session.state['msg'] = msg
        return
    if not stripped_arg:
        session.pause('输入不能为空呢，请重新输入')
    session.state[session.current_key] = msg


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


if __name__ == '__main__':
    conn = sqlite3.connect('../../bind_info.sqlite')
    curs = conn.cursor()
    # curs.execute('insert into user (qq, blog, cid, time_code) values(?,?,?,?)',
    #              (123456, 'info[0]', 'info[1]', 'info[2])'))
    curs.execute('select blog,cid,time_code from user where qq = ?', (3317200497,))
    # (blog,cid,time_code) = curs.fetchone()
    # print(blog,cid,time_code)
    curs.close()
    conn.commit()
    conn.close()