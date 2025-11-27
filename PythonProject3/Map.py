import pygame

# 화면 분할
TOP_BAR_HEIGHT = 50
SIDEBAR_WIDTH = 200
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
MAP_AREA_WIDTH = SCREEN_WIDTH - SIDEBAR_WIDTH # 600
MAP_AREA_HEIGHT = SCREEN_HEIGHT - TOP_BAR_HEIGHT # 550

class Map:
    def __init__(self, map_image_path, base_image_path, path_data, tower_spots, map_area_width, map_area_height,
                 top_bar_height):
        self.map_image_path = map_image_path
        self.base_image_path = base_image_path
        self.path_data = path_data

        self.MAP_AREA_WIDTH = map_area_width
        self.MAP_AREA_HEIGHT = map_area_height
        self.TOP_BAR_HEIGHT = top_bar_height

        # 아군/적군 기지 위치 (경로 시작/끝 사용)
        self.main_tower_position = path_data[-1]  # 경로 끝 (당근 위치)
        self.cave_tower_position = path_data[0]  # 경로 시작 (적 소환 위치)

        # Pygame 이미지 로드 및 맵 영역 크기에 맞게 스케일링
        try:
            img = pygame.image.load(map_image_path).convert_alpha()
            self.background_image = pygame.transform.scale(img, (self.MAP_AREA_WIDTH, self.MAP_AREA_HEIGHT))
        except pygame.error:
            self.background_image = pygame.Surface((self.MAP_AREA_WIDTH, self.MAP_AREA_HEIGHT))
            self.background_image.fill((34, 139, 34))

        try:
            self.base_image = pygame.image.load(base_image_path).convert_alpha()
            self.base_image = pygame.transform.scale(self.base_image,(int(self.MAP_AREA_WIDTH * 0.08), int(self.MAP_AREA_WIDTH * 0.08)))
        except pygame.error:
            self.base_image = None

    def draw(self, screen):
        # 맵 배경 이미지 그리기
        screen.blit(self.background_image, (0, self.TOP_BAR_HEIGHT))

        # 메인 타워 (아군 기지) 이미지 그리기 (갈색 길 끝에 위치)
        if self.base_image:
            base_rect = self.base_image.get_rect(center=self.main_tower_position)
            screen.blit(self.base_image, base_rect)

    def get_path(self):
        return self.path_data

    def get_cave_tower_pos(self):
        # 적군 소환 지점의 위치(경로의 시작점)를 반환합니다.
        return self.cave_tower_position

    def get_main_tower_pos(self):
        ## 아군 기지(경로의 끝점)의 위치를 반환합니다.
        return self.main_tower_position

    def get_path_area_rects(self):
        path_rects = []
        return path_rects