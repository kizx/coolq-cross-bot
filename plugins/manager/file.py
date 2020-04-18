from nonebot import on_command, CommandSession
import os


@on_command('imgdata', aliases=('清空缓存', '删除缓存', '清空图片缓存', '清空图片'))
async def _(session):
    path = r'..\..\data\image'
    if os.path.exists(path):
        for i in os.listdir(path):
            os.remove(os.path.join(path, i))
        await session.send('已清除所有图片缓存')
