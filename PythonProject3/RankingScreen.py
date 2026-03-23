import pygame

class RankingScreen:
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
            self.title_font = pygame.font.SysFont('malgungothic', int(screen_height * 0.07))
            self.rank_font = pygame.font.SysFont('malgungothic', int(screen_height * 0.03))
            self.button_font = pygame.font.SysFont('malgungothic', int(screen_height * 0.04))
        except:
            try:
                self.title_font = pygame.font.SysFont('nanumgothic', int(screen_height * 0.07))
                self.rank_font = pygame.font.SysFont('nanumgothic', int(screen_height * 0.03))
                self.button_font = pygame.font.SysFont('nanumgothic', int(screen_height * 0.04))
            except:
                self.title_font = pygame.font.SysFont('gulim', int(screen_height * 0.07))
                self.rank_font = pygame.font.SysFont('gulim', int(screen_height * 0.03))
                self.button_font = pygame.font.SysFont('gulim', int(screen_height * 0.04))

        # 뒤로가기 버튼
        back_button_width = int(screen_width * 0.15)
        back_button_height = int(screen_height * 0.08)
        back_button_x = (screen_width - back_button_width) // 2
        back_button_y = int(screen_height * 0.85)
        self.back_button = pygame.Rect(back_button_x, back_button_y, back_button_width, back_button_height)

    def draw(self, screen, user_manager):
        # 배경
        if self.background_image:
            screen.blit(self.background_image, (0, 0))
        else:
            screen.fill((50, 50, 80))

        # 제목
        title_text = self.title_font.render("랭킹", True, (255, 255, 255))
        title_rect = title_text.get_rect(center=(self.screen_width // 2, self.screen_height * 0.1))
        screen.blit(title_text, title_rect)

        # 랭킹 데이터
        rankings = user_manager.get_rankings()

        # 테이블 헤더
        header_y = self.screen_height * 0.2
        header_texts = ["순위", "아이디", "총점", "플레이 횟수", "최고점수"]
        header_positions = [0.15, 0.3, 0.5, 0.65, 0.8]

        for text, pos_x in zip(header_texts, header_positions):
            header_surface = self.rank_font.render(text, True, (255, 255, 0))
            header_rect = header_surface.get_rect(center=(self.screen_width * pos_x, header_y))
            screen.blit(header_surface, header_rect)

        # 랭킹 표시 (상위 10명)
        start_y = self.screen_height * 0.27
        line_height = self.screen_height * 0.05

        for i, rank_data in enumerate(rankings[:10]):
            y_pos = start_y + i * line_height

            # 순위 색상
            if i == 0:
                color = (255, 215, 0)  # 금색
            elif i == 1:
                color = (192, 192, 192)  # 은색
            elif i == 2:
                color = (205, 127, 50)  # 동색
            else:
                color = (255, 255, 255)

            # 현재 사용자 하이라이트
            if user_manager.current_user == rank_data['username']:
                highlight_rect = pygame.Rect(self.screen_width * 0.1, y_pos - 5,
                                             self.screen_width * 0.8, line_height - 5)
                pygame.draw.rect(screen, (50, 50, 150), highlight_rect)

            # 데이터 표시
            rank_texts = [
                f"{i + 1}",
                rank_data['username'],
                f"{rank_data['total_score']:,}",
                f"{rank_data['games_played']}",
                f"{rank_data['best_score']:,}"
            ]

            for text, pos_x in zip(rank_texts, header_positions):
                text_surface = self.rank_font.render(text, True, color)
                text_rect = text_surface.get_rect(center=(self.screen_width * pos_x, y_pos))
                screen.blit(text_surface, text_rect)

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
