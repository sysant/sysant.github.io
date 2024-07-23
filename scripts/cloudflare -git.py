#!/usr/bin/python
# -*- coding: UTF-8 -*-
# version: by san at 20201202
# cloudflare refresh api

import json
import requests
import sys
import copy
import argparse


def parse_args():
    parser = argparse.ArgumentParser(description="Cloudflare cdn refresh dir.")
    parser.add_argument('--os_dir', dest='os_dir', type=str, choices=("ios", "android"), help='optional os dir.')
    parser.add_argument('--branch', dest='branch', type=str, choices=("release", "patch", "int"), default="release",
                           help='optional branch dir;default release.')
    parser.add_argument('--version', dest='version', type=str, default='bundles',
                           help='optional version dir;default bundles.')
    parser.add_argument('--fname', dest='fname', type=str, help='optional is a file name.')
    parser.add_argument('--type', dest='type', type=str, choices=('paht','url'), default='path', 
                           help='optional is refresh url or path;default path')
    args = parser.parse_args()
    return args

# cloudflare cdn api 需要到cloudflare web控制台查找"
api = 'https://api.cloudflare.com/client/v4/zones/xxxxxxxxxxxxx/purge_cache'  # DOMAMIN  example "test.com"




# 针对目录刷新函数
def purge_msg_dir(api, url):
    headers = {'Content-Type': 'application/json; charset=utf-8', 'X-Auth-Email': 'xxx@xxx', 'X-Auth-Key': 'xxxxxxxxxxxxxx'}
    data = {
                 "prefixes": url
       }
    r = requests.post(api, data=json.dumps(data), headers=headers)
    return r.text


# 针对文件刷新函数
def purge_msg_url(api, url):
    headers = {'Content-Type': 'application/json; charset=utf-8', 'X-Auth-Email': 'xxx@xxx', 'X-Auth-Key': 'xxxxxxxxxxxxxx'}
    data = {
                 "files": url
       }
    r = requests.post(api, data=json.dumps(data), headers=headers)
    return r.text


if __name__ == '__main__':
    url_dirs = []    # 刷新路径必须存到列表
    url_https = []   # 刷新url必须存放到列表
    Prefix_url = "YOURDOMAIN/"   # 域名   不需要加http或https  如test.com/
    args = parse_args()
    if len(sys.argv) == 1:
        print("没有给参数,请尝试获取帮助说明 %s -h" % sys.argv[0])
        sys.exit(1)
    else:
        print(args.os_dir, args.branch, args.version, args.fname)
    if args.fname:       # https://test-cdn.test.com/cdn/ios/release/version/test.txt
        https_url = 'https://' + Prefix_url + 'DIR/' + args.os_dir + '/' + args.branch + '/' + args.version + '/' + args.fname
        url_https.append(https_url)
        print("刷新url : %s" % url_https)
        print(purge_msg_url(api, url_https))
    else:                  https://test-cdn.test.com/cdn/ios/release/version/
        url_dir = Prefix_url + 'DIR/' + args.os_dir + '/' + args.branch + '/' + args.version + '/'
        print(url_dir)
        url_dirs.append(url_dir)
        print("刷新目录路径 : %s" % url_dir)
        print(purge_msg_dir(api, url_dirs))
