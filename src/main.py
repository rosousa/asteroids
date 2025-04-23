import pygame
from constants import *
from player import Player
from asteroid import Asteroid
from asteroidfield import AsteroidField
from shot import Shot


def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pygame.time.Clock()

    updatable = pygame.sprite.Group()
    drawable = pygame.sprite.Group()
    asteroids = pygame.sprite.Group()
    shots = pygame.sprite.Group()

    Asteroid.containers = (asteroids, updatable, drawable)
    Shot.containers = (shots, updatable, drawable)
    AsteroidField.containers = updatable
    asteroid_field = AsteroidField()

    Player.containers = (updatable, drawable)

    player = Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)

    dt = 0

    collision_detected = False

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return

        updatable.update(dt)

        player.timer -= dt

        if len(pygame.sprite.Group(asteroids).sprites()) > 0:
            asteroids_sprites = pygame.sprite.Group(asteroids).sprites()

            for i in range(0, len(asteroids_sprites)):
                asteroid_exploded = False
                shots_sprites = pygame.sprite.Group(shots).sprites()

                if len(shots_sprites) > 0:
                    for j in range(0, len(shots_sprites)):
                        if asteroids_sprites[i].checkCollision(shots_sprites[j]):
                            shots_sprites[j].kill()
                            asteroids_sprites[i].kill()
                            asteroid_exploded = True
                            break

                if asteroid_exploded:
                    continue

                if player.checkCollision(asteroids_sprites[i]):
                    collision_detected = True
                    break

        if collision_detected:
            return

        screen.fill("black")

        for obj in drawable:
            obj.draw(screen)

        pygame.display.flip()

        # limit the framerate to 60 FPS
        dt = clock.tick(60) / 1000


if __name__ == "__main__":
    main()
