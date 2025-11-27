import pygame
import math

class Projectile:
    def __init__(self, start_pos, target_enemy, speed=10):
        self.position = list(start_pos)
        self.target = target_enemy
        self.speed = speed
        self.is_active = True

    def update(self):
        if not self.target or not self.target.is_alive:
            self.is_active = False
            return

        # 목표물 위치
        target_x, target_y = self.target.position
        current_x, current_y = self.position

        # 방향 계산
        dx = target_x - current_x
        dy = target_y - current_y
        distance = math.sqrt(dx ** 2 + dy ** 2)

        # 목표에 도달했으면
        if distance < self.speed:
            self.is_active = False
            return

        # 이동
        if distance > 0:
            ratio = self.speed / distance
            self.position[0] += dx * ratio
            self.position[1] += dy * ratio

    def draw(self, screen):
        if self.is_active:
            pygame.draw.circle(screen, (255, 255, 0),(int(self.position[0]), int(self.position[1])), 3)