from nonebot import on_command, CommandSession
import hashlib
import sqlite3


@on_command('init', aliases=('初始化',))
async def init(session: CommandSession):
    try:
        con = sqlite3.connect('bind_info.sqlite')
        cur = con.cursor()
        cur.execute(
            'create table user(id INTEGER PRIMARY KEY AUTOINCREMENT,qq int UNIQUE,blog text,cid text,time_code text)')
        cur.close()
        con.commit()
        con.close()
    except sqlite3.OperationalError:
        await session.send('已经初始化过了哦~')
    else:
        await session.send('初始化成功')


@on_command('bind', aliases=('绑定', '绑定博客', '绑定网站'))
async def bind(session: CommandSession):
    bind_info = session.get('bind_info', prompt='请输入：博客地址+时光机cid+时光机验证编码')
    try:
        info = bind_info.split('+')
        info[2] = hashlib.md5(info[2].encode("utf-8")).hexdigest()
        qq = session.ctx.get('user_id')
        con = sqlite3.connect('bind_info.sqlite')
        cur = con.cursor()
        cur.execute('insert into user(qq, blog, cid, time_code) values(?,?,?,?)', (qq, info[0], info[1], info[2]))
        cur.close()
        con.commit()
        con.close()
    except IndexError:
        await session.send('[ERR31]你填写的信息格式似乎有问题呢~请重新绑定')
    except sqlite3.OperationalError:
        await session.send('你初始化了吗？')
    except sqlite3.IntegrityError:
        await session.send('重复绑定警告！')
    except Exception as e:
        await session.send('[ERR32]发生未知错误：' + str(e))
    else:
        await session.send('绑定成功')


@on_command('unbind', aliases=('解绑', '解除绑定'))
async def unbind(session: CommandSession):
    qq = session.ctx.get('user_id')
    try:
        con = sqlite3.connect('bind_info.sqlite')
        cur = con.cursor()
        cur.execute('delete from user where qq = ?', (qq,))
        cur.close()
        con.commit()
        con.close()
    except Exception as e:
        await session.send('解绑失败了')
    else:
        await session.send('解绑成功！')