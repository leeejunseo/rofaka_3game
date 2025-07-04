from Lib import *
from Effects import *
from Lib import *
from Effects import *


def createTower(pos, tower_choice, tower_models, path, towers):
    if not path.contains(pos):
        for tower in towers.sprites():
            if tower.rect.collidepoint(pos):
                return None

        model = tower_models[tower_choice]
        if model.name == "Fire Tower":
            return FireTower(pos, model)
        elif model.name == "Ice Tower":
            return IceTower(pos, model)
        else:
            return Tower(pos, model)
    return None


class TowerModel:
    def __init__(self, name, damage, fire_rate, range, value, fire_colour, sprite_location, description):
        self.name = name
        self.damage = damage
        self.fire_rate = fire_rate
        self.range = range
        self.value = value
        self.fire_colour = fire_colour
        self.sprite_location = sprite_location
        self.description = description


class Tower(pygame.sprite.Sprite):
    def __init__(self, pos, model):
        pygame.sprite.Sprite.__init__(self)
        self.model = model
        self.image = pygame.image.load(model.sprite_location)
        self.rect = self.image.get_rect()
        self.rect.center = pos
        self.last_fired = 0;

    def update(self, enemies, effects, screen):
        if self.last_fired <= self.model.fire_rate:
            self.last_fired += self.game_speed

        else:
            # Look for target to fire at
            target = None
            for sprite in enemies.sprites():
                if not sprite.is_dead:
                    distance = getDistance(self.rect.center, sprite.rect.center)
                    if distance <= self.model.range * GRID_SIZE + 1:
                        if target is None or sprite.distance_travelled > target.distance_travelled:
                            target = sprite
            if target is not None:
                # FIRE ZE MISSILEZZ!
                target.health -= self.model.damage
                effects.add(ShootEffect(self.model.fire_colour, target.rect.center, self.rect.center, 2, screen.get_size()))
                if target.health <= 0:
                    target.is_dead = True
                    pygame.event.post(pygame.event.Event(ENEMY_KILLED, enemy=target))
                self.last_fired = 0

class TowerModel:
    def __init__(self, name, damage, fire_rate, range, value, fire_colour, sprite_location, description):
        self.name = name
        self.damage = damage
        self.fire_rate = fire_rate
        self.range = range
        self.value = value
        self.fire_colour = fire_colour
        self.sprite_location = sprite_location
        self.description = description



class Tower(pygame.sprite.Sprite):
    def __init__(self, pos, model):
        pygame.sprite.Sprite.__init__(self)
        self.model = model
        self.image = pygame.image.load(model.sprite_location)
        self.rect = self.image.get_rect()
        self.rect.center = pos
        self.last_fired = 0;

    def update(self, enemies, effects, screen):
        if self.last_fired <= self.model.fire_rate:
            self.last_fired += 1
        else:
            # Look for target to fire at
            target = None
            for sprite in enemies.sprites():
                if not sprite.is_dead:
                    distance = getDistance(self.rect.center, sprite.rect.center)
                    if distance <= self.model.range * GRID_SIZE + 1:
                        if target is None or sprite.distance_travelled > target.distance_travelled:
                            target = sprite
            if target is not None:
                # FIRE ZE MISSILEZZ!
                target.health -= self.model.damage
                effects.add(ShootEffect(self.model.fire_colour, target.rect.center, self.rect.center, 2, screen.get_size()))
                if target.health <= 0:
                    target.is_dead = True
                    pygame.event.post(pygame.event.Event(ENEMY_KILLED, enemy=target))
                self.last_fired = 0

class FireTower(Tower):
    def __init__(self, pos, model):
        super().__init__(pos, model)

    def update(self, enemies, effects, screen):
        if self.last_fired <= self.model.fire_rate:
            self.last_fired += 1
        else:
            target = None
            for sprite in enemies.sprites():
                if not sprite.is_dead:
                    distance = getDistance(self.rect.center, sprite.rect.center)
                    if distance <= self.model.range * GRID_SIZE + 1:
                        target = sprite
                        break

            if target:
                splash_radius = 50  # 픽셀 기준
                for other in enemies:
                    if not other.is_dead:
                        d = getDistance(target.rect.center, other.rect.center)
                        if d <= splash_radius:
                            other.health -= self.model.damage
                            effects.add(ShootEffect(self.model.fire_colour, other.rect.center, self.rect.center, 2, screen.get_size()))
                            if other.health <= 0:
                                other.is_dead = True
                                pygame.event.post(pygame.event.Event(ENEMY_KILLED, enemy=other))

                self.last_fired = 0

class IceTower(Tower):
    def __init__(self, pos, model):
        super().__init__(pos, model)

    def update(self, enemies, effects, screen):
        if self.last_fired <= self.model.fire_rate:
            self.last_fired += 1
        else:
            for sprite in enemies.sprites():
                if not sprite.is_dead:
                    distance = getDistance(self.rect.center, sprite.rect.center)
                    if distance <= self.model.range * GRID_SIZE + 1:
                        sprite.health -= self.model.damage
                        sprite.apply_slow(3, 0.5)  # 3초간 50% 슬로우
                        effects.add(ShootEffect(self.model.fire_colour, sprite.rect.center, self.rect.center, 2, screen.get_size()))
                        if sprite.health <= 0:
                            sprite.is_dead = True
                            pygame.event.post(pygame.event.Event(ENEMY_KILLED, enemy=sprite))
                        self.last_fired = 0
                        break


def createTower(pos, tower_choice, tower_models, path, towers):
    if not path.contains(pos):
        for tower in towers.sprites():
            if tower.rect.collidepoint(pos):
                return None

        model = tower_models[tower_choice]
        if model.name == "Fire Tower":
            return FireTower(pos, model)
        elif model.name == "Ice Tower":
            return IceTower(pos, model)
        else:
            return Tower(pos, model)
    return None