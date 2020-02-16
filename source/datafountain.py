from datetime import datetime, timedelta

import requests

from .utils import STANDARD_TIME_FORMAT

PLATFORM_NAME = 'DataFountain'


def get_data():
    url = 'https://www.datafountain.cn/api/competitions?search=&state=in_service&type=1&page=1&per_page=30&sort=latest&raceid=all'

    response = requests.get(url=url)
    content = response.json()
    competitions = content['cmpt']['competitions']

    data = {'name': PLATFORM_NAME}
    cps = []
    for competition in competitions:
        if competition['stateOrder'] == 0 or competition['stateOrder'] == 1:
            continue
        # 必须字段
        name = competition['title']
        url = 'https://www.datafountain.cn/competitions/' + str(
            competition['id'])

        deadline = competition['endTime']
        FORMAT = "%Y-%m-%dT%H:%M:%S.%fZ"
        deadline = datetime.strptime(deadline, FORMAT) + timedelta(hours=8)
        deadline = deadline.strftime(STANDARD_TIME_FORMAT)

        reward = '￥' + competition['reward']

        cp = {
            'name': name,
            'url': url,
            'description': name,
            'deadline': deadline,
            'reward': reward
        }

        cps.append(cp)
    data['competitions'] = cps

    return data
