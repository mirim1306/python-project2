# MySQL 데이터베이스 설정
DB_CONFIG = {
    'host': 'localhost',
    'database': 'rabbit_defense',
    'user': 'root',
    'password': 'ghks084@'  # 여기에 MySQL 비밀번호 입력
}

# 또는 환경에 따라 다른 설정
DEVELOPMENT_DB = {
    'host': 'localhost',
    'database': 'rabbit_defense',
    'user': 'root',
    'password': 'ghks084@'
}

PRODUCTION_DB = {
    'host': 'localhost',
    'database': 'rabbit_defense',
    'user': 'root',
    'password': 'ghks084@'
}

# 현재 사용할 설정
CURRENT_DB = DEVELOPMENT_DB
