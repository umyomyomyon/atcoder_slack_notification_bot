import json
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup

from conf import BASE_URL


def create_bs(url: str, parser: str):
    target = requests.get(url)
    soup = BeautifulSoup(target.text, parser)
    return soup


def clean_up_content_list(contents):
    return list(filter(lambda c: c != '\n', contents))


def content_handle(contents):
    cleaned_contents = clean_up_content_list(contents)
    data_list = []
    for content in cleaned_contents:
        time = content.find('time').text.split('+')[0]
        name_content = content.find_all('td')[1].find('a')
        name = name_content.text
        href = name_content['href']
        url = urljoin(BASE_URL, href)
        data = {
            'name': name,
            'url': url,
            'time': time
        }
        data_list.append(data)
    return data_list


def make_updated_contest_data_list(contest_data_list):
    return contest_data_list


def make_notification_text(updated_contest_data_list):
    base_text = f'開催予定のコンテストに更新があります。'
    contest_texts = []
    for contest_data in updated_contest_data_list:
        text = perform_make_text(contest_data)
        contest_texts.append(text)
    notification_text = '\n----------\n'.join([base_text] + contest_texts)
    return notification_text


def perform_make_text(contest_data):
    return f'コンテスト名: {contest_data["name"]}\n開催時間: {contest_data["time"]}\nURL: {contest_data["url"]}\n'


def slack_api_post(slack_api_url, notification_text):
    content = json.dumps({
        'text': notification_text,
        'username': "atcoder知らせる君(未完成)",  # 投稿のユーザー名
        'icon_emoji': u':oden:',  # 投稿のプロフィール画像に入れる絵文字
        'link_names': 1,  # メンションを有効にする
    })
    res = requests.post(slack_api_url, data=content)
