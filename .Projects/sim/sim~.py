import screener
from screener import *
import numpy as np
from math import ceil, sqrt
import random
import os
import colorama
from numba import njit

# --- Simulation Parameters ---
WIDTH = 60
HEIGHT = 30
NUM_PARTICLES = 1500
BOULDER_SIZE = (5, 5)
BOULDER_START_Y = 25
KERNEL_RADIUS = 2.0
REST_DENSITY = 4.0
STIFFNESS = 0.05
VISCOSITY = 0.01
DT = 0.016
GRAVITY = np.array([0, -0.5]) * DT
BOULDER_SPEED_X = 0.0 * DT  # Horizontal speed (set to 0 for now)
BOULDER_SPEED_Y = -1.0 * DT # Vertical speed (negative for downward)
SOLVER_ITERATIONS = 3
MAX_NEIGHBORS_PER_CELL = 30

# --- Grid for Neighbor Search ---
CELL_SIZE = KERNEL_RADIUS
GRID_WIDTH = int(WIDTH / CELL_SIZE)
GRID_HEIGHT = int(HEIGHT / CELL_SIZE)

@njit
def hash_position(pos):
    return int(pos[0] / CELL_SIZE) + int(pos[1] / CELL_SIZE) * GRID_WIDTH

@njit
def build_grid(positions):
    grid = np.empty((GRID_WIDTH * GRID_HEIGHT, MAX_NEIGHBORS_PER_CELL), dtype=np.int64)
    grid_counts = np.zeros(GRID_WIDTH * GRID_HEIGHT, dtype=np.int64)

    for i in range(positions.shape[0]):
        index = hash_position(positions[i])
        if 0 <= index < GRID_WIDTH * GRID_HEIGHT:
            count = grid_counts[index]
            if count < MAX_NEIGHBORS_PER_CELL:
                grid[index, count] = i
                grid_counts[index] += 1
    return grid, grid_counts

@njit
def get_neighbors(pos, grid, grid_counts):
    cell_x = int(pos[0] / CELL_SIZE)
    cell_y = int(pos[1] / CELL_SIZE)
    neighbors = []
    for i in range(max(0, cell_x - 1), min(GRID_WIDTH, cell_x + 2)):
        for j in range(max(0, cell_y - 1), min(GRID_HEIGHT, cell_y + 2)):
            index = i + j * GRID_WIDTH
            if 0 <= index < GRID_WIDTH * GRID_HEIGHT:
                count = grid_counts[index]
                for k in range(count):
                    neighbors.append(grid[index, k])
    return neighbors

# --- Kernels ---

@njit
def poly6_kernel(r_squared, h):
    if 0 <= r_squared <= h**2:
        return (315 / (64 * np.pi * h**9)) * (h**2 - r_squared)**3
    return 0

@njit
def spiky_kernel_gradient(r, h):
    r_len = np.linalg.norm(r)
    if 0 <= r_len <= h:
        return (15 / (np.pi * h**6)) * (h - r_len)**2 * (r / (r_len + 1e-6))
    return np.zeros_like(r)

@njit
def viscosity_kernel_laplacian(r_squared, h):
    r = np.sqrt(r_squared)
    if 0 <= r <= h:
        return (45/(np.pi * h**6)) * (h - r)
    return 0

# --- Boundary Handling ---

@njit
def constrain_to_bounds(pos):
    x, y = pos
    x = max(1, min(x, WIDTH - 2))
    y = max(1, min(y, HEIGHT - 2))
    return np.array([x, y])

# --- Boulder Movement (Corrected: Move Down) ---

@njit
def move_boulder(boulder, speed_x, speed_y):
    new_boulder = boulder + np.array([speed_x, speed_y])
    # Boundary checks (prevent boulder from leaving the screen)
    if np.any(new_boulder[:, 0] < 0) or np.any(new_boulder[:, 0] >= WIDTH) or \
       np.any(new_boulder[:, 1] < 0) or np.any(new_boulder[:, 1] >= HEIGHT):
        return boulder  # Don't move if out of bounds
    return new_boulder

# --- Rendering ---

def render(field_map, positions, boulder, dot_char='¤'):
    field_map.fill()
    for x, y in positions.astype(int):
        if 0 <= x < field_map.width and 0 <= y < field_map.height:
            field_map[x, y] = dot_char
    for x, y in boulder.astype(int):
        if 0 <= x < field_map.width and 0 <= y < field_map.height:
            field_map[x, y] = "@"
    return field_map

# --- Core Simulation Logic ---

@njit
def calculate_density(predicted_positions, grid, grid_counts):
    densities = np.zeros(NUM_PARTICLES)
    for i in range(NUM_PARTICLES):
        neighbors = get_neighbors(predicted_positions[i], grid, grid_counts)
        for j in neighbors:
            rij = predicted_positions[i] - predicted_positions[j]
            r2 = np.sum(rij * rij)
            densities[i] += poly6_kernel(r2, KERNEL_RADIUS)
    return densities

@njit
def apply_constraints(predicted_positions, densities, grid, grid_counts):
    for _ in range(SOLVER_ITERATIONS):
        for i in range(NUM_PARTICLES):
            neighbors = get_neighbors(predicted_positions[i], grid, grid_counts)
            for j in neighbors:
                if i != j:
                    rij = predicted_positions[i] - predicted_positions[j]
                    r2 = np.sum(rij * rij)
                    if r2 < KERNEL_RADIUS * KERNEL_RADIUS:
                        pressure_i = max(-0.5, min(0.5, STIFFNESS * (densities[i] / REST_DENSITY - 1)))
                        pressure_j = max(-0.5, min(0.5, STIFFNESS * (densities[j] / REST_DENSITY - 1)))
                        D = 0.5 * (pressure_i + pressure_j) * spiky_kernel_gradient(rij, KERNEL_RADIUS)
                        predicted_positions[i] += D * DT * DT
                        predicted_positions[j] -= D * DT * DT
    return predicted_positions

@njit
def apply_viscosity(predicted_positions, velocities, grid, grid_counts):
    for i in range(NUM_PARTICLES):
        neighbors = get_neighbors(predicted_positions[i], grid, grid_counts)
        for j in neighbors:
            if i != j:
                rij = predicted_positions[i] - predicted_positions[j]
                r2 = np.sum(rij * rij)
                if r2 < KERNEL_RADIUS * KERNEL_RADIUS:
                    v_ij = velocities[i] - velocities[j]
                    I = DT * VISCOSITY * viscosity_kernel_laplacian(r2, KERNEL_RADIUS) * v_ij
                    velocities[i] -= I
                    velocities[j] += I
    return velocities

@njit
def apply_collisions(positions, velocities, boulder):
    for i in range(NUM_PARTICLES):
        # Boulder collision
        for b_pos in boulder:
            dist = np.linalg.norm(positions[i] - b_pos)
            if dist < 1.5:
                direction = (positions[i] - b_pos) / (dist + 1e-6)
                positions[i] = b_pos + direction * 1.5
                velocities[i] = np.zeros(2)

        # Boundary collision
        new_pos = constrain_to_bounds(positions[i])
        if not np.array_equal(positions[i], new_pos):
            positions[i] = new_pos
            velocities[i] = np.zeros(2)
    return positions, velocities

@njit
def simulate_step(positions, velocities, boulder):
    # 1. Apply external forces
    velocities += GRAVITY

    # 2. Move boulder (downward)
    boulder = move_boulder(boulder, BOULDER_SPEED_X, BOULDER_SPEED_Y)

    # 3. Predict positions
    predicted_positions = positions + velocities * DT

    # 4. Build spatial grid
    grid, grid_counts = build_grid(predicted_positions)

    # 5. Calculate density
    densities = calculate_density(predicted_positions, grid, grid_counts)

    # 6. Apply constraints
    predicted_positions = apply_constraints(predicted_positions, densities, grid, grid_counts)

    # 7. Apply viscosity
    velocities = apply_viscosity(predicted_positions, velocities, grid, grid_counts)

    # 8. Update velocities
    velocities = (predicted_positions - positions) / DT

    # 9. Update positions
    positions = predicted_positions

    # 10. Apply collisions
    positions, velocities = apply_collisions(positions, velocities, boulder)

    return positions, velocities, boulder

def simulate(field_map, terminal_display):
    positions = np.random.rand(NUM_PARTICLES, 2) * [WIDTH - 4, HEIGHT - 4] + [2, 2]
    velocities = np.zeros((NUM_PARTICLES, 2))
    boulder = np.array([[i, j + BOULDER_START_Y] for i in range(BOULDER_SIZE[0]) for j in range(BOULDER_SIZE[1])], dtype=np.float64)

    while True:
        positions, velocities, boulder = simulate_step(positions, velocities, boulder)
        render(field_map, positions, boulder)
        terminal_display.update(field_map, fps=1 / DT)

if __name__ == "__main__":
    screener.GLOBAL_last_frame_time = 0
    field_map = CharacterMap(WIDTH, HEIGHT, filler='.')
    terminal_display = TerminalDisplay(field_map.height)
    os.system('cls')
    colorama.init()
    simulate(field_map, terminal_display)