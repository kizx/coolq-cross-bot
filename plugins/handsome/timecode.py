import requests
import base64


def msg_port(msg):
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


def img_port(img):
    """上传图片并获得图片链接"""
    with open(img, 'rb') as f:
        base64_data = base64.b64encode(f.read())
        img_base64 = f'data:image/jpeg;base64,{base64_data}'
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
    # result = textport("<img src='https://www.2bboy.com/usr/uploads/time/5dc7d458dfe08.png' />")
    result = img_port(r'C:\Users\ZXIN\Desktop\001.png')
    print(result)
