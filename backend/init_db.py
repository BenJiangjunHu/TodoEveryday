#!/usr/bin/env python3
"""
数据库初始化脚本
"""
from app.database import engine, Base
from app.models import Todo
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def init_db():
    """初始化数据库"""
    logger.info("正在创建数据库表...")
    Base.metadata.create_all(bind=engine)
    logger.info("数据库表创建完成!")

def reset_db():
    """重置数据库"""
    logger.info("正在重置数据库...")
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    logger.info("数据库重置完成!")

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "reset":
        reset_db()
    else:
        init_db()
