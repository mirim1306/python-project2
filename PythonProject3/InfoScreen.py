import pygame

class InfoScreen:
    def __init__(self, screen_width, screen_height):
        self.screen_width = screen_width
        self.screen_height = screen_height

        # 한글 폰트 설정
        try:
            self.title_font = pygame.font.SysFont('malgungothic', int(screen_height * 0.06))
            self.text_font = pygame.font.SysFont('malgungothic', int(screen_height * 0.025))
            self.button_font = pygame.font.SysFont('malgungothic', int(screen_height * 0.04))
        except:
            try:
                self.title_font = pygame.font.SysFont('nanumgothic', int(screen_height * 0.06))
                self.text_font = pygame.font.SysFont('nanumgothic', int(screen_height * 0.025))
                self.button_font = pygame.font.SysFont('nanumgothic', int(screen_height * 0.04))
            except:
                self.title_font = pygame.font.SysFont('gulim', int(screen_height * 0.06))
                self.text_font = pygame.font.SysFont('gulim', int(screen_height * 0.025))
                self.button_font = pygame.font.SysFont('gulim', int(screen_height * 0.04))

        # 뒤로가기 버튼
        button_width = int(screen_width * 0.2)
        button_height = int(screen_height * 0.08)
        button_x = (screen_width - button_width) // 2
        button_y = int(screen_height * 0.85)
        self.back_button = pygame.Rect(button_x, button_y, button_width, button_height)

    def draw(self, screen):
        # 배경
        screen.fill((50, 50, 50))

        # 제목
        title_text = self.title_font.render("게임 설명", True, (255, 255, 0))
        title_rect = title_text.get_rect(center=(self.screen_width // 2, self.screen_height * 0.08))
        screen.blit(title_text, title_rect)

        # 설명 텍스트
        info_lines = [
            "목표: 10개의 웨이브를 막아내고 당근 기지를 지키세요!",
            "",
            "타워 종류",
            "  • 활 토깽이 (50당근): 단일 공격, 사거리 150",
            "  • 워드 토깽이 (80당근): 2명 동시 공격, 사거리 180",
            "  • 폭탄 토깽이 (120당근): 3명 동시 공격, 사거리 200",
            "",
            "슬라임 종류 (빨강→주황→노랑→초록→파랑→남색→보라)",
            "  • 웨이브가 올라갈수록 강한 슬라임 등장",
            "  • 큰 슬라임은 죽으면 2마리의 작은 슬라임으로 분열!",
            "",
            "팁",
            "  • 경로 위나 당근 기지 위에는 타워 설치 불가",
            "  • 웨이브 사이 점검 시간에 타워 배치 전략 세우기",
            "  • 스킵 버튼으로 다음 웨이브 빨리 시작 가능"
        ]

        y_offset = self.screen_height * 0.18
        line_height = self.screen_height * 0.04

        for line in info_lines:
            text = self.text_font.render(line, True, (255, 255, 255))
            text_rect = text.get_rect(center=(self.screen_width // 2, y_offset))
            screen.blit(text, text_rect)
            y_offset += line_height

        # 뒤로가기 버튼
        pygame.draw.rect(screen, (0, 100, 150), self.back_button)
        pygame.draw.rect(screen, (255, 255, 255), self.back_button, 3)
        back_text = self.button_font.render("돌아가기", True, (255, 255, 255))
        back_rect = back_text.get_rect(center=self.back_button.center)
        screen.blit(back_text, back_rect)

    def handle_click(self, pos):
        if self.back_button.collidepoint(pos):
            return "back"
        return None