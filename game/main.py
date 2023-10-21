import arcade as ar
import arcade.gui
import math

#const
sc_w = 1000
sc_h = 650
sc_title = 'test'

#const for scale
charecter_scal = 1
tile_scal = 0.5
ammo_scal = 0.3

#movment speed per frame
player_sp = 5


class QuitButton(ar.gui.UIFlatButton):

    def on_click(self, event: ar.gui.UIOnClickEvent):
        ar.exit


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


        #separete variable that holds the playre sprite
        self.player_sprite = None
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

        #init scene
        self.scene = ar.Scene()

        #create sprite list
        self.scene.add_sprite_list('Player')
        self.scene.add_sprite_list('Walls', use_spatial_hash=True)

        #angle
        self.angle = 0

        #setup the player
        image_sourse = 'images/test_player.png'
        self.player_sprite = ar.Sprite(image_sourse, charecter_scal,
                                       angle=self.angle, hit_box_algorithm='Simple')
        self.player_sprite.center_x = 64
        self.player_sprite.center_y = 64
        self.scene.add_sprite('Player', self.player_sprite)

        #put some box
        cord_list = [[512, 96], [256, 96], [768, 96]]
        for cord in cord_list:
            wall = ar.Sprite('images/boxCrate.png', tile_scal)
            wall.position = cord
            self.scene.add_sprite('Walls', wall)


        # use loop for create some ammo
        for x in range(128, 1250, 256):
            bullet = ar.Sprite('images/coinBronze.png', ammo_scal)
            bullet.center_x = x
            bullet.center_y = 256
            self.scene.add_sprite('Ammo', bullet)

        #create physics engine
        self.physics_engine = ar.PhysicsEngineSimple(
                self.player_sprite, self.scene.get_sprite_list('Walls')
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



    def update_player_speed(self):

        #calculate player speed
        self.player_sprite.change_x = 0
        self.player_sprite.change_y = 0

        if self.w_p and not self.s_p:
            self.player_sprite.change_y = player_sp
            self.mouse_y += player_sp
        elif self.s_p and not self.w_p:
            self.player_sprite.change_y = -player_sp
            self.mouse_y -= player_sp
        if self.a_p and not self.d_p:
            self.player_sprite.change_x = -player_sp
            self.mouse_x -= player_sp
        elif self.d_p and not self.a_p:
            self.player_sprite.change_x = player_sp
            self.mouse_x += player_sp

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

        #Don't let camera travel past 0
        if screen_center_x < 0:
            screen_center_x = 0
        if screen_center_y < 0:
            screen_center_y = 0
        player_centered = screen_center_x, screen_center_y

        #move camera to player with smoothly
        self.camera.move_to(player_centered, 0.1)

    def on_mouse_motion(self, x, y, button, modifiers):

        self.mouse_x = x
        self.mouse_y = y

    def chenge_angle_player(self):

        self.angle = round(-math.degrees(math.atan2((
            self.player_sprite.center_x-self.mouse_x),
            (self.player_sprite.center_y-self.mouse_y))))
        self.player_sprite.angle = self.angle+90

    def on_update(self, delta_time):

        #game logic

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

        #angle of player
        self.chenge_angle_player()

def main():
    window = ar.Window(sc_w, sc_h, sc_title)
    start_view = MainMenuView()
    window.show_view(start_view)
    ar.run()


if __name__ == '__main__':
    main()
