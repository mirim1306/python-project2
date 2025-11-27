import time
import pygame

class Tower:
    def __init__(self, attack_speed, range, cost, upgrade, position, tower_type, image_path, attack_count=1):
        self.attack_speed = attack_speed
        self.range = range
        self.cost = cost
        self.upgrade = upgrade
        self.position = position
        self.tower_type = tower_type
        self.attack_count = attack_count
        self.last_attack_time = 0.0
        self.image_path = image_path

        try:
            self.image = pygame.image.load(image_path).convert_alpha()
            self.image = pygame.transform.scale(self.image, (30, 30))
        except (pygame.error, FileNotFoundError):
            self.image = None

    def target(self, enemies):
        # 범위 내 가장 먼저 포착된(경로 진행도가 높은) 적들을 찾음
        targets = []

        for enemy in enemies:
            if enemy.is_alive:
                dist = ((self.position[0] - enemy.position[0]) ** 2 +
                        (self.position[1] - enemy.position[1]) ** 2) ** 0.5
                if dist <= self.range:
                    # (경로 인덱스, 거리, 적) 형태로 저장
                    targets.append((enemy.path_index, dist, enemy))

        # 경로 진행도가 높은 순 → 거리 가까운 순으로 정렬
        targets.sort(key=lambda x: (-x[0], x[1]))
        return [enemy for _, _, enemy in targets[:self.attack_count]]

    def attack(self, target_enemies, projectiles):
        # 투사체 발사
        current_time = time.time()
        attack_delay = 1.0 / self.attack_speed
        if current_time - self.last_attack_time < attack_delay:
            return

        if target_enemies:
            from Projectile import Projectile
            for target in target_enemies:
                if target and target.is_alive:
                    projectile = Projectile(self.position, target, speed=15)
                    projectiles.append(projectile)

            self.last_attack_time = current_time

    def draw(self, screen):
        if self.image:
            image_rect = self.image.get_rect(center=self.position)
            screen.blit(self.image, image_rect)
        else:
            colors = {'bow': (255, 0, 0), 'cane': (0, 0, 255), 'bomb': (255, 165, 0)}
            color = colors.get(self.tower_type, (255, 0, 0))
            pygame.draw.circle(screen, color, self.position, 15)