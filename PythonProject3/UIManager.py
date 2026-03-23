import pygame

from Tower import Tower

TOP_BAR_HEIGHT = 50
SIDEBAR_WIDTH = 200
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
MAP_AREA_WIDTH = SCREEN_WIDTH - SIDEBAR_WIDTH  # 600
MAP_AREA_HEIGHT = SCREEN_HEIGHT - TOP_BAR_HEIGHT  # 550

class UIManager:
    # __init__ 메소드에 새로운 크기 인수를 추가합니다.
    def __init__(self, font, buttons, screen_width, screen_height, top_bar_height, sidebar_width):
        pygame.font.init()
        # 한글 지원 폰트 사용
        try:
            self.font = pygame.font.SysFont('malgungothic', int(screen_height * 0.03))
        except:
            try:
                self.font = pygame.font.SysFont('nanumgothic', int(screen_height * 0.03))
            except:
                self.font = pygame.font.SysFont('gulim', int(screen_height * 0.03))

        self.buttons = buttons
        self.selected_tower_type = None

        # 화면 상수 저장
        self.SCREEN_WIDTH = screen_width
        self.SCREEN_HEIGHT = screen_height
        self.TOP_BAR_HEIGHT = top_bar_height
        self.SIDEBAR_WIDTH = sidebar_width
        self.MAP_AREA_WIDTH = screen_width - sidebar_width

        # 타워 소환창의 Rect를 우측 Sidebar 영역에 맞춥니다.
        self.TOWER_MENU_RECT = pygame.Rect(self.MAP_AREA_WIDTH, self.TOP_BAR_HEIGHT, self.SIDEBAR_WIDTH, screen_height - self.TOP_BAR_HEIGHT)

        # 나가기 버튼 추가
        exit_button_width = int(screen_width * 0.08)
        exit_button_height = int(top_bar_height * 0.6)
        exit_button_x = int(screen_width * 0.90)
        exit_button_y = int(top_bar_height * 0.2)
        self.exit_button_rect = pygame.Rect(exit_button_x, exit_button_y, exit_button_width, exit_button_height)

    def draw_hud(self, screen, game_manager, time_until_next_wave=None):
        # 배경 (HUD 영역: 0, 0 부터 SCREEN_WIDTH, TOP_BAR_HEIGHT)
        pygame.draw.rect(screen, (50, 50, 50), (0, 0, self.SCREEN_WIDTH, self.TOP_BAR_HEIGHT))

        # 텍스트 출력 (위치도 비율에 맞춰 조정)
        self._draw_text(screen, f"당근 : {game_manager.money}", (self.SCREEN_WIDTH * 0.01, self.TOP_BAR_HEIGHT * 0.3),(255, 255, 0))
        self._draw_text(screen, f"마을 HP : {game_manager.health}", (self.SCREEN_WIDTH * 0.15, self.TOP_BAR_HEIGHT * 0.3),(255, 0, 0))
        self._draw_text(screen, f"웨이브 : {game_manager.wave}/{game_manager.MAX_WAVE}",(self.SCREEN_WIDTH * 0.32, self.TOP_BAR_HEIGHT * 0.3), (255, 255, 255))

        # 점검 시간 표시
        if time_until_next_wave is not None and time_until_next_wave > 0:
            self._draw_text(screen, f"다음 웨이브: {int(time_until_next_wave)}초",(self.SCREEN_WIDTH * 0.48, self.TOP_BAR_HEIGHT * 0.3), (0, 255, 255))

            # 스킵 버튼
            skip_button_x = int(self.SCREEN_WIDTH * 0.65)
            skip_button_y = int(self.TOP_BAR_HEIGHT * 0.2)
            skip_button_width = int(self.SCREEN_WIDTH * 0.08)
            skip_button_height = int(self.TOP_BAR_HEIGHT * 0.6)

            self.skip_button_rect = pygame.Rect(skip_button_x, skip_button_y, skip_button_width, skip_button_height)
            pygame.draw.rect(screen, (0, 150, 0), self.skip_button_rect)
            pygame.draw.rect(screen, (255, 255, 255), self.skip_button_rect, 2)  # 테두리

            # 스킵 버튼 텍스트
            self._draw_text(screen, "스킵",(skip_button_x + skip_button_width * 0.15, skip_button_y + skip_button_height * 0.2),(255, 255, 255))
        else:
            self.skip_button_rect = None

        # 나가기 버튼
        pygame.draw.rect(screen, (150, 0, 0), self.exit_button_rect)
        pygame.draw.rect(screen, (255, 255, 255), self.exit_button_rect, 2)

        exit_text_x = self.exit_button_rect.x + self.exit_button_rect.width * 0.1
        exit_text_y = self.exit_button_rect.y + self.exit_button_rect.height * 0.2
        self._draw_text(screen, "나가기", (exit_text_x, exit_text_y), (255, 255, 255))

    def draw_tower_menu(self, screen):
        # 타워 소환창 배경 (우측 Sidebar 영역)
        pygame.draw.rect(screen, (100, 100, 100), self.TOWER_MENU_RECT)

        # 제목
        title_x = self.MAP_AREA_WIDTH + int(self.SIDEBAR_WIDTH * 0.05)
        title_y = self.TOP_BAR_HEIGHT + int(self.SCREEN_HEIGHT * 0.02)
        self._draw_text(screen, "타워 소환창", (title_x, title_y), (255, 255, 255))

        # 3개의 타워 버튼
        tower_data = [
            ("활 토깽이 (50)", "bow", 50, 1),
            ("워드 토깽이 (80)", "cane", 80, 3),
            ("폭탄 토깽이 (120)", "bomb", 120, 5)
        ]

        button_x = self.MAP_AREA_WIDTH + int(self.SIDEBAR_WIDTH * 0.1)
        button_width = int(self.SIDEBAR_WIDTH * 0.8)
        button_height = int(self.SCREEN_HEIGHT * 0.06)

        for i, (name, tower_type, cost, attack_count) in enumerate(tower_data):
            button_y = self.TOP_BAR_HEIGHT + int(self.SCREEN_HEIGHT * 0.08) + i * (button_height + 10)

            # 선택된 타워 타입과 일치하면 밝은 초록색
            is_selected = (self.selected_tower_type and hasattr(self.selected_tower_type, 'tower_type') and self.selected_tower_type.tower_type == tower_type)
            color = (0, 200, 0) if is_selected else (0, 100, 0)

            button_rect = pygame.Rect(button_x, button_y, button_width, button_height)
            pygame.draw.rect(screen, color, button_rect)

            text_x = button_x + int(self.SIDEBAR_WIDTH * 0.05)
            text_y = button_y + int(button_height * 0.25)
            self._draw_text(screen, name, (text_x, text_y), (255, 255, 255))

    def handle_click(self, pos, game_manager, current_map, towers):
        x, y = pos

        # 나가기 버튼 클릭 처리
        if self.exit_button_rect.collidepoint(x, y):
            return "exit_game"

        # 스킵 버튼 클릭 처리
        if self.skip_button_rect and self.skip_button_rect.collidepoint(x, y):
            return "skip_wave"

        # 타워 버튼 데이터 (사거리 증가: 100→150, 120→180, 140→200)
        tower_data = [
            ("bow", 50, 1, "images/bow.png", 1.0, 150),
            ("cane", 80, 2, "images/cane.png", 0.8, 180),
            ("bomb", 120, 3, "images/bomb.png", 0.6, 200)
        ]

        button_x = self.MAP_AREA_WIDTH + int(self.SIDEBAR_WIDTH * 0.1)
        button_width = int(self.SIDEBAR_WIDTH * 0.8)
        button_height = int(self.SCREEN_HEIGHT * 0.06)

        # 타워 선택 버튼 클릭 검사
        for i, (tower_type, cost, attack_count, image_path, attack_speed, range_val) in enumerate(tower_data):
            button_y = self.TOP_BAR_HEIGHT + int(self.SCREEN_HEIGHT * 0.08) + i * (button_height + 10)
            tower_button_rect = pygame.Rect(button_x, button_y, button_width, button_height)

            if tower_button_rect.collidepoint(x, y):
                self.selected_tower_type = Tower(
                    attack_speed=attack_speed,
                    range=range_val,
                    cost=cost,
                    upgrade=1,
                    position=(0, 0),
                    tower_type=tower_type,
                    image_path=image_path,
                    attack_count=attack_count
                )
                return True

        # 타워 설치 시도 (게임 맵 영역 내)
        if self.selected_tower_type and x < self.MAP_AREA_WIDTH and y > self.TOP_BAR_HEIGHT:

            # 경로 충돌 검사 (갈색 길)
            path_width = int(self.MAP_AREA_WIDTH * 0.12)

            is_on_path = False
            for i in range(len(current_map.path_data) - 1):
                p1 = current_map.path_data[i]
                p2 = current_map.path_data[i + 1]

                if abs(p1[1] - p2[1]) < 10:  # 가로
                    start_x = min(p1[0], p2[0])
                    end_x = max(p1[0], p2[0])
                    rect = pygame.Rect(start_x, p1[1] - path_width // 2, end_x - start_x, path_width)
                    if rect.collidepoint(x, y):
                        is_on_path = True
                        break
                elif abs(p1[0] - p2[0]) < 10:  # 세로
                    start_y = min(p1[1], p2[1])
                    end_y = max(p1[1], p2[1])
                    rect = pygame.Rect(p1[0] - path_width // 2, start_y, path_width, end_y - start_y)
                    if rect.collidepoint(x, y):
                        is_on_path = True
                        break

            if is_on_path:
                self.selected_tower_type = None
                return True

            # 아군 기지 충돌 검사
            base_pos = current_map.get_main_tower_pos()
            base_size = int(self.MAP_AREA_WIDTH * 0.1)

            distance_to_base = ((x - base_pos[0]) ** 2 + (y - base_pos[1]) ** 2) ** 0.5

            if distance_to_base < base_size:
                self.selected_tower_type = None
                return True

            # 타워 겹침 방지 검사
            tower_min_distance = 30

            for tower in towers:
                distance = ((x - tower.position[0]) ** 2 + (y - tower.position[1]) ** 2) ** 0.5
                if distance < tower_min_distance:
                    self.selected_tower_type = None
                    return True

            # 설치 성공
            if game_manager.money >= self.selected_tower_type.cost:
                new_tower = Tower(
                    attack_speed=self.selected_tower_type.attack_speed,
                    range=self.selected_tower_type.range,
                    cost=self.selected_tower_type.cost,
                    upgrade=self.selected_tower_type.upgrade,
                    position=(x, y),
                    tower_type=self.selected_tower_type.tower_type,
                    image_path=self.selected_tower_type.image_path,
                    attack_count=self.selected_tower_type.attack_count
                )

                towers.append(new_tower)
                game_manager.money -= new_tower.cost
                self.selected_tower_type = None
                return True
            else:
                self.selected_tower_type = None
                return True

        return False

    def _draw_text(self, screen, text, position, color):
        text_surface = self.font.render(text, True, color)
        screen.blit(text_surface, position)
