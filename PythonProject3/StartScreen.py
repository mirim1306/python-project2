import pygame

class StartScreen:
    def __init__(self, screen_width, screen_height):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.is_active = True

        # 배경 이미지 로드
        try:
            self.background_image = pygame.image.load('images/start_screen.png').convert()
            self.background_image = pygame.transform.scale(self.background_image, (screen_width, screen_height))
        except (pygame.error, FileNotFoundError):
            self.background_image = None

        # 한글 폰트 설정
        try:
            self.title_font = pygame.font.SysFont('malgungothic', int(screen_height * 0.1))
            self.button_font = pygame.font.SysFont('malgungothic', int(screen_height * 0.05))
            self.info_font = pygame.font.SysFont('malgungothic', int(screen_height * 0.03))
        except:
            try:
                self.title_font = pygame.font.SysFont('nanumgothic', int(screen_height * 0.1))
                self.button_font = pygame.font.SysFont('nanumgothic', int(screen_height * 0.05))
                self.info_font = pygame.font.SysFont('nanumgothic', int(screen_height * 0.03))
            except:
                self.title_font = pygame.font.SysFont('gulim', int(screen_height * 0.1))
                self.button_font = pygame.font.SysFont('gulim', int(screen_height * 0.05))
                self.info_font = pygame.font.SysFont('gulim', int(screen_height * 0.03))

        # 시작 버튼
        button_width = int(screen_width * 0.3)
        button_height = int(screen_height * 0.1)
        button_x = (screen_width - button_width) // 2
        button_y = int(screen_height * 0.45)

        self.start_button = pygame.Rect(button_x, button_y, button_width, button_height)

        # 설명 버튼
        info_button_y = int(screen_height * 0.58)
        self.info_button = pygame.Rect(button_x, info_button_y, button_width, button_height)

        # 랭킹 버튼
        ranking_button_y = int(screen_height * 0.71)
        self.ranking_button = pygame.Rect(button_x, ranking_button_y, button_width, button_height)

        # 종료 버튼
        quit_button_y = int(screen_height * 0.84)
        self.quit_button = pygame.Rect(button_x, quit_button_y, button_width, button_height)

        # 로그인/로그아웃 버튼 (우측 상단)
        auth_button_width = int(screen_width * 0.12)
        auth_button_height = int(screen_height * 0.06)
        self.auth_button = pygame.Rect(
            screen_width - auth_button_width - 20,
            20,
            auth_button_width,
            auth_button_height
        )

    def draw(self, screen, current_user=None):
        # 배경 이미지 그리기
        if self.background_image:
            screen.blit(self.background_image, (0, 0))
        else:
            screen.fill((34, 139, 34))  # 이미지 로드 실패시 초록색 배경

        # 시작 버튼
        pygame.draw.rect(screen, (0, 150, 0), self.start_button)
        pygame.draw.rect(screen, (255, 255, 255), self.start_button, 3)
        start_text = self.button_font.render("게임 시작", True, (255, 255, 255))
        start_rect = start_text.get_rect(center=self.start_button.center)
        screen.blit(start_text, start_rect)

        # 설명 버튼
        pygame.draw.rect(screen, (100, 100, 150), self.info_button)
        pygame.draw.rect(screen, (255, 255, 255), self.info_button, 3)
        info_text = self.button_font.render("게임 설명", True, (255, 255, 255))
        info_rect = info_text.get_rect(center=self.info_button.center)
        screen.blit(info_text, info_rect)

        # 랭킹 버튼
        pygame.draw.rect(screen, (200, 150, 0), self.ranking_button)
        pygame.draw.rect(screen, (255, 255, 255), self.ranking_button, 3)
        ranking_text = self.button_font.render("랭킹", True, (255, 255, 255))
        ranking_rect = ranking_text.get_rect(center=self.ranking_button.center)
        screen.blit(ranking_text, ranking_rect)

        # 종료 버튼
        pygame.draw.rect(screen, (150, 0, 0), self.quit_button)
        pygame.draw.rect(screen, (255, 255, 255), self.quit_button, 3)
        quit_text = self.button_font.render("게임 종료", True, (255, 255, 255))
        quit_rect = quit_text.get_rect(center=self.quit_button.center)
        screen.blit(quit_text, quit_rect)

        # 로그인/로그아웃 버튼
        if current_user:
            button_color = (100, 100, 100)
            button_text = "로그아웃"
        else:
            button_color = (0, 100, 200)
            button_text = "로그인"

        pygame.draw.rect(screen, button_color, self.auth_button)
        pygame.draw.rect(screen, (255, 255, 255), self.auth_button, 3)
        auth_text = self.info_font.render(button_text, True, (255, 255, 255))
        auth_rect = auth_text.get_rect(center=self.auth_button.center)
        screen.blit(auth_text, auth_rect)

    def handle_click(self, pos, current_user=None):
        if self.start_button.collidepoint(pos):
            return "start"
        elif self.info_button.collidepoint(pos):
            return "info"
        elif self.ranking_button.collidepoint(pos):
            return "ranking"
        elif self.quit_button.collidepoint(pos):
            return "quit"
        elif self.auth_button.collidepoint(pos):
            if current_user:
                return "logout"
            else:
                return "login"
        return None