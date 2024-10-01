# Libraries
import pygame
import sys
import math
import random

pygame.init()

# Constants
WIDTH, HEIGHT = 800, 600
BACKGROUND_COLOR = (0, 0, 0)
PLANET1_COLOR = (255,192,203)
PLANET2_COLOR = (100, 100, 200)
ASTEROID_COLOR = (173, 216, 230)
G = 20 # Gravitational constant
frame_rate = 120
time_step = 1 / frame_rate

# Classes
class CelestialObject:
    def __init__(self, x, y, mass, radius, color):
        self.x = x
        self.y = y
        self.mass = mass
        self.radius = radius
        self.color = color
        self.acceleration_x = 0
        self.acceleration_y = 0
        self.velocity_x = 0
        self.velocity_y = 0

    def apply_gravity(self, other):
        if other is not None and self.mass != 0:
            dx = other.x - self.x
            dy = other.y - self.y
            distance = max(1, math.sqrt(dx ** 2 + dy ** 2))
            force = G * self.mass * other.mass / (distance ** 2) # Newton's law of gravitation
            angle = math.atan2(dy, dx)
            self.acceleration_x = force * math.cos(angle) / self.mass
            self.acceleration_y = force * math.sin(angle) / self.mass
            self.velocity_x += self.acceleration_x * time_step
            self.velocity_y += self.acceleration_y * time_step

    def update(self):
        self.x += 0.5 * self.acceleration_x * time_step ** 2 + self.velocity_x * time_step
        self.y += 0.5 * self.acceleration_y * time_step ** 2 + self.velocity_y * time_step

class Planet(CelestialObject):
    def __init__(self, x, y, mass, radius, color):
        super().__init__(x, y, mass, radius, color)
        self.shockwaves = []

class Asteroid(CelestialObject):
    def __init__(self, x, y, mass, radius, color, velocity_x, velocity_y):
        super().__init__(x, y, mass, radius, color)
        self.velocity_x = velocity_x
        self.velocity_y = velocity_y
        self.target_planet = None 

class Particle:
    def __init__(self, x, y, size, color):
        self.x = x
        self.y = y
        self.size = size
        self.color = color
        self.velocity = [random.uniform(-0.07, 0.07), random.uniform(-0.07, 0.07)]
        self.alpha = 255

    def move(self):
        self.x += self.velocity[0]
        self.y += self.velocity[1]
        self.alpha -= 0.4 

    def is_faded(self):
        return self.alpha <= 0
    
class Shockwave:
    def __init__(self, x, y, max_radius, expansion_speed, initial_alpha, strength, creator_planet):
        self.x = x
        self.y = y
        self.max_radius = max_radius
        self.expansion_speed = expansion_speed
        self.current_radius = 0
        self.current_alpha = initial_alpha
        self.strength = strength
        self.creator_planet = creator_planet

    def update(self):
        self.current_radius += self.expansion_speed
        self.current_alpha -= 0.1  
        if self.strength > 0:
            self.strength -= 0.1

    def is_faded(self):
        return self.current_alpha <= 0  

def create_explosion(x, y):
    explosion = []
    for _ in range(20):
        size = random.randint(2, 6)
        color = (random.randint(200, 255), random.randint(100, 200), 0)
        particle = Particle(x, y, size, color)
        explosion.append(particle)
    return explosion

# Create planets
planet1 = Planet(WIDTH // 3, HEIGHT // 2, 5000, 20, PLANET1_COLOR)
planet1.velocity_x = 0 
planet1.velocity_y = 0  
planet2 = Planet(2 * WIDTH // 3, HEIGHT // 2, 7000, 25, PLANET2_COLOR)
planet2.velocity_x = 0  
planet2.velocity_y = 0  

asteroids = [] 
explosions = [] 
shockwaves = []
planets_hit_by_asteroid = []

# Screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Planetary Motion and Asteroid Impact")

# Main simulation loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.MOUSEBUTTONDOWN:
            x, y = event.pos
            asteroid = Asteroid(x, y, 100, 5, ASTEROID_COLOR, 0, 0)

            # Which planet was hit by the asteroid
            if planet1.x - asteroid.x < planet1.radius and planet1.y - asteroid.y < planet1.radius:
                asteroid.target_planet = planet1
            elif planet2.x - asteroid.x < planet2.radius and planet2.y - asteroid.y < planet2.radius:
                asteroid.target_planet = planet2
            asteroids.append(asteroid)

    # Apply gravity to planets and asteroids
    for asteroid in asteroids:
        planet1.apply_gravity(asteroid)
        planet2.apply_gravity(asteroid)
        asteroid.apply_gravity(planet1)
        asteroid.apply_gravity(planet2)

    # Gravity planet to planet
    # planet1.apply_gravity(planet2)
    # planet2.apply_gravity(planet1)

    # Update positions and handle screen boundaries for planets
    for planet in [planet1, planet2]:
        planet.update()
        if planet.x - planet.radius < 0:
            planet.x = planet.radius
            planet.velocity_x *= -0.7
        elif planet.x + planet.radius > WIDTH:
            planet.x = WIDTH - planet.radius
            planet.velocity_x *= -0.7
        if planet.y - planet.radius < 0:
            planet.y = planet.radius
            planet.velocity_y *= -0.7
        elif planet.y + planet.radius > HEIGHT:
            planet.y = HEIGHT - planet.radius
            planet.velocity_y *= -0.7

    # Planet-planet collisions
    if planet1 != planet2:
        dx = planet2.x - planet1.x
        dy = planet2.y - planet1.y
        distance = math.sqrt(dx ** 2 + dy ** 2)
        
        # Restitution coefficient (0 = perfectly inelastic, 1 = perfectly elastic)
        restitution_coefficient = 0.3

        if distance < planet1.radius + planet2.radius:
            overlap = (planet1.radius + planet2.radius - distance)
            angle = math.atan2(dy, dx)

            # Move the planets apart so they don't overlap
            planet1.x -= overlap * 0.5 * math.cos(angle)
            planet1.y -= overlap * 0.5 * math.sin(angle)
            planet2.x += overlap * 0.5 * math.cos(angle)
            planet2.y += overlap * 0.5 * math.sin(angle)

            # Calculate the relative velocity
            relative_velocity_x = planet2.velocity_x - planet1.velocity_x
            relative_velocity_y = planet2.velocity_y - planet1.velocity_y

            # Calculate the normal vector along the collision axis
            normal_x = math.cos(angle)
            normal_y = math.sin(angle)

            # Calculate the dot product of the relative velocity and the normal
            dot_product = relative_velocity_x * normal_x + relative_velocity_y * normal_y

            # Update the velocities
            planet1.velocity_x += 2 * restitution_coefficient * dot_product * normal_x
            planet1.velocity_y += 2 * restitution_coefficient * dot_product * normal_y
            planet2.velocity_x -= 2 * restitution_coefficient * dot_product * normal_x
            planet2.velocity_y -= 2 * restitution_coefficient * dot_product * normal_y

    # Update positions and handle screen boundaries for asteroids
    for asteroid in asteroids:
        asteroid.update()
        if asteroid.x - asteroid.radius < 0 or asteroid.x + asteroid.radius > WIDTH:
            asteroid.velocity_x *= -0.7
        if asteroid.y - asteroid.radius < 0 or asteroid.y + asteroid.radius > HEIGHT:
            asteroid.velocity_y *= -0.7

    # Asteroid-planet collisions
    for asteroid in asteroids[:]:
        for planet in [planet1, planet2]:
            dx = planet.x - asteroid.x
            dy = planet.y - asteroid.y
            distance = math.sqrt(dx ** 2 + dy ** 2)
            if distance < planet.radius + asteroid.radius:
                if planet.mass + asteroid.mass != 0:
                    planet.velocity_x = (planet.mass * planet.velocity_x + asteroid.mass * asteroid.velocity_x) / (planet.mass + asteroid.mass)
                    planet.velocity_y = (planet.mass * planet.velocity_y + asteroid.mass * asteroid.velocity_y) / (planet.mass + asteroid.mass)
                    planet.mass -= asteroid.mass
                    asteroids.remove(asteroid)

                # Explosion at the collision point
                explosion = create_explosion(asteroid.x, asteroid.y)
                explosions.append(explosion)

                # Shockwave at the collision point
                shockwave = Shockwave(asteroid.x, asteroid.y, 80, 0.1, 255, 160, asteroid.target_planet)
                planet.shockwaves.append(shockwave)

                planets_hit_by_asteroid.append(planet)
                # Remove the first planet in the list if there are two planets in it
                if len(planets_hit_by_asteroid) > 1:
                    planets_hit_by_asteroid.pop(0)

    planets_hit_by_asteroid = list(set(planets_hit_by_asteroid))

    # Update position of particles in explosion
    for explosion in explosions:
        for particle in explosion:
            particle.move()
        if all(particle.alpha <= 0 for particle in explosion):
            explosions.remove(explosion)

    # Update position of shockwaves for each planet
    for planet in [planet1, planet2]:
        for shockwave in planet.shockwaves:
            shockwave.update()

        # Iterate through the shockwaves associated with the current planet
        for shockwave in planet.shockwaves:
            for other_planet in [planet1, planet2]:
                if other_planet != planet:
                    dx = other_planet.x - shockwave.x
                    dy = other_planet.y - shockwave.y
                    distance = max(1, math.sqrt(dx ** 2 + dy ** 2))
                    if distance < shockwave.current_radius:
                        angle = math.atan2(dy, dx)
                        force = shockwave.strength / distance
                        other_planet.velocity_x += force * math.cos(angle)
                        other_planet.velocity_y += force * math.sin(angle)

        # Remove faded shockwaves from the list
        planet.shockwaves = [shockwave for shockwave in planet.shockwaves if not shockwave.is_faded()]

    # Clear the screen
    screen.fill(BACKGROUND_COLOR)

    # Drawing section
    for planet in [planet1, planet2]:
        for shockwave in planet.shockwaves:
            if shockwave.current_radius > 0:
                num_dots = 20
                dot_radius = 1.5
                for i in range(num_dots):
                    angle = i * (2 * math.pi / num_dots)
                    x_dot = shockwave.x + shockwave.current_radius * math.cos(angle)
                    y_dot = shockwave.y + shockwave.current_radius * math.sin(angle)
                    pygame.draw.circle(screen, (0, 255, 255, shockwave.current_alpha), (int(x_dot), int(y_dot)), dot_radius)

        # Check if any shockwaves have faded completely and remove them from the list
        planet.shockwaves = [shockwave for shockwave in planet.shockwaves if not shockwave.is_faded()]

    pygame.draw.circle(screen, planet1.color, (int(planet1.x), int(planet1.y)), planet1.radius)
    pygame.draw.circle(screen, planet2.color, (int(planet2.x), int(planet2.y)), planet2.radius)
    for asteroid in asteroids:
        pygame.draw.circle(screen, asteroid.color, (int(asteroid.x), int(asteroid.y)), asteroid.radius)

    for explosion in explosions:
        for particle in explosion:
            pygame.draw.circle(screen, particle.color + (particle.alpha,), (int(particle.x), int(particle.y)), particle.size)

    # Check if all particles in each explosion have faded and remove the finished explosions
    explosions = [explosion for explosion in explosions if not all(particle.alpha <= 0 for particle in explosion)]

    pygame.display.flip()