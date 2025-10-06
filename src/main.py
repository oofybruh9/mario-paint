import pygame, random, os # type: ignore

PATH = os.path.dirname(os.path.abspath('__file__'))+"/"

def run_game(width, height, fps, starting_scene):
    pygame.init()
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Mario Paint: Python Version")
    pygame.mouse.set_visible(False)

    active_scene = starting_scene

    while active_scene is not None:
        pressed_keys = pygame.key.get_pressed()
        
        # Event filtering
        filtered_events = []
        for event in pygame.event.get():
            quit_attempt = False
            if event.type == pygame.QUIT:
                quit_attempt = True
            elif event.type == pygame.KEYDOWN:
                alt_pressed = pressed_keys[pygame.K_LALT] or pressed_keys[pygame.K_RALT]
                if event.key == pygame.K_ESCAPE:
                    quit_attempt = True
                elif event.key == pygame.K_F4 and alt_pressed:
                    quit_attempt = True
            
            if quit_attempt:
                active_scene.Terminate()
            else:
                filtered_events.append(event)
        
        active_scene.ProcessInput(filtered_events, pressed_keys)
        active_scene.Update()
        active_scene.Render(screen)
        
        active_scene = active_scene.next
        
        pygame.display.flip()
        clock.tick(fps)

class SceneBase:
    def __init__(self):
        self.next = self

    def ProcessInput(self, events, pressed_keys):
        print("uh-oh, you didn't override this in the child class")

    def Update(self):
        print("uh-oh, you didn't override this in the child class")

    def Render(self, screen):
        print("uh-oh, you didn't override this in the child class")

    def SwitchToScene(self, next_scene):
        self.next = next_scene

    def Terminate(self):
        self.SwitchToScene(None)

class TitleScene(SceneBase):
    def __init__(self):
        SceneBase.__init__(self)
        # Play Mario Paint title music once
        pygame.mixer.init()
        titlemusic = PATH+"assets/music/Mario Paint.wav"
        pygame.mixer.music.load(titlemusic)
        pygame.mixer.music.play(-1)  # -1 = loop forever

    def ProcessInput(self, events, pressed_keys):
        for event in events:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                pygame.mixer.music.stop()   # stop title music
                self.SwitchToScene(Cheering())

    def Update(self):
        pass

    def Render(self, screen):
        width, height = 1024, 768
        custom_cursor_image = pygame.image.load(PATH+"assets/spritesheets/cursor.png").convert_alpha()
        cursor = pygame.transform.scale(custom_cursor_image, (52, 52))
        WHITE, BLACK = (255, 255, 255), (0, 0, 0)

        font = pygame.font.Font(PATH+'assets/mario-paint-title.ttf', 56)
        screen.fill((254, 255, 250))
        title_text = font.render("MARIO PAINT", True, BLACK)
        title_rect = title_text.get_rect(center=(width // 2, height // 4))
        screen.blit(title_text, title_rect)

        instruction_font = pygame.font.Font(PATH+'assets/snes-fonts-mario-paint.ttf', 24)
        instruction_text = instruction_font.render("(C) 1992  NINTENDO", True, BLACK)
        instruction_rect = instruction_text.get_rect(center=(width // 2, height * 2 // 2.2))
        screen.blit(instruction_text, instruction_rect)

        mouse_pos = pygame.mouse.get_pos()
        screen.blit(cursor, mouse_pos)

class Cheering(SceneBase):
    def __init__(self):
        SceneBase.__init__(self)
        pygame.mixer.init()
        self.start_time = pygame.time.get_ticks()
        self.sound_played = False  # flag so we only play once

        # pick random sound
        if random.randint(1, 2) == 1:
            self.cheer_file = PATH+"assets/music/Cheering.mp3"
        else:
            self.cheer_file = PATH+"assets/music/Fan Chant.mp3"

    def Update(self):
        # Check if 2 seconds passed and sound not played yet
        elapsed = pygame.time.get_ticks() - self.start_time
        if elapsed >= 2000 and not self.sound_played:
            self.chant = pygame.mixer.Sound(self.cheer_file)
            self.chant.play()
            self.sound_played = True

    def Render(self, screen):
        screen.fill((200, 255, 200))
    def ProcessInput(self, events, pressed_keys):
        pass


run_game(1024, 768, 60, TitleScene())
