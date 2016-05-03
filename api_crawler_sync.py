#!/usr/bin/env python
import timeit
import requests
import json


channelid_map = {
        1: '飞碟说', 2: '飞碟一分钟', 3: '飞碟唱',
        4: '飞碟冷知识', 5: '飞碟实验室', 6: '飞碟宝贝计划',
        7: '飞碟啪', 8: '飞碟词库',
        13: '飞碟爱美丽', 14: '飞碟说人物', 15: '飞碟头条',
        20: '校够了没', 21: '默默说', 22: '今天听什么'
}


def crawl_with_api_load_more():
    host = 'http://feidieshuo.com/media/load_more'

    def get_totalPages():
        response = requests.get(host+'?page=0').json()
        return response['totalPages']

    totalPages = get_totalPages()
    result = []

    for page in range(1, totalPages+1):
        query = '?page={}'.format(page)
        response = requests.get(host+query).json()
        for rec in response['records']:
            result.append(rec)
            print(rec['mp4'])

    with open('result_load_more_sync.json', 'w') as outputfile:
        for item in json.dumps(result, ensure_ascii=False, indent=4):
            outputfile.write(item)
    return result


def crawl_with_api_load_more_channel_video():
    result = []

    def crawl_channel(channelid):
        host = 'http://feidieshuo.com/media/load_more_channle_video'
        result_tem = []

        def get_channel_totalPages():
            response = requests.get(host+'?page=0&channelid={}'.format(channelid))
            return response.json()['totalPages']

        totalPages = get_channel_totalPages()

        for page in range(1, totalPages+1):
            query = '?page={}&channelid={}'.format(page, channelid)
            response = requests.get(host+query).json()
            for rec in response['records']:
                result.append(rec)
                print(rec['mp4'])
        return result_tem

    for channleid in channelid_map.keys():
        result.extend(crawl_channel(channleid))

    with open('result_load_more_channle_video_sync.json', 'w') as outputfile:
        for item in json.dumps(result, ensure_ascii=False, indent=4):
            outputfile.write(item)

    return result


if __name__ == '__main__':
    print(timeit.timeit('crawl_with_api_load_more()', number=1, globals=globals()))
    print(timeit.timeit('crawl_with_api_load_more_channel_video()', number=1, globals=globals()))
