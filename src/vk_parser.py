from vkbottle import API
from time import sleep
from datetime import datetime
import logging
from tqdm import tqdm
import csv
from typing import List, Dict
import asyncio

_logger = logging.getLogger(__name__)

GROUP_ID = 87598739


def is_relevant(s: str) -> bool:
    """
    It's pool post
    """
    phrases = ["себя чувствуете",
               "с указанием вашей геолокации",
               "отпишитесь по самочувствию",
               "с локацией",
               "отпишитесь по состоянию",
               "как самочувствие",
               "как состояние",
               "какая ситуация",
               "как здоровье",
               "локаци",
               "геолокаци",
               "как ваше самочувствие"
               ]

    for phrase in phrases:
        if s.lower().find(phrase) > -1:
            return True
    return False


def get_date(dttm: int) -> str:
    """
    Unox epoch to datetime
    """
    return datetime.fromtimestamp(dttm).strftime("%Y-%m-%d %H:%M:%S")


async def aget_comments(vk_token: str) -> List[Dict]:
    """
    :param vk_token: VK API token
    :return:
    """
    _logger.debug("Run VK API parser")
    api = API(vk_token)

    posts_list = []
    for i in range(10):
        _logger.debug("Iteration %d", i)
        posts = await api.wall.get(owner_id=-GROUP_ID, count=100, offset=i*100, order=2)
        if len(posts.items) == 0:
            break
        _logger.debug("Got %d posts", len(posts.items))
        for post in posts.items:
            t = {"text": post.text,
                 "date": get_date(post.date),
                 "id": post.id,
                 "comments_count": post.comments.count}
            posts_list.append(t)

    # filter topics
    posts_list = [el for el in posts_list if is_relevant(el["text"]) and el["comments_count"] > 0]
    _logger.debug("%d posts after filtration", len(posts_list))

    comments_list = []
    _logger.debug("Get comments")

    for post in tqdm(posts_list):
        comments = await api.wall.get_comments(owner_id=-GROUP_ID, post_id=post["id"], count=100, extended=1)
        for i, comment in enumerate(comments.items):
            # remove empty comments
            if comment.text == "":
                continue
            # remove replies
            if (comment.text.find("[id")+1):
                continue

            try:
                v = await api.users.get(user_ids=[comment.from_id], fields=["screen_name"])
                sleep(1)
                user_name = v[0].first_name + " " + v[0].last_name
            except Exception as err:
                _logger.warning("Can not get username for %d. Error %r", comment.from_id, err)
                user_name = None

            comments_list.append(
                {"datetime": get_date(comment.date),
                 "user_id": comment.from_id,
                 "user_name": user_name,
                 "id": comment.id,
                 "text": comment.text,
                 "post_id": comment.post_id})

    _logger.debug("Got %d comments", len(comments_list))

    return comments_list


def get_comments(vk_token):
    return asyncio.run(aget_comments(vk_token=vk_token))
