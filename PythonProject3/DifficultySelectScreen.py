import pygame

class DifficultySelectScreen:
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
            self.button_font = pygame.font.SysFont('malgungothic', int(screen_height * 0.05))
            self.desc_font = pygame.font.SysFont('malgungothic', int(screen_height * 0.03))
        except:
            try:
                self.title_font = pygame.font.SysFont('nanumgothic', int(screen_height * 0.08))
                self.button_font = pygame.font.SysFont('nanumgothic', int(screen_height * 0.05))
                self.desc_font = pygame.font.SysFont('nanumgothic', int(screen_height * 0.03))
            except:
                self.title_font = pygame.font.SysFont('gulim', int(screen_height * 0.08))
                self.button_font = pygame.font.SysFont('gulim', int(screen_height * 0.05))
                self.desc_font = pygame.font.SysFont('gulim', int(screen_height * 0.03))

        # 난이도 데이터
        self.difficulties = [
            {'name': '쉬움', 'key': 'easy', 'desc': '초보자에게 적합', 'color': (0, 200, 0)},
            {'name': '보통', 'key': 'normal', 'desc': '적당한 도전', 'color': (200, 200, 0)},
            {'name': '어려움', 'key': 'hard', 'desc': '숙련자를 위한 난이도', 'color': (200, 0, 0)}
        ]

        # 난이도 버튼 배치
        button_width = int(screen_width * 0.3)
        button_height = int(screen_height * 0.12)
        button_x = (screen_width - button_width) // 2
        start_y = int(screen_height * 0.3)
        spacing = int(screen_height * 0.05)

        self.difficulty_buttons = []
        for i in range(len(self.difficulties)):
            button_y = start_y + i * (button_height + spacing)
            self.difficulty_buttons.append(pygame.Rect(button_x, button_y, button_width, button_height))

        # 뒤로가기 버튼
        back_button_width = int(screen_width * 0.15)
        back_button_height = int(screen_height * 0.08)
        back_button_x = int(screen_width * 0.05)
        back_button_y = int(screen_height * 0.05)
        self.back_button = pygame.Rect(back_button_x, back_button_y, back_button_width, back_button_height)

    def draw(self, screen):
        # 배경
        if self.background_image:
            screen.blit(self.background_image, (0, 0))
        else:
            screen.fill((100, 100, 150))

        # 제목
        title_text = self.title_font.render("난이도 선택", True, (255, 255, 255))
        title_rect = title_text.get_rect(center=(self.screen_width // 2, self.screen_height * 0.15))
        screen.blit(title_text, title_rect)

        # 난이도 버튼들
        for i, (difficulty, button_rect) in enumerate(zip(self.difficulties, self.difficulty_buttons)):
            # 버튼 배경
            pygame.draw.rect(screen, difficulty['color'], button_rect)
            pygame.draw.rect(screen, (255, 255, 255), button_rect, 3)

            # 난이도 이름
            name_text = self.button_font.render(difficulty['name'], True, (255, 255, 255))
            name_rect = name_text.get_rect(center=(button_rect.centerx, button_rect.centery - 15))
            screen.blit(name_text, name_rect)

            # 설명
            desc_text = self.desc_font.render(difficulty['desc'], True, (255, 255, 255))
            desc_rect = desc_text.get_rect(center=(button_rect.centerx, button_rect.centery + 20))
            screen.blit(desc_text, desc_rect)

        # 뒤로가기 버튼
        pygame.draw.rect(screen, (100, 100, 100), self.back_button)
        pygame.draw.rect(screen, (255, 255, 255), self.back_button, 3)
        back_text = self.button_font.render("뒤로가기", True, (255, 255, 255))
        back_rect = back_text.get_rect(center=self.back_button.center)
        screen.blit(back_text, back_rect)

    def handle_click(self, pos):
        # 뒤로가기 버튼
        if self.back_button.collidepoint(pos):
            return {'action': 'back'}

        # 난이도 선택
        for i, button_rect in enumerate(self.difficulty_buttons):
            if button_rect.collidepoint(pos):
                return {'action': 'select_difficulty', 'difficulty': self.difficulties[i]['key']}

        return None