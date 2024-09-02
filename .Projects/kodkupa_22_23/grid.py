import sys
sys.setrecursionlimit(10000)
"""
def is_valid(grid, row, col, color):
    # Check if the adjacent cells have the same color
    directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
    for dr, dc in directions:
        new_row, new_col = row + dr, col + dc
        if 0 <= new_row < len(grid) and 0 <= new_col < len(grid[0]) and grid[new_row][new_col] == color:
            return False
    return True

def backtrack(grid, counts, n, m):
    # Base case: if counts are all zero, then the solution is found
    if all(count == 0 for count in counts):
        return True
    
    for row in range(n):
        for col in range(m):
            if grid[row][col] == 0:
                for color in range(1, 4):
                    if counts[color - 1] > 0 and is_valid(grid, row, col, color):
                        grid[row][col] = color
                        counts[color - 1] -= 1
                        if backtrack(grid, counts, n, m):
                            return True
                        grid[row][col] = 0
                        counts[color - 1] += 1
                return False
    return False

def is_possible(n, m, counts):
    # Initialize an empty grid
    grid = [[0] * m for _ in range(n)]
    if backtrack(grid, counts, n, m):
        return grid
    else:
        return None

n, m, r, g, b = map(int, input().split())
counts = [r, g, b]

result = is_possible(n, m, counts)

if result:
    print("YES")
    for row in range(n):
        print("".join(["RGB"[result[row][col] - 1] for col in range(m)]))
    
else:
    print("NO")
"""
def is_possible(r, g, b, M):
    def backtrack(curr, r, g, b):
        if curr == M:
            return True

        if r > 0 and (curr == 0 or colors[-1] != 'R'):
            curr_color = 'R'
            if backtrack(curr + 1, r - 1, g, b):
                colors.append(curr_color)
                return True

        if g > 0 and (curr == 0 or colors[-1] != 'G'):
            curr_color = 'G'
            if backtrack(curr + 1, r, g - 1, b):
                colors.append(curr_color)
                return True

        if b > 0 and (curr == 0 or colors[-1] != 'B'):
            curr_color = 'B'
            if backtrack(curr + 1, r, g, b - 1):
                colors.append(curr_color)
                return True

        return False

    colors = []
    if backtrack(0, r, g, b):
        return colors
    else:
        return None

# Example usage:
N, M, r_, g_, b_ = map(int, input().split())

result = is_possible(r_, g_, b_, M)
if result:
    print(f"Possible arrangement: {result}")
else:
    print("Not possible.")