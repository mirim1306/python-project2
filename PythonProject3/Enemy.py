import pygame

class Enemy:
    BASE_DAMAGE = 1

    def __init__(self, speed, money, position, path_data, enemy_type, image_path):
        self.speed = speed
        self.money = money
        self.is_alive = True
        self.has_attacked = False
        self.path_data = path_data
        self.path_index = 0
        self.position = list(position)
        self.enemy_type = enemy_type

        # 이미지 로드
        try:
            self.image = pygame.image.load(image_path).convert_alpha()
            self.image = pygame.transform.scale(self.image, (20, 20))
        except (pygame.error, FileNotFoundError):
            self.image = None

    def move(self, game_manager):
        if not self.is_alive or self.has_attacked:
            return False

        if self.path_index >= len(self.path_data):
            self.attack_base(game_manager)
            return False

        target_x, target_y = self.path_data[self.path_index]
        current_x, current_y = self.position

        # 이동 로직
        dx = target_x - current_x
        dy = target_y - current_y
        distance = (dx ** 2 + dy ** 2) ** 0.5

        # 거리가 매우 가까우면(1픽셀 이하) 다음 지점으로
        if distance < 1:
            self.path_index += 1
            return True

        if distance <= self.speed:
            self.position = [target_x, target_y]
            self.path_index += 1
        else:
            ratio = self.speed / distance
            self.position[0] += dx * ratio
            self.position[1] += dy * ratio

        return True

    def attack_base(self, game_manager):
        # 기지 공격 - 분열 없이 그냥 사라짐
        if not self.has_attacked:
            game_manager.health -= self.BASE_DAMAGE
            self.has_attacked = True
            self.is_alive = False

    def take_damage(self, game_manager, enemies_list):
        # 데미지를 받아 사망 - 분열 가능
        if self.is_alive:
            self.is_alive = False
            self.die(game_manager, enemies_list)

    def die(self, game_manager, enemies_list):
        # 사망 처리 - 보상 지급 및 분열
        game_manager.money += self.money

        # 분열 로직 (보상도 절반)
        split_data = {
            'purple': ('navy', 'images/navy_slime.png', 30),
            'navy': ('blue', 'images/blue_slime.png', 25),
            'blue': ('green', 'images/green_slime.png', 20),
            'green': ('yellow', 'images/yellow_slime.png', 15),
            'yellow': ('orange', 'images/orange_slime.png', 10),
            'orange': ('red', 'images/red_slime.png', 5),
            'red': None
        }

        split_info = split_data.get(self.enemy_type)

        if split_info:
            new_type, new_image, new_money = split_info
            # 죽은 위치에서 2마리 생성
            for i in range(2):
                new_enemy = Enemy(
                    speed=self.speed * 1.2,
                    money=new_money,
                    position=self.position.copy(),
                    path_data=self.path_data,
                    enemy_type=new_type,
                    image_path=new_image
                )
                new_enemy.path_index = self.path_index
                enemies_list.append(new_enemy)

    def draw(self, screen):
        if self.image:
            image_rect = self.image.get_rect(center=(int(self.position[0]), int(self.position[1])))
            screen.blit(self.image, image_rect)
        else:
            colors = {
                'red': (255, 0, 0),
                'orange': (255, 165, 0),
                'yellow': (255, 255, 0),
                'green': (0, 255, 0),
                'blue': (0, 0, 255),
                'navy': (0, 0, 128),
                'purple': (128, 0, 128)
            }
            color = colors.get(self.enemy_type, (0, 0, 255))
            rect = pygame.Rect(self.position[0] - 5, self.position[1] - 5, 10, 10)
            pygame.draw.rect(screen, color, rect)