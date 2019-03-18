lines = open('input.txt', 'r').read().strip().split('\n')
width = len(lines[0].strip())
height = len(lines)
grid = {}
for y in range(height):
    for x in range(width):
        grid[(x, y)] = lines[y][x] == '#'
for i in range(100):
    new_grid = {}
    for y in range(height):
        for x in range(width):
            n = 0
            for dy in range(max(0, y - 1), min(height, y + 2)):
                for dx in range(max(0, x - 1), min(width, x + 2)):
                    if dx == x and dy == y:
                        continue
                    if grid[(dx, dy)]:
                        n += 1
            if grid[(x, y)]:
                new_grid[(x, y)] = 2 <= n <= 3
            else:
                new_grid[(x, y)] = n == 3
    grid = new_grid
print('After 100 iterations, {} lights are on.'.format(sum(1 for light in 
    grid.values() if light)))
for y in range(height):
    for x in range(width):
        grid[(x, y)] = lines[y][x] == '#'
grid[(0, 0)] = grid[(width - 1, 0)] = grid[(width -1, height - 1)] = \
        grid[(0, height - 1)] = True
for i in range(100):
    new_grid = {}
    for y in range(height):
        for x in range(width):
            n = 0
            for dy in range(max(0, y - 1), min(height, y + 2)):
                for dx in range(max(0, x - 1), min(width, x + 2)):
                    if dx == x and dy == y:
                        continue
                    if grid[(dx, dy)]:
                        n += 1
            if grid[(x, y)]:
                new_grid[(x, y)] = 2 <= n <= 3
            else:
                new_grid[(x, y)] = n == 3
    grid = new_grid
    grid[(0, 0)] = grid[(width - 1, 0)] = grid[(width -1, height - 1)] = \
            grid[(0, height - 1)] = True
print('After 100 iterations in the actual grid, {} lights are on.'.format(
    sum(1 for light in grid.values() if light)))
