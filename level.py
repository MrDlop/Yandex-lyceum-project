import pygame
from support import import_csv_layout, import_cut_graphics
from settings import tile_size, screen_height, screen_width, FPS
from tiles import Tile, StaticTile, Crate, Coin, Palm
from enemy import Enemy
from player import Player
from decoration import Sky, Water, Clouds



class Level:
    def __init__(self, level_data, surface):
        # general setup
        self.display_surface = surface
        self.world_shift = 0
        self.current_x = None

        # health
        self.health = 10
        self.health_size = 140 // self.health
        self.health_counter_bg = pygame.image.load('graphics/progress_bar/health_bar.png')
        self.health_counter_bg = pygame.transform.scale(self.health_counter_bg, (150, 21))
        self.health_counter_bg_rect = self.health_counter_bg.get_rect(center=(90, 40))
        self.health_counter = pygame.image.load('graphics/progress_bar/Loading_bar.png')
        self.health_counter = pygame.transform.scale(self.health_counter, (self.health_size * self.health, 17))
        self.health_counter_rect = self.health_counter.get_rect(midleft=(20, 39))



        # player
        self.level_data = level_data
        player_layout = import_csv_layout(level_data['player'])
        self.player = pygame.sprite.GroupSingle()
        self.goal = pygame.sprite.GroupSingle()
        self.player_setup(player_layout)

        # dust
        self.dust_sprite = pygame.sprite.GroupSingle()
        self.player_on_ground = False

        # terrain setup
        terrain_layout = import_csv_layout(level_data['terrain'])
        self.terrain_sprites = self.create_tile_group(terrain_layout, 'terrain')

        # grass setup
        grass_layout = import_csv_layout(level_data['grass'])
        self.grass_sprites = self.create_tile_group(grass_layout, 'grass')

        # crates
        crate_layout = import_csv_layout(level_data['crates'])
        self.crate_sprites = self.create_tile_group(crate_layout, 'crates')

        # coins
        self.count_coins = 0
        coin_layout = import_csv_layout(level_data['coins'])
        self.coins_many = len(coin_layout)
        self.coin_sprites = self.create_tile_group(coin_layout, 'coins')
        self.f1 = pygame.font.Font(None, 36)

        # foreground palms
        fg_palm_layout = import_csv_layout(level_data['fg palms'])
        self.fg_palm_sprites = self.create_tile_group(fg_palm_layout, 'fg palms')

        # background palms
        bg_palm_layout = import_csv_layout(level_data['bg palms'])
        self.bg_palm_sprites = self.create_tile_group(bg_palm_layout, 'bg palms')

        # enemy
        enemy_layout = import_csv_layout(level_data['enemies'])
        self.enemy_sprites = self.create_tile_group(enemy_layout, 'enemies')

        # constraint
        constraint_layout = import_csv_layout(level_data['constraints'])
        self.constraint_sprites = self.create_tile_group(constraint_layout, 'constraint')

        # decoration
        self.sky = Sky(8)
        self.level_width = len(terrain_layout[0]) * tile_size
        self.water = Water(screen_height - 20, self.level_width)
        self.clouds = Clouds(400, self.level_width, 30)

    def create_tile_group(self, layout, type):
        sprite_group = pygame.sprite.Group()

        for row_index, row in enumerate(layout):
            for col_index, val in enumerate(row):
                if val != '-1':

                    x = col_index * tile_size
                    y = row_index * tile_size

                    if type == 'terrain':
                        terrain_tile_list = import_cut_graphics('graphics/level/graphics/tiles.png')
                        tile_surface = terrain_tile_list[int(val)]
                        sprite = StaticTile(tile_size, x, y, tile_surface)
                        sprite_group.add(sprite)

                    if type == 'grass':
                        grass_tile_list = import_cut_graphics('graphics/decoration/grass/grass.png')
                        tile_surface = grass_tile_list[int(val)]
                        sprite = StaticTile(tile_size, x, y, tile_surface)
                        sprite_group.add(sprite)

                    if type == 'crates':
                        sprite = Crate(tile_size, x, y)
                        sprite_group.add(sprite)

                    if type == 'coins':
                        if val == '0':
                            sprite = Coin(tile_size, x, y, 'graphics/coins/gold')
                            sprite_group.add(sprite)
                        if val == '1':
                            sprite = Coin(tile_size, x, y, 'graphics/coins/silver')
                            sprite_group.add(sprite)

                    if type == 'fg palms':
                        if val == '0':
                            sprite = Palm(tile_size, x, y, 'graphics/level/graphics/palm_small', 38)
                            sprite_group.add(sprite)
                        if val == '1':
                            sprite = Palm(tile_size, x, y, 'graphics/level/graphics/palm_large', 64)
                            sprite_group.add(sprite)
                    if type == 'bg palms':
                        sprite = Palm(tile_size, x, y, 'graphics/level/graphics/palm_bg', 64)
                        sprite_group.add(sprite)
                    if type == 'enemies':
                        sprite = Enemy(tile_size, x, y)
                        sprite_group.add(sprite)
                    if type == 'constraint':
                        sprite = Tile(tile_size, x, y)
                        sprite_group.add(sprite)

        return sprite_group

    def player_setup(self, layout):
        for row_index, row in enumerate(layout):
            for col_index, val in enumerate(row):
                x = col_index * tile_size
                y = row_index * tile_size
                if val == '0':
                    sprite = Player((x, y), self.display_surface, self.create_jump_particles)
                    self.player.add(sprite)

    def enemy_collision_reverse(self):
        for enemy in self.enemy_sprites.sprites():
            if pygame.sprite.spritecollide(enemy, self.constraint_sprites, False):
                enemy.reverse()

    def create_jump_particles(self, pos):
        if self.player.sprite.facing_right:
            pos -= pygame.math.Vector2(10, 5)
        else:
            pos += pygame.math.Vector2(10, -5)

    def horizontal_movement_collision(self):
        player = self.player.sprite
        player.rect.x += player.direction.x * player.speed
        collidable_sprites = self.terrain_sprites.sprites() + self.crate_sprites.sprites() + self.fg_palm_sprites.sprites()
        for sprite in collidable_sprites:
            if sprite.rect.colliderect(player.rect):
                if player.direction.x < 0:
                    player.rect.left = sprite.rect.right
                    player.on_left = True
                    self.current_x = player.rect.left
                elif player.direction.x > 0:
                    player.rect.right = sprite.rect.left
                    player.on_right = True
                    self.current_x = player.rect.right

        if player.on_left and (player.rect.left < self.current_x or player.direction.x >= 0):
            player.on_left = False
        if player.on_right and (player.rect.right > self.current_x or player.direction.x <= 0):
            player.on_right = False

    def vertical_movement_collision(self):
        player = self.player.sprite
        player.apply_gravity()
        collidable_sprites = self.terrain_sprites.sprites() + self.crate_sprites.sprites() + self.fg_palm_sprites.sprites()

        for sprite in collidable_sprites:
            if sprite.rect.colliderect(player.rect):
                if player.direction.y > 0:
                    player.rect.bottom = sprite.rect.top
                    player.direction.y = 0
                    player.on_ground = True
                elif player.direction.y < 0:
                    player.rect.top = sprite.rect.bottom
                    player.direction.y = 0
                    player.on_ceiling = True

        if player.on_ground and player.direction.y < 0 or player.direction.y > 1:
            player.on_ground = False
        if player.on_ceiling and player.direction.y > 0.1:
            player.on_ceiling = False

    def check_coin_collisions(self):
        collided_coins = pygame.sprite.spritecollide(self.player.sprite, self.coin_sprites, True)
        if collided_coins:
            for coin in collided_coins:
                self.count_coins += 1

    def scroll_x(self):
        player = self.player.sprite
        player_x = player.rect.centerx
        direction_x = player.direction.x

        if player_x < screen_width / 4 and direction_x < 0:
            self.world_shift = 8
            player.speed = 0
        elif player_x > screen_width - (screen_width / 4) and direction_x > 0:
            self.world_shift = -8
            player.speed = 0
        else:
            self.world_shift = 0
            player.speed = 8

    def get_player_on_ground(self):
        if self.player.sprite.on_ground:
            self.player_on_ground = True
        else:
            self.player_on_ground = False

    def create_landing_dust(self):
        if not self.player_on_ground and self.player.sprite.on_ground and not self.dust_sprite.sprites():
            if self.player.sprite.facing_right:
                offset = pygame.math.Vector2(10, 15)
            else:
                offset = pygame.math.Vector2(-10, 15)

    def restart(self):
        self.__init__(self.level_data, self.display_surface)

    def check_death(self):
        if self.player.sprite.rect.top > screen_height:
            self.restart()
        if self.player.sprite.health <= 1 * FPS:
            self.restart()

    def check_enemy_collisions(self):
        enemy_collisions = pygame.sprite.spritecollide(self.player.sprite, self.enemy_sprites, False)

        if enemy_collisions:
            for enemy in enemy_collisions:
                enemy_center = enemy.rect.centery
                enemy_top = enemy.rect.top
                player_bottom = self.player.sprite.rect.bottom
                if enemy_top < player_bottom < enemy_center and self.player.sprite.direction.y >= 0:
                    self.player.sprite.direction.y = -15
                    enemy.kill()
                else:
                    self.player.sprite.direction.y = -10
                    self.player.sprite.get_damage(-10)

    def check_win(self):
        if self.count_coins == self.coins_many * 2:
            return 1

    def run(self):
        # run the entire game / level

        # sky
        self.sky.draw(self.display_surface)
        self.clouds.draw(self.display_surface, self.world_shift)

        # background palms
        self.bg_palm_sprites.update(self.world_shift)
        self.bg_palm_sprites.draw(self.display_surface)

        # terrain
        self.terrain_sprites.update(self.world_shift)
        self.terrain_sprites.draw(self.display_surface)

        # enemy
        self.enemy_sprites.update(self.world_shift)
        self.constraint_sprites.update(self.world_shift)
        self.enemy_collision_reverse()
        self.enemy_sprites.draw(self.display_surface)

        # crate
        self.crate_sprites.update(self.world_shift)
        self.crate_sprites.draw(self.display_surface)

        # grass
        self.grass_sprites.update(self.world_shift)
        self.grass_sprites.draw(self.display_surface)

        # coins
        self.coin_sprites.update(self.world_shift)
        self.coin_sprites.draw(self.display_surface)

        text2 = self.f1.render(str(self.count_coins), 1, pygame.Color('yellow'))
        self.display_surface.blit(text2, (10, 10))

        # health
        if self.health_size * (self.player.sprite.health // FPS) >= 0:
            self.health_counter = pygame.transform.scale(self.health_counter,
                                                     (self.health_size * (self.player.sprite.health // FPS), 17))
            self.display_surface.blit(self.health_counter, self.health_counter_rect)
            self.display_surface.blit(self.health_counter_bg, self.health_counter_bg_rect)


        # foreground palms
        self.fg_palm_sprites.update(self.world_shift)
        self.fg_palm_sprites.draw(self.display_surface)

        # dust particles
        self.dust_sprite.update(self.world_shift)
        self.dust_sprite.draw(self.display_surface)

        # player sprites
        self.player.update()
        self.horizontal_movement_collision()

        self.get_player_on_ground()
        self.vertical_movement_collision()
        self.create_landing_dust()

        self.scroll_x()
        self.player.draw(self.display_surface)
        self.goal.update(self.world_shift)
        self.goal.draw(self.display_surface)

        # water
        self.water.draw(self.display_surface, self.world_shift)

        self.check_win()
        self.check_death()

        self.check_coin_collisions()
        self.check_enemy_collisions()
        return self.check_win()
