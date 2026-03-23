import mysql.connector
from mysql.connector import Error
import hashlib
from datetime import datetime

class UserDatabase:
    def __init__(self, host='localhost', database='rabbit_defense', user='root', password=''):
        # MySQL 데이터베이스 연결 초기화
        self.host = host
        self.database = database
        self.user = user
        self.password = password
        self.connection = None
        self.current_user_id = None
        self.current_username = None

    def connect(self):
        # 데이터베이스 연결
        try:
            self.connection = mysql.connector.connect(
                host=self.host,
                database=self.database,
                user=self.user,
                password=self.password
            )
            if self.connection.is_connected():
                print("MySQL 데이터베이스에 연결되었습니다.")
                return True
        except Error as e:
            print(f"데이터베이스 연결 오류: {e}")
            return False

    def disconnect(self):
        # 데이터베이스 연결 해제
        if self.connection and self.connection.is_connected():
            self.connection.close()
            print("MySQL 데이터베이스 연결이 종료되었습니다.")

    def hash_password(self, password):
        # 비밀번호
        return hashlib.sha256(password.encode()).hexdigest()

    def is_valid_username(self, username):
        # 아이디 유효성 검사
        import re
        if ' ' in username or not username.strip():
            return False, "공백은 사용할 수 없습니다."

        if not re.match(r'^[a-zA-Z0-9]+$', username):
            return False, "영문자와 숫자만 사용 가능합니다."

        return True, ""

    def is_valid_password(self, password):
        # 비밀번호 유효성 검사
        if ' ' in password or not password.strip():
            return False, "공백은 사용할 수 없습니다."

        return True, ""

    def register(self, username, password):
        # 회원가입
        # 유효성 검사
        valid, message = self.is_valid_username(username)
        if not valid:
            return False, message

        valid, message = self.is_valid_password(password)
        if not valid:
            return False, message

        if len(username) < 3:
            return False, "아이디는 3자 이상이어야 합니다."

        if len(password) < 4:
            return False, "비밀번호는 4자 이상이어야 합니다."

        try:
            cursor = self.connection.cursor()

            # 중복 확인
            check_query = "SELECT user_id FROM users WHERE username = %s"
            cursor.execute(check_query, (username,))
            if cursor.fetchone():
                cursor.close()
                return False, "이미 존재하는 아이디입니다."

            # 사용자 등록
            insert_query = """
                INSERT INTO users (username, password_hash, total_score, games_played, best_score)
                VALUES (%s, %s, 0, 0, 0)
            """
            cursor.execute(insert_query, (username, self.hash_password(password)))
            self.connection.commit()
            cursor.close()

            return True, "회원가입 성공!"

        except Error as e:
            print(f"회원가입 오류: {e}")
            return False, "회원가입 중 오류가 발생했습니다."

    def login(self, username, password):
        # 로그인
        try:
            cursor = self.connection.cursor(dictionary=True)

            query = """
                SELECT user_id, username, password_hash 
                FROM users 
                WHERE username = %s
            """
            cursor.execute(query, (username,))
            user = cursor.fetchone()

            if not user:
                cursor.close()
                return False, "존재하지 않는 아이디입니다."

            if user['password_hash'] != self.hash_password(password):
                cursor.close()
                return False, "비밀번호가 틀렸습니다."

            # 로그인 성공 - 마지막 로그인 시간 업데이트
            self.current_user_id = user['user_id']
            self.current_username = user['username']

            update_query = "UPDATE users SET last_login = NOW() WHERE user_id = %s"
            cursor.execute(update_query, (self.current_user_id,))
            self.connection.commit()
            cursor.close()

            return True, "로그인 성공!"

        except Error as e:
            print(f"로그인 오류: {e}")
            return False, "로그인 중 오류가 발생했습니다."

    def add_score(self, money, health, difficulty, map_type, waves_completed):
        # 점수 추가 및 게임 기록 저장
        if not self.current_user_id:
            return 0

        try:
            # 점수 계산
            base_score = money + (health * 10)

            difficulty_bonus = {
                'easy': 1.0,
                'normal': 1.5,
                'hard': 2.0
            }

            map_bonus = {
                'field': 1.0,
                'desert': 1.2,
                'snow_mountain': 1.5
            }

            final_score = int(base_score * difficulty_bonus.get(difficulty, 1.0) *
                              map_bonus.get(map_type, 1.0))

            cursor = self.connection.cursor()

            # 사용자 점수 업데이트
            update_query = """
                UPDATE users 
                SET total_score = total_score + %s,
                    games_played = games_played + 1,
                    best_score = GREATEST(best_score, %s)
                WHERE user_id = %s
            """
            cursor.execute(update_query, (final_score, final_score, self.current_user_id))

            # 게임 기록 저장
            insert_query = """
                INSERT INTO game_records 
                (user_id, map_type, difficulty, final_score, waves_completed, 
                 final_money, final_health)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """
            cursor.execute(insert_query,
                           (self.current_user_id, map_type, difficulty, final_score,
                            waves_completed, money, health))

            self.connection.commit()
            cursor.close()

            return final_score

        except Error as e:
            print(f"점수 추가 오류: {e}")
            return 0

    def get_rankings(self, limit=10):
        # 랭킹 조회
        try:
            cursor = self.connection.cursor(dictionary=True)

            query = """
                SELECT username, total_score, games_played, best_score
                FROM users
                ORDER BY total_score DESC, best_score DESC
                LIMIT %s
            """
            cursor.execute(query, (limit,))
            rankings = cursor.fetchall()
            cursor.close()

            return rankings

        except Error as e:
            print(f"랭킹 조회 오류: {e}")
            return []

    def get_user_stats(self):
        # 현재 사용자 통계
        if not self.current_user_id:
            return None

        try:
            cursor = self.connection.cursor(dictionary=True)

            query = """
                SELECT username, total_score, games_played, best_score, 
                       last_login, created_at
                FROM users
                WHERE user_id = %s
            """
            cursor.execute(query, (self.current_user_id,))
            stats = cursor.fetchone()
            cursor.close()

            return stats

        except Error as e:
            print(f"통계 조회 오류: {e}")
            return None

    def get_user_game_history(self, limit=10):
        # 사용자 게임 기록 조회
        if not self.current_user_id:
            return []

        try:
            cursor = self.connection.cursor(dictionary=True)

            query = """
                SELECT map_type, difficulty, final_score, waves_completed,
                       final_money, final_health, play_date
                FROM game_records
                WHERE user_id = %s
                ORDER BY play_date DESC
                LIMIT %s
            """
            cursor.execute(query, (self.current_user_id, limit))
            history = cursor.fetchall()
            cursor.close()

            return history

        except Error as e:
            print(f"기록 조회 오류: {e}")
            return []

    def logout(self):
        # 로그아웃
        self.current_user_id = None
        self.current_username = None

    @property
    def current_user(self):
        # 현재 로그인한 사용자명
        return self.current_usernameimport mysql.connector
from mysql.connector import Error
import hashlib
from datetime import datetime

class UserDatabase:
    def __init__(self, host='localhost', database='rabbit_defense', user='root', password=''):
        # MySQL 데이터베이스 연결 초기화
        self.host = host
        self.database = database
        self.user = user
        self.password = password
        self.connection = None
        self.current_user_id = None
        self.current_username = None

    def connect(self):
        # 데이터베이스 연결
        try:
            self.connection = mysql.connector.connect(
                host=self.host,
                database=self.database,
                user=self.user,
                password=self.password
            )
            if self.connection.is_connected():
                print("MySQL 데이터베이스에 연결되었습니다.")
                return True
        except Error as e:
            print(f"데이터베이스 연결 오류: {e}")
            return False

    def disconnect(self):
        # 데이터베이스 연결 해제
        if self.connection and self.connection.is_connected():
            self.connection.close()
            print("MySQL 데이터베이스 연결이 종료되었습니다.")

    def hash_password(self, password):
        # 비밀번호
        return hashlib.sha256(password.encode()).hexdigest()

    def is_valid_username(self, username):
        # 아이디 유효성 검사
        import re
        if ' ' in username or not username.strip():
            return False, "공백은 사용할 수 없습니다."

        if not re.match(r'^[a-zA-Z0-9]+$', username):
            return False, "영문자와 숫자만 사용 가능합니다."

        return True, ""

    def is_valid_password(self, password):
        # 비밀번호 유효성 검사
        if ' ' in password or not password.strip():
            return False, "공백은 사용할 수 없습니다."

        return True, ""

    def register(self, username, password):
        # 회원가입
        # 유효성 검사
        valid, message = self.is_valid_username(username)
        if not valid:
            return False, message

        valid, message = self.is_valid_password(password)
        if not valid:
            return False, message

        if len(username) < 3:
            return False, "아이디는 3자 이상이어야 합니다."

        if len(password) < 4:
            return False, "비밀번호는 4자 이상이어야 합니다."

        try:
            cursor = self.connection.cursor()

            # 중복 확인
            check_query = "SELECT user_id FROM users WHERE username = %s"
            cursor.execute(check_query, (username,))
            if cursor.fetchone():
                cursor.close()
                return False, "이미 존재하는 아이디입니다."

            # 사용자 등록
            insert_query = """
                INSERT INTO users (username, password_hash, total_score, games_played, best_score)
                VALUES (%s, %s, 0, 0, 0)
            """
            cursor.execute(insert_query, (username, self.hash_password(password)))
            self.connection.commit()
            cursor.close()

            return True, "회원가입 성공!"

        except Error as e:
            print(f"회원가입 오류: {e}")
            return False, "회원가입 중 오류가 발생했습니다."

    def login(self, username, password):
        # 로그인
        try:
            cursor = self.connection.cursor(dictionary=True)

            query = """
                SELECT user_id, username, password_hash 
                FROM users 
                WHERE username = %s
            """
            cursor.execute(query, (username,))
            user = cursor.fetchone()

            if not user:
                cursor.close()
                return False, "존재하지 않는 아이디입니다."

            if user['password_hash'] != self.hash_password(password):
                cursor.close()
                return False, "비밀번호가 틀렸습니다."

            # 로그인 성공 - 마지막 로그인 시간 업데이트
            self.current_user_id = user['user_id']
            self.current_username = user['username']

            update_query = "UPDATE users SET last_login = NOW() WHERE user_id = %s"
            cursor.execute(update_query, (self.current_user_id,))
            self.connection.commit()
            cursor.close()

            return True, "로그인 성공!"

        except Error as e:
            print(f"로그인 오류: {e}")
            return False, "로그인 중 오류가 발생했습니다."

    def add_score(self, money, health, difficulty, map_type, waves_completed):
        # 점수 추가 및 게임 기록 저장
        if not self.current_user_id:
            return 0

        try:
            # 점수 계산
            base_score = money + (health * 10)

            difficulty_bonus = {
                'easy': 1.0,
                'normal': 1.5,
                'hard': 2.0
            }

            map_bonus = {
                'field': 1.0,
                'desert': 1.2,
                'snow_mountain': 1.5
            }

            final_score = int(base_score * difficulty_bonus.get(difficulty, 1.0) *
                              map_bonus.get(map_type, 1.0))

            cursor = self.connection.cursor()

            # 사용자 점수 업데이트
            update_query = """
                UPDATE users 
                SET total_score = total_score + %s,
                    games_played = games_played + 1,
                    best_score = GREATEST(best_score, %s)
                WHERE user_id = %s
            """
            cursor.execute(update_query, (final_score, final_score, self.current_user_id))

            # 게임 기록 저장
            insert_query = """
                INSERT INTO game_records 
                (user_id, map_type, difficulty, final_score, waves_completed, 
                 final_money, final_health)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """
            cursor.execute(insert_query,
                           (self.current_user_id, map_type, difficulty, final_score,
                            waves_completed, money, health))

            self.connection.commit()
            cursor.close()

            return final_score

        except Error as e:
            print(f"점수 추가 오류: {e}")
            return 0

    def get_rankings(self, limit=10):
        # 랭킹 조회
        try:
            cursor = self.connection.cursor(dictionary=True)

            query = """
                SELECT username, total_score, games_played, best_score
                FROM users
                ORDER BY total_score DESC, best_score DESC
                LIMIT %s
            """
            cursor.execute(query, (limit,))
            rankings = cursor.fetchall()
            cursor.close()

            return rankings

        except Error as e:
            print(f"랭킹 조회 오류: {e}")
            return []

    def get_user_stats(self):
        # 현재 사용자 통계
        if not self.current_user_id:
            return None

        try:
            cursor = self.connection.cursor(dictionary=True)

            query = """
                SELECT username, total_score, games_played, best_score, 
                       last_login, created_at
                FROM users
                WHERE user_id = %s
            """
            cursor.execute(query, (self.current_user_id,))
            stats = cursor.fetchone()
            cursor.close()

            return stats

        except Error as e:
            print(f"통계 조회 오류: {e}")
            return None

    def get_user_game_history(self, limit=10):
        # 사용자 게임 기록 조회
        if not self.current_user_id:
            return []

        try:
            cursor = self.connection.cursor(dictionary=True)

            query = """
                SELECT map_type, difficulty, final_score, waves_completed,
                       final_money, final_health, play_date
                FROM game_records
                WHERE user_id = %s
                ORDER BY play_date DESC
                LIMIT %s
            """
            cursor.execute(query, (self.current_user_id, limit))
            history = cursor.fetchall()
            cursor.close()

            return history

        except Error as e:
            print(f"기록 조회 오류: {e}")
            return []

    def logout(self):
        # 로그아웃
        self.current_user_id = None
        self.current_username = None

    @property
    def current_user(self):
        # 현재 로그인한 사용자명
        return self.current_username
