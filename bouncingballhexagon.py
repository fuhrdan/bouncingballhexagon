###############################################################################
## AI Code generated from the following prompt:                              ##
## Please write a python program that shows a ball bouncing inside a         ##
## spinning hexagon.  The ball should be affected by gravity and friction,   ##
## and it must bounce off the rotating walls realistically.                  ##
###############################################################################
###############################################################################

import pygame
import numpy as np

# Constants
WIDTH, HEIGHT = 600, 600
BACKGROUND_COLOR = (10, 10, 30)
BALL_COLOR = (255, 100, 100)
HEX_COLOR = (100, 255, 100)
BALL_RADIUS = 10
GRAVITY = np.array([0, 0.5])  # Stronger gravity
FRICTION = 0.995  # Less friction, so gravity has a stronger effect
ROTATION_SPEED = 0.02  # Radians per frame

# Initialize pygame
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

def hexagon_vertices(center, size, angle):
    return [
        (
            center[0] + size * np.cos(angle + np.pi / 3 * i),
            center[1] + size * np.sin(angle + np.pi / 3 * i)
        )
        for i in range(6)
    ]

def point_line_distance(point, line_start, line_end):
    line_vec = line_end - line_start
    point_vec = point - line_start
    
    line_length = np.dot(line_vec, line_vec)
    if line_length == 0:
        return np.linalg.norm(point_vec), line_start
    
    projection = np.dot(point_vec, line_vec) / line_length
    projection = np.clip(projection, 0, 1)
    closest_point = line_start + projection * line_vec
    distance = np.linalg.norm(point - closest_point)
    return distance, closest_point

# Ball properties
ball_pos = np.array([WIDTH // 2, HEIGHT // 3], dtype=np.float64)
ball_vel = np.array([2.0, -2.0], dtype=np.float64)
hex_size = 200
angle = 0

running = True
while running:
    screen.fill(BACKGROUND_COLOR)
    
    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    # Update hexagon rotation
    angle += ROTATION_SPEED
    vertices = hexagon_vertices((WIDTH // 2, HEIGHT // 2), hex_size, angle)
    
    # Update ball physics
    ball_vel[0] *= FRICTION  # Apply friction to horizontal movement
    ball_vel[1] += GRAVITY[1]  # Apply gravity
    ball_pos += ball_vel
    
    # Check collisions with hexagon edges
    for i in range(6):
        p1, p2 = np.array(vertices[i]), np.array(vertices[(i + 1) % 6])
        distance, closest_point = point_line_distance(ball_pos, p1, p2)
        
        if distance <= BALL_RADIUS:  # Collision detected
            edge_vector = p2 - p1
            normal = np.array([-edge_vector[1], edge_vector[0]])
            normal /= np.linalg.norm(normal)
            
            if np.dot(ball_vel, normal) < 0:  # Ensure ball is moving towards the wall
                ball_pos += normal * (BALL_RADIUS - distance)  # Correct position
                ball_vel -= 2 * np.dot(ball_vel, normal) * normal  # Reflect velocity
    
    # Draw hexagon
    pygame.draw.polygon(screen, HEX_COLOR, vertices, 2)
    
    # Draw ball
    pygame.draw.circle(screen, BALL_COLOR, ball_pos.astype(int), BALL_RADIUS)
    
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
