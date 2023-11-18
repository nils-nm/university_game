import arcade as ar
import arcade.gui
import math
import mouse
from arcade.experimental import Shadertoy
from pathlib import Path
from typing import Optional
from arcade.pymunk_physics_engine import PymunkPhysicsEngine

#const
sc_w = 800
sc_h = 600
sc_title = 'test'

#const for scale
charecter_scal = 1.5
enemy_scal = 1
tile_scal = 0.5
tilemap_scal = 1
ammo_scal = 0.3

fps = 7

#consts used for track if the player is facing
#DOWN_FACING = 0
#LEFT_DOWN_FACING = 1
LEFT_FACING = 1
#LEFT_UP_FACING = 3
#UP_FACING = 4
#RIGHT_UP_FACING = 5
RIGHT_FACING = 0
#RIGHT_DOWN_FACING = 7

#movment speed per frame
player_sp = 3
PLAYER_MOVE_FORCE = 4000
BULLET_MOVE_FORCE = 2500

PLAYING_FIELD_WIDTH = 1600
PLAYING_FIELD_HEIGHT = 1600

#angle mouse
angle = 0


def load_texture_pair(filename):
    return [
            ar.load_texture(filename),
            ar.load_texture(filename, flipped_horizontally=True)
            ]


class Enemy(ar.Sprite):

    def __init__(self):

        #set up parent class
        super().__init__()

        #defoult face direction
        self.enemy_face_direction = RIGHT_FACING


        self.scale = enemy_scal
        self.cur_texture = 0

        #main path for images
        main_path = 'ref/'
        self.idle_texture_pair = load_texture_pair(f'{main_path}enemy/idle.png')

        self.texture = self.idle_texture_pair[0]

        self.hit_box = self.texture.hit_box_points

class PlayerCharecter(ar.Sprite):

    def __init__(self):

        #set up parent class
        super().__init__()

        #defoult face direction
        self.charecter_face_direction = RIGHT_FACING

        #used for flipping between image sequens
        self.cur_texture = 0
        self.scale = charecter_scal

        #main path for images
        main_path = 'ref/'

        #load textures
        self.idle_texture_pair = load_texture_pair(f'{main_path}charecter/idle.png') # idle

        self.walk_texture = {'up': [],
                            'right-up': [],
                            'right': [],
                            'right-down': [],
                            'down': []}
        for i in range(8): # walk left/right
            texture = load_texture_pair(f'{main_path}walk/up{i}.png')
            self.walk_texture['up'].append(texture)
        for i in range(8): # walk left/right
            texture = load_texture_pair(f'{main_path}walk/right-up{i}.png')
            self.walk_texture['right-up'].append(texture)
        for i in range(8): # walk left/right
            texture = load_texture_pair(f'{main_path}walk/right{i}.png')
            self.walk_texture['right'].append(texture)
        for i in range(8): # walk left/right
            texture = load_texture_pair(f'{main_path}walk/right-down{i}.png')
            self.walk_texture['right-down'].append(texture)
        for i in range(8): # walk left/right
            texture = load_texture_pair(f'{main_path}walk/down{i}.png')
            self.walk_texture['down'].append(texture)

        #set the initial texture
        self.texture = self.idle_texture_pair[0]

        #hit box
        self.hit_box = self.texture.hit_box_points

    def update_animations(self, delta_time: float = 1/60):

        #change face direction if press wasd

        """
        if self.change_x < 0 and self.charecter_face_direction == RIGHT_FACING:
            self.charecter_face_direction = LEFT_FACING
        elif self.change_x > 0 and self.charecter_face_direction == LEFT_FACING:
            self.charecter_face_direction = RIGHT_FACING

        """

        #change face direction if mose motion


        if -15 < angle < 15:
            self.charecter_face_direction = ['right', LEFT_FACING]
        elif -165 > angle > -180 or 180 > angle > 165:
            self.charecter_face_direction = ['right', RIGHT_FACING]
        elif -15 > angle > -75:
            self.charecter_face_direction = ['right-up', LEFT_FACING]
        elif -75 > angle > -105:
            self.charecter_face_direction = ['up', RIGHT_FACING]
        elif -105 > angle > -165:
            self.charecter_face_direction = ['right-up', RIGHT_FACING]
        elif -165 > angle > -180 or 180 > angle > 165:
            self.charecter_face_direction = ['right', RIGHT_FACING]
        elif 165 > angle > 105:
            self.charecter_face_direction = ['right-down', RIGHT_FACING]
        elif 105 > angle > 75:
            self.charecter_face_direction = ['down', RIGHT_FACING]
        elif 75 > angle > 15:
            self.charecter_face_direction = ['right-down', LEFT_FACING]

        #idle animation
        if self.change_x == 0 and self.change_y == 0:
            self.texture = self.idle_texture_pair[self.charecter_face_direction[1]]
            return

        #walk animation
        self.cur_texture += 1
        if self.cur_texture > 7*fps:
            self.cur_texture = 0
        self.texture = self.walk_texture[self.charecter_face_direction[0]][self.cur_texture//fps][self.charecter_face_direction[1]]


class MainMenuView(ar.View):

    def on_show_view(self):
        ar.set_background_color(ar.color.ARSENIC)

        ar.set_viewport(0, self.window.width, 0, self.window.height)

        #creating the gui manager
        self.uimanager = ar.gui.UIManager()
        self.uimanager.enable()

        #create box for menu buttons
        self.v_box = ar.gui.UIBoxLayout()

        #create start and quit and settings button
        start_button = ar.gui.UIFlatButton(text='start game', width=200)
        self.v_box.add(start_button.with_space_around(bottom=20))

        settings_button = ar.gui.UIFlatButton(text='settings', width=200)
        self.v_box.add(settings_button.with_space_around(bottom=20))

        quit_button = ar.gui.UIFlatButton(text='quit', width=200)
        self.v_box.add(quit_button)

        #func for button
        start_button.on_click = self.button_start
        settings_button.on_click = self.button_settings
        quit_button.on_click = self.button_quit

        #adding button in  the our manager
        self.uimanager.add(
                ar.gui.UIAnchorWidget(
                    anchor_x='center_x',
                    anchor_y='center_y',
                    child=self.v_box)
                )


    def button_start(self, e):
        game_view = GameView()
        self.uimanager.clear()
        self.window.show_view(game_view)
        game_view.setup()

    def button_settings(self, e):
        print('settings')

    def button_quit(self, e):
        ar.exit()


    def on_draw(self):

        #draw this view
        self.clear()

        ar.start_render()

        ar.draw_text('Main menu', self.window.width/2, self.window.height/2+150,
                     ar.color.WHITE,font_size=50, anchor_x='center')

        #ar.draw_text('click for avance', self.window.width/2, self.window.height/2-75,
        #             ar.color.WHITE, font_size=50, anchor_x='center')

        self.uimanager.draw()



class GameView(ar.View):
    def __init__(self):

        #call the parent class and set up the window
        super().__init__()

        #our scene obj
        self.scene = None
        self.scene_map = None

        #our phisics engine
        #self.physics_engine = None
        self.physics_engine: Optional[PymunkPhysicsEngine] = None

        #track the current state of key
        self.w_p = False
        self.a_p = False
        self.s_p = False
        self.d_p = False

        #offset
        self.offset_x = None
        self.offset_y = None

        #cords mouse
        self.mouse_x = 0
        self.mouse_y = 0

        #our tilemap object
        self.tile_map = None

        #the shadertoy and chanels
        self.shadertoy = None
        self.channel0 = None
        self.channel1 = None
        self.load_shader()

        #separete variable that holds the playre sprite
        self.player_sprite = None
        self.test_sprite = None # =====TEST=====
        self.enemy_sprite = None # ===TEST=ENEMY===

        self.angle = 0

        #our cords mouse
        self.mouse_x = 0
        self.mouse_y = 0

        # A Camera that can be used for scrolling the screen
        self.camera = None

        #gui camera
        self.gui_camera = None

        #keep trak score
        self.bullets = 0

        #set bg color
        ar.set_background_color(ar.color.ARSENIC)


    def load_shader(self):

        shader_file_path = Path('step_01.glsl')

        #size of window
        window_size = self.window.get_size()

        #create the shader toy
        self.shadertoy = Shadertoy.create_from_file(window_size, shader_file_path)

        #create channels 0 and 1, make buffer with 4 cannels (rgba)
        self.channel0 = self.shadertoy.ctx.framebuffer(color_attachments=[self.shadertoy.ctx.texture(window_size, components=4)])

        self.channel1 = self.shadertoy.ctx.framebuffer(color_attachments=[self.shadertoy.ctx.texture(window_size, components=4)])

        #assign the frame buffers to the cannels
        self.shadertoy.channel_0 = self.channel0.color_attachments[0]
        self.shadertoy.channel_1 = self.channel1.color_attachments[0]

    def setup(self):

        #setup the game

        # Set up the Camera
        self.camera = ar.Camera(self.window.width, self.window.height)

        #set up gui camera
        self.gui_camera = ar.Camera(self.window.width, self.window.height)

        #keep track score
        self.bullets = 10

        #setup offset
        self.offset_x = 0
        self.offset_y = 0

        #name of map to load
        map_name = 'untitled.json'

        #layers
        layer_options = {
                'Background': {
                    'use_spatial_hash': True,
                    },
                'Walls': {
                    'use_spatial_hash': True,
                    },
                }

        #read in the tiled map
        self.tile_map = ar.load_tilemap(map_name, tilemap_scal, layer_options)

        #init scene
        self.scene_map = ar.Scene.from_tilemap(self.tile_map)
        self.scene = ar.Scene()

        #create sprite list
        self.scene.add_sprite_list('Player')
        self.scene.add_sprite_list('Enemy')
        self.scene.add_sprite_list('Light')

        self.bullet_list = ar.SpriteList()
        #self.scene.add_sprite_list('Walls', use_spatial_hash=True)

        #angle
        self.angle = 0

        #setup the player
        image_sourse = 'images/test_player_1.png' # =====TEST====
        self.test_sprite = ar.Sprite(image_sourse, charecter_scal) # =====TEST====
        self.test_sprite.center_x = 64 # ===TEST===
        self.test_sprite.center_y = 64 # ===TEST===
        self.scene.add_sprite('Light', self.test_sprite) # ===TEST===

        self.player_sprite = PlayerCharecter()
        self.player_sprite.center_x = 400
        self.player_sprite.center_y = 400
        self.scene.add_sprite('Player', self.player_sprite)

        #======SET=UP=ENEMY=TEST====
        self.enemy_sprite = Enemy()
        self.enemy_sprite.center_x = 500
        self.enemy_sprite.center_y = 500
        self.scene.add_sprite('Enemy', self.enemy_sprite)

        #put some box
        #cord_list = [[512, 96], [256, 96], [768, 96]]
        #for cord in cord_list:
            #wall = ar.Sprite('images/boxCrate.png', tile_scal)
            #wall.position = cord
            #self.scene.add_sprite('Walls', wall)


        # use loop for create some ammo
        for x in range(128, 1250, 256):
            bullet = ar.Sprite('images/coinBronze.png', ammo_scal)
            bullet.center_x = x
            bullet.center_y = 256
            self.scene.add_sprite('Ammo', bullet)

        #create physics engine
        #self.physics_engine = ar.PhysicsEngineSimple(
        #        self.player_sprite, walls=[self.scene_map['Walls'], self.scene['Enemy']]
        #        )

        #=====TEST=NEW=ENGINE=====
        damping = 0.7
        gravity = (0, 0)


        self.physics_engine = ar.PymunkPhysicsEngine(damping=damping,
                                                     gravity=gravity)

        def wall_hit_handler(sprite_a, sprite_b, arbiter, space, data):
            bullet_shape = arbiter.shapes[0]
            bullet_sprite = self.physics_engine.get_sprite_for_shape(bullet_shape)
            bullet_sprite.remove_from_sprite_lists()
            print('Wall')

        self.physics_engine.add_collision_handler('bullet', 'wall', post_handler=wall_hit_handler)

        self.physics_engine.add_sprite(
                self.player_sprite,
                friction=0.6,
                moment_of_inertia=PymunkPhysicsEngine.MOMENT_INF,
                damping=0.01,
                collision_type='Player',
                max_velocity=200
                )

        self.physics_engine.add_sprite_list(
                self.scene_map['Walls'],
                friction=0.6,
                collision_type='wall',
                body_type=PymunkPhysicsEngine.STATIC
                )

    def on_mouse_press(self, x, y, button, modifiers):

        bullet = ar.SpriteSolidColor(5, 5, ar.color.RED)
        self.bullet_list.append(bullet)

        start_x = self.player_sprite.center_x
        start_y = self.player_sprite.center_y
        bullet.position = self.player_sprite.position

        ang = math.radians(angle+180)
        force = [math.cos(ang), math.sin(ang)]
        size = max(self.player_sprite.width, self.player_sprite.height)/2

        bullet.center_x += size * force[0]
        bullet.center_y += size * force[1]

        self.physics_engine.add_sprite(bullet,
                                       mass=0.1,
                                       damping=1.0,
                                       friction=0.6,
                                       collision_type='bullet',
                                       elasticity=0.9
                                       )

        force[0] *= BULLET_MOVE_FORCE
        force[1] *= BULLET_MOVE_FORCE

        self.physics_engine.apply_force(bullet, force)


    def on_draw(self):

        self.camera.use()

        #select the channel 0 frame buffer to draw on
        self.channel0.use()
        self.channel0.clear()

        #draw our scene
        self.scene_map['Walls'].draw()
        self.scene['Light'].draw()
        self.scene['Enemy'].draw()

        #select the window to draw on
        self.window.use()

        '''
        ar.draw_line(0,
                     0,
                     self.test_sprite.center_x-self.offset_x,
                     self.test_sprite.center_y-self.offset_y,
                     ar.color.BLUE, 2)

        ar.draw_line(self.test_sprite.center_x-self.offset_x,
                     self.test_sprite.center_y-self.offset_y,
                     self.mouse_x,
                     self.mouse_y,
                     ar.color.GREEN, 2)
        '''

        #render the sc
        self.clear()

        #calculate the light position
        p = (self.player_sprite.position[0] - self.camera.position[0],
             self.player_sprite.position[1] - self.camera.position[1])

        #p = (100, 100)
        #set the uniform data
        self.shadertoy.program['lightPosition'] = p
        self.shadertoy.program['lightSize'] = 500


        self.scene_map.draw()
        self.scene.draw()

        self.bullet_list.draw()
        #run the shader and render to the window
        self.shadertoy.render()


        self.gui_camera.use()

        #draw our ammo on the screen
        ammo_text = f'ammo: {self.bullets}'
        ar.draw_text(
                ammo_text,
                10, 10,
                ar.color.WHITE,
                18)
        #draw our angle on the screen
        angle_text = f'angle: {angle}'
        ar.draw_text(
                angle_text,
                210, 10,
                ar.color.WHITE,
                18)
    '''
    def update_player_speed(self):

        #calculate player speed
        self.player_sprite.change_x = 0
        self.player_sprite.change_y = 0
        #self.test_sprite.change_x = 0 # ===TEST===
        #self.test_sprite.change_y = 0 # ===TEST===

        if self.w_p and not self.s_p:
            force = (0, PLAYER_MOVE_FORCE)
            self.physics_engine.apply_force(self.player_sprite, force)
            #self.player_sprite.change_y = player_sp
            #self.test_sprite.change_y = player_sp # ===TEST===
            #self.mouse_y += player_sp
        elif self.s_p and not self.w_p:
            force = (0, -PLAYER_MOVE_FORCE)
            self.physics_engine.apply_force(self.player_sprite, force)
            #self.player_sprite.change_y = -player_sp
            #self.test_sprite.change_y = -player_sp # ===TEST===
            #self.mouse_y -= player_sp
        if self.a_p and not self.d_p:
            force = (-PLAYER_MOVE_FORCE, 0)
            self.physics_engine.apply_force(self.player_sprite, force)
            #self.player_sprite.change_x = -player_sp
            #self.test_sprite.change_x = -player_sp # ===TEST===
            #self.mouse_x -= player_sp
        elif self.d_p and not self.a_p:
            force = (PLAYER_MOVE_FORCE, 0)
            self.physics_engine.apply_force(self.player_sprite, force)
            #self.player_sprite.change_x = player_sp
            #self.test_sprite.change_x = player_sp # ===TEST===
            #self.mouse_x += player_sp
    '''
        #self.physics_engine.step()

    def on_key_press(self, key, modifiers):

        if key == ar.key.W:
            self.w_p = True
            #self.update_player_speed()
        if key == ar.key.S:
            self.s_p = True
            #self.update_player_speed()
        if key == ar.key.A:
            self.a_p = True
            #self.update_player_speed()
        if key == ar.key.D:
            self.d_p = True
            #self.update_player_speed()



    def on_key_release(self, key, modifiers):

        if key == ar.key.W:
            self.w_p = False
            #self.update_player_speed()
        if key == ar.key.S:
            self.s_p = False
            #self.update_player_speed()
        if key == ar.key.A:
            self.a_p = False
            #self.update_player_speed()
        if key == ar.key.D:
            self.d_p = False
            #self.update_player_speed()

    def center_camera_to_player(self):
        screen_center_x = self.player_sprite.center_x - (self.camera.viewport_width / 2)
        screen_center_y = self.player_sprite.center_y - (self.camera.viewport_height / 2)


        #print(self.mouse_x, self.mouse_y, mouse.get_position())

        #Don't let camera travel past 0
        '''
        if screen_center_x < 0:
            screen_center_x = 0
        if screen_center_y < 0:
            screen_center_y = 0
        '''

        player_centered = screen_center_x, screen_center_y
        offset_x, offset_y = screen_center_x, screen_center_y
        #print(offset_x, offset_y)

        #move camera to player with smoothly
        self.camera.move_to(player_centered, 0.1)


    def change_angle_player(self):

        global angle
        angle = round(math.degrees(math.atan2((
            self.camera.viewport_height/2-self.mouse_y),
            (self.camera.viewport_width/2-self.mouse_x))))

        #if self.mouse_x < (self.camera.viewport_width / 2):
        #    if self.mouse_y < (self.camera.viewport_height / 2):
        #        angle = 180 + angle
        #    else:
        #        angle = 180 - angle
        #else:
        #    if self.mouse_y < (self.camera.viewport_height / 2):
        #        angle = -angle

        self.test_sprite.angle = angle

        #print(angle)

    def on_mouse_motion(self, x, y, a, b):

        self.mouse_x = x
        self.mouse_y = y

    def on_update(self, delta_time):

        #game logic
        #print(mouse.get_position())
        #self.mouse_x, self.mouse_y = mouse.get_position()
        #self.mouse_x += self.offset_x
        #self.mouse_y += self.offset_y
        #print(self.test_sprite.center_x, self.test_sprite.center_y)

        #calculate player speed
        self.player_sprite.change_x = 0
        self.player_sprite.change_y = 0
        #self.test_sprite.change_x = 0 # ===TEST===
        #self.test_sprite.change_y = 0 # ===TEST===

        if self.w_p and not self.s_p:
            force = (0, PLAYER_MOVE_FORCE)
            self.physics_engine.apply_force(self.player_sprite, force)
            #self.player_sprite.change_y = player_sp
            #self.test_sprite.change_y = player_sp # ===TEST===
            #self.mouse_y += player_sp
        elif self.s_p and not self.w_p:
            force = (0, -PLAYER_MOVE_FORCE)
            self.physics_engine.apply_force(self.player_sprite, force)
            #self.player_sprite.change_y = -player_sp
            #self.test_sprite.change_y = -player_sp # ===TEST===
            #self.mouse_y -= player_sp
        if self.a_p and not self.d_p:
            force = (-PLAYER_MOVE_FORCE, 0)
            self.physics_engine.apply_force(self.player_sprite, force)
            #self.player_sprite.change_x = -player_sp
            #self.test_sprite.change_x = -player_sp # ===TEST===
            #self.mouse_x -= player_sp
        elif self.d_p and not self.a_p:
            force = (PLAYER_MOVE_FORCE, 0)
            self.physics_engine.apply_force(self.player_sprite, force)
            #self.player_sprite.change_x = player_sp
            #self.test_sprite.change_x = player_sp # ===TEST===
            #self.mouse_x += player_sp


        # Activate our Camera
        self.camera.use()


        #see if we hit any ammo
        ammo_hit_list = ar.check_for_collision_with_list(
                self.player_sprite, self.scene['Ammo'])

        #loop throught each ammo we hit and remove it
        for bullet in ammo_hit_list:
            #remove ammo
            bullet.remove_from_sprite_lists()
            # add 10 bullet to ammo
            self.bullets += 10

        #Position the camera
        self.center_camera_to_player()
        self.test_sprite.center_x = self.player_sprite.center_x
        self.test_sprite.center_y = self.player_sprite.center_y

        #update animations
        self.scene.update_animation(delta_time, ['Player'])
        self.player_sprite.update_animations(delta_time)

        #angle of player
        self.change_angle_player()

        #move player
        self.physics_engine.step(delta_time)

def main():
    global start_view
    window = ar.Window(sc_w, sc_h, sc_title)
    start_view = MainMenuView()
    window.show_view(start_view)
    ar.run()


if __name__ == '__main__':
    main()
