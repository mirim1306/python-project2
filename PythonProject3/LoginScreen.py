import pygame

class LoginScreen:
    def __init__(self, screen_width, screen_height):
        self.screen_width = screen_width
        self.screen_height = screen_height

        # 배경 이미지 로드
        try:
            self.background_image = pygame.image.load('images/basic_screen.png').convert()
            self.background_image = pygame.transform.scale(self.background_image, (screen_width, screen_height))
        except (pygame.error, FileNotFoundError):
            self.background_image = None

        # 한글 폰트 설정
        try:
            self.title_font = pygame.font.SysFont('malgungothic', int(screen_height * 0.08))
            self.button_font = pygame.font.SysFont('malgungothic', int(screen_height * 0.04))
            self.input_font = pygame.font.SysFont('malgungothic', int(screen_height * 0.03))
            self.small_font = pygame.font.SysFont('malgungothic', int(screen_height * 0.02))
        except:
            try:
                self.title_font = pygame.font.SysFont('nanumgothic', int(screen_height * 0.08))
                self.button_font = pygame.font.SysFont('nanumgothic', int(screen_height * 0.04))
                self.input_font = pygame.font.SysFont('nanumgothic', int(screen_height * 0.03))
                self.small_font = pygame.font.SysFont('nanumgothic', int(screen_height * 0.02))
            except:
                self.title_font = pygame.font.SysFont('gulim', int(screen_height * 0.08))
                self.button_font = pygame.font.SysFont('gulim', int(screen_height * 0.04))
                self.input_font = pygame.font.SysFont('gulim', int(screen_height * 0.03))
                self.small_font = pygame.font.SysFont('gulim', int(screen_height * 0.02))

        # 입력 필드
        input_width = int(screen_width * 0.3)
        input_height = int(screen_height * 0.06)
        input_x = (screen_width - input_width) // 2

        self.username_input = pygame.Rect(input_x, int(screen_height * 0.35), input_width, input_height)
        self.password_input = pygame.Rect(input_x, int(screen_height * 0.48), input_width, input_height)

        # 버튼
        button_width = int(screen_width * 0.15)
        button_height = int(screen_height * 0.08)
        button_y = int(screen_height * 0.65)

        self.login_button = pygame.Rect(input_x, button_y, button_width, button_height)
        self.register_button = pygame.Rect(input_x + button_width + 20, button_y, button_width, button_height)

        # 뒤로가기 버튼
        back_button_width = int(screen_width * 0.12)
        back_button_height = int(screen_height * 0.06)
        self.back_button = pygame.Rect(int(screen_width * 0.05), int(screen_height * 0.05),
                                       back_button_width, back_button_height)

        # 입력 텍스트
        self.username_text = ""
        self.password_text = ""
        self.active_field = None  # 'username' or 'password'
        self.message = ""
        self.message_color = (255, 255, 255)

    def draw(self, screen):
        # 배경
        if self.background_image:
            screen.blit(self.background_image, (0, 0))
        else:
            screen.fill((50, 50, 80))

        # 제목
        title_text = self.title_font.render("로그인", True, (255, 255, 255))
        title_rect = title_text.get_rect(center=(self.screen_width // 2, self.screen_height * 0.15))
        screen.blit(title_text, title_rect)

        # 아이디 레이블
        username_label = self.input_font.render("아이디:", True, (255, 255, 255))
        screen.blit(username_label, (self.username_input.x, self.username_input.y - 35))

        # 아이디 안내문
        username_guide = self.small_font.render("(영문, 숫자만 가능)", True, (200, 200, 200))
        screen.blit(username_guide, (self.username_input.x, self.username_input.y - 15))

        # 아이디 입력 필드
        color = (100, 150, 255) if self.active_field == 'username' else (200, 200, 200)
        pygame.draw.rect(screen, color, self.username_input)
        pygame.draw.rect(screen, (255, 255, 255), self.username_input, 2)
        username_surface = self.input_font.render(self.username_text, True, (0, 0, 0))
        screen.blit(username_surface, (self.username_input.x + 10, self.username_input.y + 10))

        # 비밀번호 레이블
        password_label = self.input_font.render("비밀번호:", True, (255, 255, 255))
        screen.blit(password_label, (self.password_input.x, self.password_input.y - 35))

        # 비밀번호 안내문
        password_guide = self.small_font.render("(공백 불가)", True, (200, 200, 200))
        screen.blit(password_guide, (self.password_input.x, self.password_input.y - 15))

        # 비밀번호 입력 필드
        color = (100, 150, 255) if self.active_field == 'password' else (200, 200, 200)
        pygame.draw.rect(screen, color, self.password_input)
        pygame.draw.rect(screen, (255, 255, 255), self.password_input, 2)
        password_display = '*' * len(self.password_text)
        password_surface = self.input_font.render(password_display, True, (0, 0, 0))
        screen.blit(password_surface, (self.password_input.x + 10, self.password_input.y + 10))

        # 로그인 버튼
        pygame.draw.rect(screen, (0, 150, 0), self.login_button)
        pygame.draw.rect(screen, (255, 255, 255), self.login_button, 3)
        login_text = self.button_font.render("로그인", True, (255, 255, 255))
        login_rect = login_text.get_rect(center=self.login_button.center)
        screen.blit(login_text, login_rect)

        # 회원가입 버튼
        pygame.draw.rect(screen, (0, 100, 150), self.register_button)
        pygame.draw.rect(screen, (255, 255, 255), self.register_button, 3)
        register_text = self.button_font.render("회원가입", True, (255, 255, 255))
        register_rect = register_text.get_rect(center=self.register_button.center)
        screen.blit(register_text, register_rect)

        # 뒤로가기 버튼
        pygame.draw.rect(screen, (100, 100, 100), self.back_button)
        pygame.draw.rect(screen, (255, 255, 255), self.back_button, 3)
        back_text = self.button_font.render("뒤로가기", True, (255, 255, 255))
        back_rect = back_text.get_rect(center=self.back_button.center)
        screen.blit(back_text, back_rect)

        # 메시지
        if self.message:
            message_surface = self.input_font.render(self.message, True, self.message_color)
            message_rect = message_surface.get_rect(center=(self.screen_width // 2, self.screen_height * 0.78))
            screen.blit(message_surface, message_rect)

    def handle_click(self, pos):
        if self.back_button.collidepoint(pos):
            return {'action': 'back'}
        elif self.username_input.collidepoint(pos):
            self.active_field = 'username'
        elif self.password_input.collidepoint(pos):
            self.active_field = 'password'
        elif self.login_button.collidepoint(pos):
            return {'action': 'login', 'username': self.username_text, 'password': self.password_text}
        elif self.register_button.collidepoint(pos):
            return {'action': 'register', 'username': self.username_text, 'password': self.password_text}
        else:
            self.active_field = None
        return None

    def handle_key(self, event):
        if self.active_field == 'username':
            if event.key == pygame.K_BACKSPACE:
                self.username_text = self.username_text[:-1]
            elif event.key == pygame.K_RETURN:
                self.active_field = 'password'
            elif event.key == pygame.K_SPACE:
                # 공백 무시
                pass
            elif len(self.username_text) < 20:
                # 영문자, 숫자만 허용
                if event.unicode.isalnum():
                    self.username_text += event.unicode
        elif self.active_field == 'password':
            if event.key == pygame.K_BACKSPACE:
                self.password_text = self.password_text[:-1]
            elif event.key == pygame.K_RETURN:
                return {'action': 'login', 'username': self.username_text, 'password': self.password_text}
            elif event.key == pygame.K_SPACE:
                # 공백 무시
                pass
            elif len(self.password_text) < 20:
                self.password_text += event.unicode
        return None

    def set_message(self, message, is_error=False):
        self.message = message
        self.message_color = (255, 0, 0) if is_error else (0, 255, 0)

    def clear_inputs(self):
        self.username_text = ""
        self.password_text = ""
        self.message = ""
        self.active_field = None
