import pygame
import constants
import math

class Character():
    def __init__(self, x, y, health, mob_animations, mob_type):
        self.mob_type = mob_type
        self.flip = False
        self.animation_list = mob_animations[mob_type]
        self.frame_index = 0 # index to change sprite states
        self.move_state = 0 # idle = 0, run = 1, ...
        self.update_time = pygame.time.get_ticks() # time since frame updated
        self.health = health
        self.alive = True
        self.money = 0


        # image stuff :)
        self.image = self.animation_list[self.move_state][self.frame_index]
        self.rect = pygame.Rect(0, 0, constants.TILE_SIZE, constants.TILE_SIZE) # makes player same size as tile
        self.rect.center = (x, y)


    def move(self, dx, dy):
        screen_scroll = [0, 0]

        # makes it so player does not move twice as fast in diagonal
        if dx != 0 and dy != 0:
            dx = dx * math.sqrt(2)/2
            dy = dy * math.sqrt(2)/2

        # faces the player where the cursor is
        pos = pygame.mouse.get_pos()
        x_dist = pos[0] - self.rect.centerx

        if x_dist > 0:
            self.flip = False
        if x_dist < 0:
            self.flip = True

        # updates player pos
        self.rect.x += dx
        self.rect.y += dy

        if dx == 0 and dy == 0:
            self.move_state = 0
        else:
            self.move_state = 1

        # screen only scrolls around player
        if self.mob_type == 0:
            # moves camera left/right
            if self.rect.right > (constants.SCREEN_WIDTH - constants.SCROLL_THRESH):
                screen_scroll[0] = (constants.SCREEN_WIDTH - constants.SCROLL_THRESH) - self.rect.right
            if self.rect.left < constants.SCROLL_THRESH:
                screen_scroll[0] = constants.SCROLL_THRESH - self.rect.left

        return screen_scroll

    def update(self):

        if self.health <= 0: #see if your dead
            self.health = 0
            self.alive = False


        # sets current character frame state -- idle version
        self.image = self.animation_list[self.move_state][self.frame_index]

        # check if enough time passed since last update
        if pygame.time.get_ticks() - self.update_time > constants.ANIMATION_COOLDOWN:
            self.frame_index += 1
            self.update_time = pygame.time.get_ticks()

        # addresses out of bounds error
        if self.frame_index >= len(self.animation_list[self.move_state]):
            self.frame_index = 0

    def draw(self, surface):
        flipped_image = pygame.transform.flip(self.image, self.flip, False)

        if self.mob_type == 0:
            surface.blit(flipped_image, (self.rect.x, self.rect.y - constants.PLAYER_SCALE * constants.OFFSET))
        else:
            if self.alive:
                surface.blit(flipped_image, self.rect)
                pygame.draw.rect(surface, constants.RED, self.rect, 1)
