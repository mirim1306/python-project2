import json
import os
import hashlib
import re

class UserManager:
    def __init__(self):
        self.users_file = "users.json"
        self.current_user = None
        self.load_users()

    def load_users(self):
        # 사용자 데이터 로드
        if os.path.exists(self.users_file):
            try:
                with open(self.users_file, 'r', encoding='utf-8') as f:
                    self.users = json.load(f)
            except:
                self.users = {}
        else:
            self.users = {}

    def save_users(self):
        # 사용자 데이터 저장
        with open(self.users_file, 'w', encoding='utf-8') as f:
            json.dump(self.users, f, ensure_ascii=False, indent=4)

    def hash_password(self, password):
        # 비밀번호
        return hashlib.sha256(password.encode()).hexdigest()

    def is_valid_username(self, username):
        # 아이디 유효성 검사 - 영문, 숫자만 허용
        if ' ' in username or not username.strip():
            return False, "공백은 사용할 수 없습니다."

        # 영문자와 숫자만 허용
        if not re.match(r'^[a-zA-Z0-9]+$', username):
            return False, "영문자와 숫자만 사용 가능합니다."

        return True, ""

    def is_valid_password(self, password):
        # 비밀번호 유효성 검사 - 공백 불가
        if ' ' in password or not password.strip():
            return False, "공백은 사용할 수 없습니다."

        return True, ""

    def register(self, username, password):
        """회원가입"""
        # 아이디 유효성 검사
        valid, message = self.is_valid_username(username)
        if not valid:
            return False, message

        # 비밀번호 유효성 검사
        valid, message = self.is_valid_password(password)
        if not valid:
            return False, message

        if username in self.users:
            return False, "이미 존재하는 아이디입니다."

        if len(username) < 3:
            return False, "아이디는 3자 이상이어야 합니다."

        if len(password) < 4:
            return False, "비밀번호는 4자 이상이어야 합니다."

        self.users[username] = {
            'password': self.hash_password(password),
            'total_score': 0,
            'games_played': 0,
            'best_score': 0
        }
        self.save_users()
        return True, "회원가입 성공!"

    def login(self, username, password):
        # 로그인
        if username not in self.users:
            return False, "존재하지 않는 아이디입니다."

        if self.users[username]['password'] != self.hash_password(password):
            return False, "비밀번호가 틀렸습니다."

        self.current_user = username
        return True, "로그인 성공!"

    def add_score(self, money, health, difficulty, map_type):
        # 점수 추가
        if not self.current_user:
            return

        # 점수 계산: 남은 당근 + (체력 * 10)
        base_score = money + (health * 10)

        # 난이도 보너스
        difficulty_bonus = {
            'easy': 1.0,
            'normal': 1.5,
            'hard': 2.0
        }

        # 맵 보너스
        map_bonus = {
            'field': 1.0,
            'desert': 1.2,
            'snow_mountain': 1.5
        }

        final_score = int(base_score * difficulty_bonus.get(difficulty, 1.0) * map_bonus.get(map_type, 1.0))

        user_data = self.users[self.current_user]
        user_data['total_score'] += final_score
        user_data['games_played'] += 1

        if final_score > user_data['best_score']:
            user_data['best_score'] = final_score

        self.save_users()
        return final_score

    def get_rankings(self):
        # 전체 랭킹 가져오기 (총점 기준)
        rankings = []
        for username, data in self.users.items():
            rankings.append({
                'username': username,
                'total_score': data['total_score'],
                'games_played': data['games_played'],
                'best_score': data['best_score']
            })

        rankings.sort(key=lambda x: x['total_score'], reverse=True)
        return rankings

    def get_current_user_data(self):
        # 현재 사용자 데이터
        if self.current_user:
            return self.users[self.current_user]
        return None

    def logout(self):
        # 로그아웃
        self.current_user = None