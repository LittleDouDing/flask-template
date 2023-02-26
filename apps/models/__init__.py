#!/usr/bin/env python
# -*- coding: utf-8 -*-
from aioredis.client import Redis
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


async def connect_redis():
    redis = Redis()
    redis = await redis.from_url("redis://127.0.0.1", port="3306", password="XXXXXX", encoding='utf-8',
                                 decode_responses=True)
    return redis


async def get_value(key):
    redis = await connect_redis()
    value = await redis.get(key)
    await redis.close()
    return value


async def set_value(key, value, expire=300):
    redis = await connect_redis()
    await redis.set(key, value)
    await redis.expire(key, expire)
    await redis.close()


async def set_times(key, expire=1800):
    redis = await connect_redis()
    await redis.incr(key)
    await redis.expire(key, expire)
    await redis.close()


async def delete_key(key):
    redis = await connect_redis()
    await redis.delete(key)
    await redis.close()


async def get_keys():
    redis = await connect_redis()
    keys = await redis.keys()
    await redis.close()
    return keys
