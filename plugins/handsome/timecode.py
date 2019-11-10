import requests


def textport(msg):
    url = 'https://www.2bboy.com/'
    data = {
        'token': 'crx',
        'time_code': 'abbea043c506a9a19b7c1844f373153f',
        'msg_type': 'text',
        'mediaId': '1',
        'content': msg,
        'cid': '32',
        'action': 'send_talk'
    }
    response = requests.post(url, data,)
    print(response)
    print(response.text)
    print(response.content)

    return 'biubiubiu~发送成功'


if __name__ == '__main__':
    result = textport('发自pycharm')
    print(result)
