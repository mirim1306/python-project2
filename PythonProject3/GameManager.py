class GameManager:
    MAX_WAVE = 10

    def __init__(self, wave, health, money):
        self.wave = wave
        self.health = health
        self.money = money
        self.is_running = True

    def update(self):
        if self.health <= 0:
            self.game_over()
            return False
        if self.wave > self.MAX_WAVE:
            self.game_clear()
            return False
        return True

    def game_over(self):
        self.health = 0
        self.is_running = False
        print("--- GAME OVER ---")

    def game_clear(self):
        self.is_running = False
        print("--- GAME CLEAR! ---")
