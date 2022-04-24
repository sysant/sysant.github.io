#!/usr/bin/python
# -*- coding: utf8 -*-

# 腾讯云官方帮助文档
'''
# https://intl.cloud.tencent.com/zh/document/product/228/31719
# https://console.intl.cloud.tencent.com/api/explorer?Product=cdn&Version=2018-06-06&Action=PurgePathCache&SignVersion=
'''

import json, sys
import argparse
from tencentcloud.common import credential
from tencentcloud.common.profile.client_profile import ClientProfile
from tencentcloud.common.profile.http_profile import HttpProfile
from tencentcloud.common.exception.tencent_cloud_sdk_exception import TencentCloudSDKException
from tencentcloud.cdn.v20180606 import cdn_client, models

# 定义脚本参数
def parse_args():
    parser = argparse.ArgumentParser(description="Cloudflare cdn refresh dir.")
    parser.add_argument('--os_dir', dest='os_dir', type=str, choices=("ios", "android"), help='选项为平台,必须存在.')
    parser.add_argument('--branch', dest='branch', type=str, choices=("release", "patch", "int"), default="release",
                        help='选项为分支目录;默认release.')
    parser.add_argument('--version', dest='version', type=str, default='bundles',
                        help='选项为版本目录;默认bundles.')
    parser.add_argument('--fname', dest='fname', type=str, help='选项包含文件名fname,在刷新url或预热url时必须存在')
    parser.add_argument('--type', dest='type', type=str, choices=("fpath", "purl", "furl"), default='fpath',
                        help='选项包含 刷新furl or 刷新目录fpath or 预热purl;默认fpath')
    args = parser.parse_args()
    return args

# 刷新id与key 你有权限的id和密钥key
secret_id = ''
secret_key = ''

# 腾讯云 cdn 地址 如： https://test-cdn.test.com/
prex_base_url = ''

# 刷新目录类型 flush:下新增加资源; delete：刷新全部资源
flush_type = 'flush'   # flush 刷新目录下新增加资源; delete：刷新全部资源

# 刷新url 区域
Area = 'overseas'

# 封装腾讯云目录刷新和地址刷新函数
def TxPathApi(SecretId, SecretKey,fun,Params):
    '''
     fpath:刷新目录
     furl: 刷新单个url
     purl: 预热单个url
    '''
    try:
        cred = credential.Credential(secret_id, secret_key)
        httpProfile = HttpProfile()
        httpProfile.endpoint = "cdn.tencentcloudapi.com"
        clientProfile = ClientProfile()
        clientProfile.httpProfile = httpProfile
        client = cdn_client.CdnClient(cred, "", clientProfile)
        if fun == "fpath":
            req = models.PurgePathCacheRequest()
            # 刷新参数params = {
            #          'Path':['https://test-cdn.test.com/cdn/ios/release/1'],
            #           'flushType': 'flush'}
            params = Params
            req.from_json_string(json.dumps(params))
            resp = client.PurgePathCache(req)
            print(resp.to_json_string())
        elif fun == 'purl':
            req = models.PushUrlsCacheRequest()
            # 刷新参数 params={'Urls': ['https://test-cdn.test.com/cdn/ios/release/test.txt'], 'Area': 'overseas'}
            params = Params
            req.from_json_string(json.dumps(params))
            resp = client.PushUrlsCache(req)
            print(resp.to_json_string())            
        else:
            req = models.PurgeUrlsCacheRequest()
            # 刷新参数 params={'Urls': ['https://test-cdn.test.com/cdn/ios/release/test.txt'], 'Area': 'overseas'}
            params = Params
            req.from_json_string(json.dumps(params))
            resp = client.PurgeUrlsCache(req)  #刷新
            print(resp.to_json_string())
    except TencentCloudSDKException as err:
        print(err)

if __name__ == '__main__':
    args  = parse_args()
    if len(sys.argv) == 1:
        print("No args input,please %s -h" % sys.argv[0])
        sys.exit(1)
    else:
        print(args.os_dir, args.branch, args.version, args.fname)

    Paths = []
    params = {}
    if args.type and args.type == 'fpath':
        # 刷新目录fpath (方法:PurgePathCache)        
        try:
            cdn_dir  = prex_base_url + 'cdn/' + args.os_dir + '/' + args.branch + '/' + args.version + '/' 
            Paths.append(cdn_dir)
            params['Paths'] = Paths
            params['FlushType'] = 'flush'
            print('提交刷新的目录:%s' % Paths)
            TxPathApi(secret_id,secret_key,args.type,params)
        except:
            print("获取帮助: %s -h " % sys.argv[0])
            print("试试: %s --os_dir XX  --branch YY --version ZZ --type path " % sys.argv[0])
    elif args.type and 'url' in  args.type:
        try:
            cdn_url = prex_base_url + 'cdn/' + args.os_dir + '/' + args.branch + '/' \
                      + args.version + '/' + args.fname
            Paths.append(cdn_url)
            params['Urls'] = Paths
            params['Area'] = Area
            # 如果是furl则是提交刷新(PurgeUrlsCache);否则是提交预热url(purl:PushUrlsCache)
            if args.type == "furl":
                print('提交刷新的路径:%s' % Paths)
                TxPathApi(secret_id,secret_key,args.type,params)
            else:
                print('提交预热的路径:%s' % Paths)
                TxPathApi(secret_id,secret_key,args.type,params)
        except:
            print("获取帮助: %s -h " % sys.argv[0])
            print("必须要有--fname;试试: %s --os_dir XX  --branch YY --version ZZ --fname AA --type furl " % sys.argv[0])
    else:
         print("参数是否少--type ?")
         sys.exit(1)
