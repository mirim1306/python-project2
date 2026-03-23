import pygame
import time

from GameManager import GameManager
from Enemy import Enemy
from Map import Map
from UIManager import UIManager
from StartScreen import StartScreen
from InfoScreen import InfoScreen
from MapSelectScreen import MapSelectScreen
from DifficultySelectScreen import DifficultySelectScreen
from LoginScreen import LoginScreen
from RankingScreen import RankingScreen
from UserDatabase import UserDatabase
from config import CURRENT_DB

TOP_BAR_HEIGHT = 50
SIDEBAR_WIDTH = 200
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
MAP_AREA_WIDTH = SCREEN_WIDTH - SIDEBAR_WIDTH
MAP_AREA_HEIGHT = SCREEN_HEIGHT - TOP_BAR_HEIGHT

class MainGame:
    def __init__(self):
        pygame.init()

        # 1. 전체 화면 설정 및 해상도 가져오기
        info = pygame.display.Info()
        self.SCREEN_WIDTH = info.current_w
        self.SCREEN_HEIGHT = info.current_h

        # 전체 화면 모드 설정
        self.screen = pygame.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT), pygame.FULLSCREEN)

        self.clock = pygame.time.Clock()
        self.FPS = 60

        # 게임 상태 - 시작 화면부터 시작
        self.game_state = "start"  # "start", "login", "map_select", "difficulty_select", "info", "ranking", "playing"

        # 사용자 관리 - MySQL 사용
        self.user_manager = UserDatabase(**CURRENT_DB)

        # 데이터베이스 연결
        if not self.user_manager.connect():
            print("데이터베이스 연결 실패. JSON 파일 모드로 전환합니다.")
            # 대체: JSON 기반 UserManager 사용
            from UserManager import UserManager
            self.user_manager = UserManager()

        # 화면들
        self.login_screen = LoginScreen(self.SCREEN_WIDTH, self.SCREEN_HEIGHT)
        self.start_screen = StartScreen(self.SCREEN_WIDTH, self.SCREEN_HEIGHT)
        self.info_screen = InfoScreen(self.SCREEN_WIDTH, self.SCREEN_HEIGHT)
        self.map_select_screen = MapSelectScreen(self.SCREEN_WIDTH, self.SCREEN_HEIGHT)
        self.difficulty_select_screen = DifficultySelectScreen(self.SCREEN_WIDTH, self.SCREEN_HEIGHT)
        self.ranking_screen = RankingScreen(self.SCREEN_WIDTH, self.SCREEN_HEIGHT)

        self.running = True

        # 게임 설정 저장
        self.selected_map = None
        self.selected_map_image = None
        self.selected_difficulty = None

        # 게임 초기화는 나중에
        self.game_initialized = False

    def initialize_game(self):
        # 게임 시작 시 초기화
        # 난이도에 따른 초기 설정
        if self.selected_difficulty == 'easy':
            initial_health = 150
            initial_money = 150
        elif self.selected_difficulty == 'hard':
            initial_health = 50
            initial_money = 80
        else:
            initial_health = 100
            initial_money = 100

        self.game_manager = GameManager(wave=0, health=initial_health, money=initial_money)

        # 2. 화면 분할 상수 정의 (전체 화면 기준 비율)
        self.TOP_BAR_HEIGHT = int(self.SCREEN_HEIGHT * 0.08)
        self.SIDEBAR_WIDTH = int(self.SCREEN_WIDTH * 0.20)

        self.MAP_AREA_WIDTH = self.SCREEN_WIDTH - self.SIDEBAR_WIDTH
        self.MAP_AREA_HEIGHT = self.SCREEN_HEIGHT - self.TOP_BAR_HEIGHT

        # 3. 맵별 경로 데이터 정의
        map_paths = {
            'field': [  # 들판 맵 경로
                (0, 125),
                (140, 125),
                (140, 490),
                (725, 490),
                (725, 190)
            ],
            'desert': [  # 사막 맵 경로
                (80, 0),
                (80, 240),
                (320, 240),
                (320, 435),
                (640, 435),
                (640, 290),
                (725, 290),
                (725, 100)
            ],
            'snow_mountain': [  # 설산 맵 경로
                (0, 525),
                (75, 525),
                (75, 60),
                (220, 60),
                (220, 525),
                (370, 525),
                (370, 265),
                (465, 265),
                (465, 60),
                (610, 60),
                (610, 450),
                (725, 450),
                (725, 190)
            ]
        }

        # 선택한 맵의 경로 가져오기
        raw_path_data = map_paths.get(self.selected_map, map_paths['field'])

        def scale_and_offset(coords):
            scaled_coords = []
            MAX_MAP_RAW_X = 800
            MAX_MAP_RAW_Y = 600

            for rx, ry in coords:
                scaled_x = int(rx / MAX_MAP_RAW_X * self.MAP_AREA_WIDTH)
                scaled_y = int(ry / MAX_MAP_RAW_Y * self.MAP_AREA_HEIGHT) + self.TOP_BAR_HEIGHT
                scaled_coords.append((scaled_x, scaled_y))
            return scaled_coords

        self.path_data = scale_and_offset(raw_path_data)

        # 4. Map, UIManager 초기화 (선택한 맵 이미지 사용)
        map_image = self.selected_map_image if self.selected_map_image else "images/field.png"

        self.current_map = Map(
            map_image_path=map_image,
            base_image_path="images/base.png",
            path_data=self.path_data,
            tower_spots=[],
            map_area_width=self.MAP_AREA_WIDTH,
            map_area_height=self.MAP_AREA_HEIGHT,
            top_bar_height=self.TOP_BAR_HEIGHT
        )

        self.ui_manager = UIManager(
            font="Arial", buttons=['타워1'],
            screen_width=self.SCREEN_WIDTH, screen_height=self.SCREEN_HEIGHT,
            top_bar_height=self.TOP_BAR_HEIGHT, sidebar_width=self.SIDEBAR_WIDTH
        )

        self.towers = []
        self.enemies = []
        self.projectiles = []
        self.last_wave_time = time.time()
        self.wave_interval = 60

        self.game_initialized = True

    def handle_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            # ESC 키로 전체화면 종료
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False

                # 로그인 화면에서 키보드 입력
                if self.game_state == "login":
                    result = self.login_screen.handle_key(event)
                    if result:
                        self.handle_login_action(result)

            # 마우스 클릭 처리
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if self.game_state == "start":
                    action = self.start_screen.handle_click(event.pos, self.user_manager.current_user)
                    if action == "start":
                        self.game_state = "map_select"
                    elif action == "info":
                        self.game_state = "info"
                    elif action == "ranking":
                        self.game_state = "ranking"
                    elif action == "login":
                        self.game_state = "login"
                        self.login_screen.clear_inputs()
                    elif action == "logout":
                        self.user_manager.logout()
                        self.login_screen.set_message("로그아웃 되었습니다.")
                    elif action == "quit":
                        self.running = False

                elif self.game_state == "login":
                    result = self.login_screen.handle_click(event.pos)
                    if result:
                        if result['action'] == 'back':
                            self.game_state = "start"
                        else:
                            self.handle_login_action(result)

                elif self.game_state == "ranking":
                    action = self.ranking_screen.handle_click(event.pos)
                    if action == "back":
                        self.game_state = "start"

                elif self.game_state == "map_select":
                    result = self.map_select_screen.handle_click(event.pos)
                    if result:
                        if result['action'] == 'back':
                            self.game_state = "start"
                        elif result['action'] == 'select_map':
                            self.selected_map = result['map']
                            self.selected_map_image = result['map_image']
                            self.game_state = "difficulty_select"

                elif self.game_state == "difficulty_select":
                    result = self.difficulty_select_screen.handle_click(event.pos)
                    if result:
                        if result['action'] == 'back':
                            self.game_state = "map_select"
                        elif result['action'] == 'select_difficulty':
                            self.selected_difficulty = result['difficulty']
                            if not self.game_initialized:
                                self.initialize_game()
                            self.game_state = "playing"

                elif self.game_state == "info":
                    action = self.info_screen.handle_click(event.pos)
                    if action == "back":
                        self.game_state = "start"

                elif self.game_state == "playing":
                    result = self.ui_manager.handle_click(event.pos, self.game_manager, self.current_map, self.towers)
                    # 나가기 버튼 클릭 시
                    if result == "exit_game":
                        self.end_game()
                    # 스킵 버튼 클릭 시
                    elif result == "skip_wave":
                        self.last_wave_time = time.time() - self.wave_interval

    def handle_login_action(self, result):
        # 로그인/회원가입 처리
        if result['action'] == 'login':
            success, message = self.user_manager.login(result['username'], result['password'])
            self.login_screen.set_message(message, not success)
            if success:
                self.game_state = "start"
        elif result['action'] == 'register':
            success, message = self.user_manager.register(result['username'], result['password'])
            self.login_screen.set_message(message, not success)

    def end_game(self):
        # 게임 종료 및 점수 저장
        if self.user_manager.current_user:
            waves_completed = self.game_manager.wave

            if self.game_manager.wave >= self.game_manager.MAX_WAVE:
                self.user_manager.add_score(
                    self.game_manager.money,
                    self.game_manager.health,
                    self.selected_difficulty,
                    self.selected_map,
                    waves_completed
                )
            else:
                self.user_manager.add_score(
                    self.game_manager.money,
                    self.game_manager.health,
                    self.selected_difficulty,
                    self.selected_map,
                    waves_completed
                )

        self.game_state = "start"
        self.game_initialized = False

    def wave_management(self):
        current_time = time.time()

        if (not self.enemies and
                current_time - self.last_wave_time > self.wave_interval and
                self.game_manager.wave < self.game_manager.MAX_WAVE):

            self.game_manager.wave += 1
            self.last_wave_time = current_time

            slime_types = [
                ('red', 'images/red_slime.png', 1.0, 5),
                ('orange', 'images/orange_slime.png', 1.0, 5),
                ('yellow', 'images/yellow_slime.png', 1.0, 10),
                ('green', 'images/green_slime.png', 1.0, 10),
                ('blue', 'images/blue_slime.png', 1.0, 15),
                ('navy', 'images/navy_slime.png', 1.0, 15),
                ('purple', 'images/purple_slime.png', 1.0, 20)
            ]

            wave = self.game_manager.wave

            # 난이도에 따른 적 속도 조정
            speed_multiplier = 1.0
            if self.selected_difficulty == 'easy':
                speed_multiplier = 0.8
            elif self.selected_difficulty == 'hard':
                speed_multiplier = 1.3

            # 맵에 따른 적 수 배율
            enemy_count_multiplier = 1.0
            if self.selected_map == 'field':
                enemy_count_multiplier = 1.0  # 기본
            elif self.selected_map == 'desert':
                enemy_count_multiplier = 1.5  # 사막: 50% 더 많음
            elif self.selected_map == 'snow_mountain':
                enemy_count_multiplier = 2.5  # 설산: 150% 더 많음

            # 웨이브별 슬라임 타입과 기본 적 수 결정
            if wave <= 3:
                slime_type, image, speed, money = slime_types[0]
                base_num_enemies = wave + 4
            elif wave <= 4:
                slime_type, image, speed, money = slime_types[1]
                base_num_enemies = wave + 2
            elif wave <= 5:
                slime_type, image, speed, money = slime_types[2]
                base_num_enemies = wave
            elif wave <= 6:
                slime_type, image, speed, money = slime_types[3]
                base_num_enemies = wave - 2
            elif wave <= 7:
                slime_type, image, speed, money = slime_types[4]
                base_num_enemies = wave - 4
            elif wave <= 8:
                slime_type, image, speed, money = slime_types[5]
                base_num_enemies = wave - 6
            else:
                slime_type, image, speed, money = slime_types[6]
                base_num_enemies = wave - 8

            # 맵 배율 적용
            num_enemies = int(base_num_enemies * enemy_count_multiplier)

            path = self.current_map.get_path()
            start_pos = list(self.current_map.get_cave_tower_pos())

            if len(path) > 1:
                dx = path[1][0] - path[0][0]
                dy = path[1][1] - path[0][1]
                dist = (dx ** 2 + dy ** 2) ** 0.5
                if dist > 0:
                    start_pos[0] -= (dx / dist) * 20
                    start_pos[1] -= (dy / dist) * 20

            for i in range(num_enemies):
                enemy = Enemy(
                    speed=speed * speed_multiplier,
                    money=money,
                    position=start_pos.copy(),
                    path_data=path,
                    enemy_type=slime_type,
                    image_path=image
                )
                self.enemies.append(enemy)

    def update(self):
        if self.game_state != "playing":
            return

        # 게임 업데이트 및 종료 체크
        should_continue = self.game_manager.update()

        # 게임 오버 또는 클리어 시
        if not should_continue:
            self.end_game()
            return

        # 적 이동
        enemies_to_remove = []
        for enemy in self.enemies:
            is_moving = enemy.move(self.game_manager)
            if not is_moving or not enemy.is_alive:
                enemies_to_remove.append(enemy)

        # 타워 공격
        for tower in self.towers:
            targets = tower.target(self.enemies)
            if targets:
                tower.attack(targets, self.projectiles)

        # 투사체 업데이트
        projectiles_to_remove = []
        for projectile in self.projectiles:
            projectile.update()
            if not projectile.is_active:
                if projectile.target and projectile.target.is_alive:
                    projectile.target.take_damage(self.game_manager, self.enemies)
                projectiles_to_remove.append(projectile)

        # 제거
        self.enemies[:] = [e for e in self.enemies if e not in enemies_to_remove]
        self.projectiles[:] = [p for p in self.projectiles if p not in projectiles_to_remove]

        # 웨이브 관리
        self.wave_management()

    def draw(self):
        if self.game_state == "start":
            self.start_screen.draw(self.screen, self.user_manager.current_user)

        elif self.game_state == "login":
            self.login_screen.draw(self.screen)

        elif self.game_state == "ranking":
            self.ranking_screen.draw(self.screen, self.user_manager)

        elif self.game_state == "map_select":
            self.map_select_screen.draw(self.screen)

        elif self.game_state == "difficulty_select":
            self.difficulty_select_screen.draw(self.screen)

        elif self.game_state == "info":
            self.info_screen.draw(self.screen)

        elif self.game_state == "playing":
            self.screen.fill((150, 150, 150))
            self.current_map.draw(self.screen)

            # 타워 그리기
            for tower in self.towers:
                tower.draw(self.screen)

            # 적 그리기
            for enemy in self.enemies:
                if enemy.is_alive:
                    enemy.draw(self.screen)

            # 투사체 그리기
            for projectile in self.projectiles:
                projectile.draw(self.screen)

            # 다음 웨이브까지 남은 시간 계산
            time_until_next_wave = None
            if not self.enemies and self.game_manager.wave < self.game_manager.MAX_WAVE:
                time_until_next_wave = self.wave_interval - (time.time() - self.last_wave_time)
                if time_until_next_wave < 0:
                    time_until_next_wave = 0

            # UI 그리기
            self.ui_manager.draw_hud(self.screen, self.game_manager, time_until_next_wave)
            self.ui_manager.draw_tower_menu(self.screen)

            # 분리선
            pygame.draw.line(self.screen, (0, 0, 0), (0, self.TOP_BAR_HEIGHT),(self.SCREEN_WIDTH, self.TOP_BAR_HEIGHT), 5)
            pygame.draw.line(self.screen, (0, 0, 0), (self.MAP_AREA_WIDTH, self.TOP_BAR_HEIGHT),(self.MAP_AREA_WIDTH, self.SCREEN_HEIGHT), 5)

        pygame.display.flip()

    def run(self):
        while self.running:
            self.handle_input()
            self.update()
            self.draw()
            self.clock.tick(self.FPS)

        # 게임 종료 시 데이터베이스 연결 해제
        if hasattr(self.user_manager, 'disconnect'):
            self.user_manager.disconnect()

        pygame.quit()

if __name__ == '__main__':
    game = MainGame()
    game.run()
