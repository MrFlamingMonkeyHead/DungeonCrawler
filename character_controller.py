import pygame
import time

# Initialize pygame
pygame.init()

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60

import pygame

class PlayerController:
    def __init__(self, x, y, speed, sprite_sheet_path="Archer-Green.png"):
        self.sprite_sheet = pygame.image.load(sprite_sheet_path).convert_alpha()
        self.rect = pygame.Rect(x, y, 32, 32)
        self.speed = speed
        self.position = [x, y]
        self.animation_frames = [0]
        self.previous_frames = self.animation_frames
        self.current_frame = 0
        self.animation_speed = 0.2
        self.animation_timer = 0

        self.sheet_columns = 24
        self.sheet_rows = 8
        self.frame_width = 32
        self.frame_height = 32
        self.is_attacking = False

    def handle_events(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Left mouse button
                self.start_attack_animation()

    def start_attack_animation(self):
        self.animation_frames = [4, 5, 6, 7]
        self.current_frame = 0
        self.previous_frames = self.animation_frames
        #self.update_animation(0)  # force an immediate frame update

    def move(self, keys, dt):
        if self.is_attacking:
            return
        dx, dy = 0, 0
        if keys[pygame.K_s] and keys[pygame.K_d]:
            dx = self.speed
            dy = self.speed
            self.animation_frames = [24, 25, 26, 27]
        elif keys[pygame.K_d] and keys[pygame.K_w]:
            dx = self.speed
            dy = -self.speed
            self.animation_frames = [72, 73, 74, 75]
        elif keys[pygame.K_w] and keys[pygame.K_a]:
            dx = -self.speed
            dy = -self.speed
            self.animation_frames = [120, 121, 122, 123]
        elif keys[pygame.K_a] and keys[pygame.K_s]:
            dx = -self.speed
            dy = self.speed
            self.animation_frames = [169, 170, 171, 172]
        elif keys[pygame.K_s]:
            dy = self.speed
            self.animation_frames = [0, 1, 2, 3]
        elif keys[pygame.K_d]:
            dx = self.speed
            self.animation_frames = [48, 49, 50, 51]
        elif keys[pygame.K_w]:
            dy = -self.speed
            self.animation_frames = [96, 97, 98, 99]
        elif keys[pygame.K_a]:
            dx = -self.speed
            self.animation_frames = [144, 145, 146, 147]
        else:
            self.animation_frames = [self.animation_frames[0]]

        if self.animation_frames != self.previous_frames:
            self.current_frame = 0
            self.previous_frames = self.animation_frames

        self.position[0] += dx * dt * 60
        self.position[1] += dy * dt * 60

        self.rect.topleft = (int(self.position[0]), int(self.position[1]))

    def update_animation(self, dt):
        if self.animation_frames:
        # Update the animation frame based on time_elapsed or other logic
        # Here, we'll simply advance the frame by one in order
            self.current_frame += 1

            if self.current_frame >= len(self.animation_frames):
                # Animation is complete, reset to the beginning
                self.current_frame = 0
            
            # Return to idle animation after attack finishes
            #if self.animation_frames == [192, 193, 194, 195] and self.current_frame == 0:
                #self.animation_frames = [self.animation_frames[0]]  # This would be the idle frame (or adjust as needed)
            #if self.animation_frames == [4, 5, 6, 7] and self.current_frame == 0 and self.animation_timer == 0:
                #self.is_attacking = False

    def draw(self, screen, camera_offset):
        frame_index = self.animation_frames[self.current_frame]
        col = frame_index % self.sheet_columns
        row = frame_index // self.sheet_columns
        frame_x = col * self.frame_width
        frame_y = row * self.frame_height
        frame_rect = pygame.Rect(frame_x, frame_y, self.frame_width, self.frame_height)
        frame = self.sprite_sheet.subsurface(frame_rect)

        screen.blit(frame, (self.rect.x - camera_offset[0], self.rect.y - camera_offset[1]))

class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Follow Player Camera with Attack Event")
        self.clock = pygame.time.Clock()
        self.running = True

    def run(self):
        player = PlayerController(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2, 5)

        while self.running:
            dt = self.clock.tick(FPS) / 1000
            

            # Handle all events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                player.handle_events(event)  # Handle player-specific events, including attack

            keys = pygame.key.get_pressed()
            player.move(keys, dt)
            player.update_animation(dt)

            # Camera logic
            camera_offset = [player.rect.x - SCREEN_WIDTH // 2, player.rect.y - SCREEN_HEIGHT // 2]

            self.screen.fill((0, 0, 0))
            player.draw(self.screen, camera_offset)

            pygame.draw.rect(self.screen, (255, 0, 0), (200 - camera_offset[0], 200 - camera_offset[1], 50, 50))  # Red square for reference

            pygame.display.flip()

        pygame.quit()

if __name__ == "__main__":
    Game().run()

