import redis

def set_redis_connection():
    redis_cli=redis.Redis(host='127.0.0.1',port=6379,db=0)
    return redis_cli

if __name__=='__main__':
    redis_cli=set_redis_connection()
    print redis_cli.get('name')
