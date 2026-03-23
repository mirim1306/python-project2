import pygame

class MapSelectScreen:
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
        except:
            try:
                self.title_font = pygame.font.SysFont('nanumgothic', int(screen_height * 0.08))
                self.button_font = pygame.font.SysFont('nanumgothic', int(screen_height * 0.04))
            except:
                self.title_font = pygame.font.SysFont('gulim', int(screen_height * 0.08))
                self.button_font = pygame.font.SysFont('gulim', int(screen_height * 0.04))

        # 맵 데이터 (이름, 이미지 경로, 프리뷰 이미지)
        self.maps = [
            {'name': '들판', 'image': 'images/field.png', 'key': 'field'},
            {'name': '사막', 'image': 'images/desert.png', 'key': 'desert'},
            {'name': '설산', 'image': 'images/snow_mountain.png', 'key': 'snow_mountain'}
        ]

        # 맵 프리뷰 이미지 로드
        preview_width = int(screen_width * 0.25)
        preview_height = int(screen_height * 0.3)

        for map_data in self.maps:
            try:
                preview = pygame.image.load(map_data['image']).convert_alpha()
                map_data['preview'] = pygame.transform.scale(preview, (preview_width, preview_height))
            except (pygame.error, FileNotFoundError):
                map_data['preview'] = None

        # 맵 버튼 배치
        self.map_buttons = []
        button_y = int(screen_height * 0.3)
        total_width = len(self.maps) * preview_width + (len(self.maps) - 1) * int(screen_width * 0.05)
        start_x = (screen_width - total_width) // 2

        for i, map_data in enumerate(self.maps):
            button_x = start_x + i * (preview_width + int(screen_width * 0.05))
            button_rect = pygame.Rect(button_x, button_y, preview_width, preview_height)
            self.map_buttons.append(button_rect)

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
        title_text = self.title_font.render("맵 선택", True, (255, 255, 255))
        title_rect = title_text.get_rect(center=(self.screen_width // 2, self.screen_height * 0.15))
        screen.blit(title_text, title_rect)

        # 맵 버튼들
        for i, (map_data, button_rect) in enumerate(zip(self.maps, self.map_buttons)):
            # 프리뷰 이미지 또는 색상 박스
            if map_data['preview']:
                screen.blit(map_data['preview'], button_rect)
            else:
                colors = [(34, 139, 34), (194, 178, 128), (240, 248, 255)]
                pygame.draw.rect(screen, colors[i], button_rect)

            # 테두리
            pygame.draw.rect(screen, (255, 255, 255), button_rect, 3)

            # 맵 이름
            name_text = self.button_font.render(map_data['name'], True, (255, 255, 255))
            name_bg_rect = pygame.Rect(button_rect.x, button_rect.bottom + 10, button_rect.width, 50)
            pygame.draw.rect(screen, (50, 50, 50), name_bg_rect)
            name_rect = name_text.get_rect(center=name_bg_rect.center)
            screen.blit(name_text, name_rect)

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

        # 맵 선택
        for i, button_rect in enumerate(self.map_buttons):
            if button_rect.collidepoint(pos):
                return {'action': 'select_map', 'map': self.maps[i]['key'], 'map_image': self.maps[i]['image']}

        return None
