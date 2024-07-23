#coding:utf-8
import redis
import time
import sys
from threading import Thread, current_thread

# 开启进程数
t = 4
# 连接密码
Password=''
# redis 主机
Host='192.168.1.88'
# 默认端口6379
Port=6379
# 默认DB 0
DB=0
# 连接
r = redis.Redis(host=Host,password=Password,port=Port,db=DB)

# 清key功能块
def clear_redis(key):
    keys = r.keys('%s:*' % key)
    for k in keys:
        r.delete(k)

if __name__ == '__main__':
    start_time = time.time()
    print(start_time)
    if len(sys.argv) <= 1:
        sys.exit("Error!!!!, Like this 'python %s 111111'" % sys.argv[0])
    else:
        arg = sys.argv[1]
        print("Clear keys is %s:*" % arg)

    try:
        r.ping()
    except:
        print("Redis connect failed.No password?")
    else:
        threads = [Thread(target=clear_redis,args=(arg,)) for _ in range(t)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()
    print '%d second'% (time.time()-start_time)
