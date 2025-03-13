# -*- coding: utf-8 -*-
"""
Created on Thu Nov 17 18:26:14 2022
@author: https://github.com/vik1109/
"""
import os
import pandas as pd
import re
from datetime import datetime
import logging

from  .toponim_parser_yargo import ToponimParserYargo

_logger = logging.getLogger(__name__)

# шаблон для чистки сообщений
BAD_PART = re.compile(r'^\[\S+|S+\],\s?')


def extract(input_data_pth: str, output_data_pth: str):
    # читаем сообщения
    try:
        comments = pd.read_csv(input_data_pth, sep=";")
    except IOError as err:
        _logger.error("File read error: %s, %s", input_data_pth, repr(err))
        return

    comments = comments.dropna().reset_index(drop=True)
    comments = comments.rename(columns={'text': 'msg'})
    comments['msg'] = comments['msg'].apply(lambda x: BAD_PART.sub('', x, 1).strip())

    if len(comments) == 0:
        _logger.info("No comments was found. File is empty")

    # парсим топонимы
    toponims = ToponimParserYargo(comments[['datetime', 'msg', 'user_name']])
    toponims.pars_all()

    # название отчета формируется из слова report_ и текущуй даты и текущего времени.
    report = os.path.join(output_data_pth, 'report_' + str(datetime.now().strftime("%d_%m_%Y_%H_%M_%S")) + '.csv')
    toponims.to_csv(report)