import logging

log = logging.getLogger('pythonie')


def configure_redis(redis_url, test=False):
    if test:
        log.info('Configuring redis for test')
        import fakeredis

        return fakeredis.FakeStrictRedis()

    if redis_url:
        import redis
        from urllib.parse import urlparse

        url = urlparse(redis_url)
        log.info('Redis configured with redis_url: %s' % redis_url)
        return redis.Redis(host=url.hostname,
                           port=url.port,
                           password=url.password)

    log.warn('Redis not configured')
