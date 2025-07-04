from Enemies import *


class Wave:
    def __init__(self, number, spawn_loc):
        self.number = number

        # 👇 웨이브 5, 10는 특별하게 더 많은 적 등장
        
        if number == 5:
            self.enemies = 25
        
        if number == 10:
            self.enemies = 40
        else:
            self.enemies = 2 * number + 3
        
        
        self.delay = int(120/number)
        self.current_time = 0
        self.time_until_next_spawn = 0
        self.spawn_loc = spawn_loc

    def update(self, enemies):
        if self.time_until_next_spawn <= 0 and self.enemies >= 1:
            self.time_until_next_spawn = self.delay
            enemy = createEnemy(self.spawn_loc)
            enemies.add(enemy)
            self.enemies -= 1
        else:
            self.time_until_next_spawn -= 1


class WaveHandler:
    def __init__(self, spawn_loc, start_wave=0):
        self.spawn_loc = spawn_loc
        self.current_wave_number = start_wave
        self.current_wave = None
        self.in_wave = False

    def start_wave(self):
        self.in_wave = True
        self.current_wave_number += 1
        self.current_wave = Wave(self.current_wave_number, self.spawn_loc)

    def update(self, enemies, game):
        
        if self.in_wave:
            self.current_wave.update(enemies)

        if self.current_wave_number == 5 and not hasattr(self, 'special_shown'):
            game.special_wave_message = "!!성무의식!!"
            game.special_wave_timer = 180  # ✅ 여기!
            self.special_shown = True  # 한 번만 실행되도록 표시
    # ✅ 10웨이브일 때 딱 한 번만 메시지 보여주기
        if self.current_wave_number == 10 and not hasattr(self, 'special_shown'):
            game.special_wave_message = "!!무용구보!!"
            game.special_wave_timer = 180  # ✅ 여기!
            self.special_shown = True  # 한 번만 실행되도록 표시