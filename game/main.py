import arcade as ar
import arcade.gui
import math
import mouse

#const
sc_w = 1000
sc_h = 650
sc_title = 'test'

#const for scale
charecter_scal = 1.5
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
player_sp = 5

#angle mouse
angle = 0


def load_texture_pair(filename):
    return [
            ar.load_texture(filename),
            ar.load_texture(filename, flipped_horizontally=True)
            ]


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

        self.walk_texture = []
        for i in range(8): # walk left/right
            texture = load_texture_pair(f'{main_path}walk/right{i}.png')
            self.walk_texture.append(texture)

        #set the initial texture
        self.texture = self.idle_texture_pair[0]

        #hit box
        self.hit_box = self.texture.hit_box_points

    def update_animations(self, delta_time: float = 1/60):

        #change face direction if press wasd

        if self.change_x < 0 and self.charecter_face_direction == RIGHT_FACING:
            self.charecter_face_direction = LEFT_FACING
        elif self.change_x > 0 and self.charecter_face_direction == LEFT_FACING:
            self.charecter_face_direction = RIGHT_FACING

        """
        #change face direction if mose motion
        if -15 < angle < 15:
            self.charecter_face_direction = LEFT_FACING
        elif -165 > angle > -180 or 180 > angle > 165:
            self.charecter_face_direction = RIGHT_FACING
        """

        #idle animation
        if self.change_x == 0 and self.change_y == 0:
            self.texture = self.idle_texture_pair[self.charecter_face_direction]
            return

        #walk animation
        self.cur_texture += 1
        if self.cur_texture > 7*fps:
            self.cur_texture = 0
        self.texture = self.walk_texture[self.cur_texture//fps][self.charecter_face_direction]


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
        game_view.setup()
        self.window.show_view(game_view)

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

        #our phisics engine
        self.physics_engine = None

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

        #separete variable that holds the playre sprite
        self.player_sprite = None
        self.test_sprite = None # =====TEST=====
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
        self.scene = ar.Scene.from_tilemap(self.tile_map)

        #create sprite list
        self.scene.add_sprite_list('Player')
        #self.scene.add_sprite_list('Walls', use_spatial_hash=True)

        #angle
        self.angle = 0

        #setup the player
        image_sourse = 'images/test_player.png' # =====TEST====
        self.test_sprite = ar.Sprite(image_sourse, charecter_scal) # =====TEST====
        self.test_sprite.center_x = 64 # ===TEST===
        self.test_sprite.center_y = 64 # ===TEST===
        self.scene.add_sprite('Player', self.test_sprite) # ===TEST===

        self.player_sprite = PlayerCharecter()
        self.player_sprite.center_x = 64
        self.player_sprite.center_y = 64
        self.scene.add_sprite('Player', self.player_sprite)

        #put some box
        cord_list = [[512, 96], [256, 96], [768, 96]]
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
        self.physics_engine = ar.PhysicsEngineSimple(
                self.player_sprite, walls=self.scene['Walls']
                )


    def on_draw(self):

        #render the sc
        self.clear()

        #draw our scene
        self.scene.draw()

        #activate gui camera
        self.gui_camera.use()

        #draw our ammo on the screen
        ammo_text = f'ammo: {self.bullets}'
        ar.draw_text(
                ammo_text,
                10, 10,
                ar.color.WHITE,
                18)

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


    def update_player_speed(self):

        #calculate player speed
        self.player_sprite.change_x = 0
        self.player_sprite.change_y = 0
        #self.test_sprite.change_x = 0 # ===TEST===
        #self.test_sprite.change_y = 0 # ===TEST===

        if self.w_p and not self.s_p:
            self.player_sprite.change_y = player_sp
            #self.test_sprite.change_y = player_sp # ===TEST===
            #self.mouse_y += player_sp
        elif self.s_p and not self.w_p:
            self.player_sprite.change_y = -player_sp
            #self.test_sprite.change_y = -player_sp # ===TEST===
            #self.mouse_y -= player_sp
        if self.a_p and not self.d_p:
            self.player_sprite.change_x = -player_sp
            #self.test_sprite.change_x = -player_sp # ===TEST===
            #self.mouse_x -= player_sp
        elif self.d_p and not self.a_p:
            self.player_sprite.change_x = player_sp
            #self.test_sprite.change_x = player_sp # ===TEST===
            #self.mouse_x += player_sp

    def on_key_press(self, key, modifiers):

        if key == ar.key.W:
            self.w_p = True
            self.update_player_speed()
        if key == ar.key.S:
            self.s_p = True
            self.update_player_speed()
        if key == ar.key.A:
            self.a_p = True
            self.update_player_speed()
        if key == ar.key.D:
            self.d_p = True
            self.update_player_speed()


    def on_key_release(self, key, modifiers):

        if key == ar.key.W:
            self.w_p = False
            self.update_player_speed()
        if key == ar.key.S:
            self.s_p = False
            self.update_player_speed()
        if key == ar.key.A:
            self.a_p = False
            self.update_player_speed()
        if key == ar.key.D:
            self.d_p = False
            self.update_player_speed()

    def center_camera_to_player(self):
        screen_center_x = self.player_sprite.center_x - (self.camera.viewport_width / 2)
        screen_center_y = self.player_sprite.center_y - (self.camera.viewport_height / 2)


        print(self.mouse_x, self.mouse_y, mouse.get_position())

        #Don't let camera travel past 0
        #if screen_center_x < 0:
        #    screen_center_x = 0
        #if screen_center_y < 0:
        #    screen_center_y = 0
        player_centered = screen_center_x, screen_center_y
        offset_x, offset_y = screen_center_x, screen_center_y
        print(offset_x, offset_y)

        #move camera to player with smoothly
        self.camera.move_to(player_centered, 0.1)


    def change_angle_player(self):

        global angle
        angle = round(math.degrees(math.atan2((
            self.test_sprite.center_y-self.mouse_y-self.offset_y),
            (self.test_sprite.center_x-self.mouse_x-self.offset_x))))
        self.test_sprite.angle = angle

        print(angle)

    def on_mouse_motion(self, x, y, a, b):

        self.mouse_x = x
        self.mouse_y = y

    def on_update(self, delta_time):

        #game logic
        #print(mouse.get_position())
        #self.mouse_x, self.mouse_y = mouse.get_position()
        #self.mouse_x += self.offset_x
        #self.mouse_y += self.offset_y
        print(self.test_sprite.center_x, self.test_sprite.center_y)



        # Activate our Camera
        self.camera.use()

        #move player
        self.physics_engine.update()

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

def main():
    window = ar.Window(sc_w, sc_h, sc_title)
    start_view = MainMenuView()
    window.show_view(start_view)
    ar.run()


if __name__ == '__main__':
    main()
