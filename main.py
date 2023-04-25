# https://www.henryschmale.org/2021/01/07/pygame-linein-audio-viz.html
import pygame
import numpy as np
import random
import time
import math

import opensimplex
# from pixelsort import pixelsort

# display
SCR_WIDTH = 1920
SCR_HEIGHT = 1080

# NOAA data
# Visualizing data from the shoreline
"""
import requests
import json
import pprint
import datetime
# https://coastwatch.pfeg.noaa.gov/erddap/tabledap/pmelTaoDySst.mat?time,T_25&station="0n0e"&time>=2015-05-23T12:00:00Z&time<=2015-05-31T12:00:00Z
# noaa_url = "https://coastwatch.pfeg.noaa.gov/erddap/tabledap/pmelTaoDySst.json?longitude,latitude,time,station,wmo_platform_code,T_25&time%3E=2015-05-23T12:00:00Z&time%3C=2015-05-31T12:00:00Z"


today = datetime.datetime.utcnow()
prior = today - datetime.timedelta(days=60)

today = today.isoformat() + "Z"
prior = prior.isoformat() + "Z"

print(today, prior)

# noaa_url = "https://coastwatch.pfeg.noaa.gov/erddap/tabledap/pmelTaoDySst.json?longitude,latitude,time,station,wmo_platform_code,T_25&time%3E={0}&time%3C={1}".format(prior, today)#2015-05-31T12:00:00Z"
# data = json.loads(requests.get(noaa_url).text)


# pprint.pprint(data["table"])
# print(datetime.utcnow().isoformat() + "Z")
"""

def initCA():
    cells = [0 for _ in range(num_cells)]
    if random.random() > 0.5:
        cells[len(cells) // 2] = 1
    else:
        cells[random.randint(0,len(cells)-1)] = 1

    # standard wolfram rules
    # TBD param
    if random.random() > 0.5:
        ruleset = [0, 1, 0, 1, 1, 0, 1, 0]
    else:
        # random rules
        ruleset = []
        for _ in range(8):
            ruleset.append(random.choice([0, 1]))
    return cells, ruleset

def WolframCARules(a, b, c, ruleset):
    if a == 1 and b == 1 and c == 1: return ruleset[0]
    if a == 1 and b == 1 and c == 0: return ruleset[1]
    if a == 1 and b == 0 and c == 1: return ruleset[2]
    if a == 1 and b == 0 and c == 0: return ruleset[3]
    if a == 0 and b == 1 and c == 1: return ruleset[4]
    if a == 0 and b == 1 and c == 0: return ruleset[5]
    if a == 0 and b == 0 and c == 1: return ruleset[6]
    if a == 0 and b == 0 and c == 0: return ruleset[7]
    return 0


def WolframCAGenerate(cells, generation, ruleset):
    nextgen = [0 for _ in range(len(cells))]
    for i in range(1, len(cells) - 1):
        left = cells[i - 1]
        middle = cells[i]
        right = cells[i + 1]
        nextgen[i] = WolframCARules(left, middle, right, ruleset)
    #cells = nextgen
    generation += 1
    return nextgen, generation

# map function similar to p5.js
# @nb.njit(parallel=True, fastmath=True)
def p5map(n, start1, stop1, start2, stop2):
    return ((n - start1) / (stop1 - start1)) * (stop2 - start2) + start2

# https://stackoverflow.com/questions/6339057/draw-a-transparent-rectangles-and-polygons-in-pygame
def draw_rect_alpha(surf, col, rect):
    shape_surf = pygame.Surface(pygame.Rect(rect).size, pygame.SRCALPHA)
    pygame.draw.rect(shape_surf, col, shape_surf.get_rect())
    surf.blit(shape_surf, rect)

def draw_circ_alpha(surf, col, x, y, r):
    # shape_surf = pygame.Surface((SCR_WIDTH, SCR_HEIGHT), pygame.SRCALPHA)
    surf.set_alpha(col[3])
    rect = pygame.Rect(x, y, r*2, r*2)
    # shape_surf = pygame.Surface(rect.size, pygame.SRCALPHA)
    pygame.draw.circle(surf, col, (x, y), r)
    # surf.blit(shape_surf, rect)

def draw_ui(surf, font, col, active, refreshTimer, technique):
    op = "R[{0}] G[{1}] B[{2}] A[{3}], RT[{4}], T[{5}]".format(col[0], col[1], col[2], col[3], refreshTimer, technique)
    text_width, text_height = font.size(op)
    label = font.render(op, 1, (220, 220, 220))
    draw_rect_alpha(surf, (0,0,0), pygame.Rect(20,20,text_width, text_height))
    surf.blit(label, (20, 20))

# constrain value to range
def constrain(val, min_val, max_val):
    return min(max_val, max(min_val, val))

def makeNoiseField(noise_grid, multX, multY, t):
    for r in range(SCR_HEIGHT-1):#num_cells):
        for c in range(SCR_WIDTH-1):#num_cells):
            n = opensimplex.noise3(x=c*multX, y=r*multY, z=multY*random.randint(0,10000))
            val = p5map(n, -1.0, 1.0, 0.0, math.pi * 2.0)
            noise_grid[c,r] = val
    return noise_grid

import pygame.pixelcopy

# c/o https://github.com/pygame/pygame/issues/1244
def make_surface_rgba(array):
    """Returns a surface made from a [w, h, 4] numpy array with per-pixel alpha
    """
    shape = array.shape
    if len(shape) != 3 and shape[2] != 4:
        raise ValueError("Array not RGBA")

    # Create a surface the same width and height as array and with
    # per-pixel alpha.
    surface = pygame.Surface(shape[0:2], pygame.SRCALPHA, 32)

    # Copy the rgb part of array to the new surface.
    pygame.pixelcopy.array_to_surface(surface, array[:,:,0:3])

    # Copy the alpha part of array to the surface using a pixels-alpha
    # view of the surface.
    surface_alpha = np.array(surface.get_view('A'), copy=False)
    surface_alpha[:,:] = array[:,:,3]

    return surface

def generateParticles():
    particles = []
    num_particles = random.randint(50,150)
    for _ in range(num_particles):
        r = random.randint(1,15)
        particles.append({
            'x': random.randint(0,SCR_WIDTH-1),
            'y': random.randint(0,SCR_HEIGHT-1),
            'r': r,
            'r2': r/2,
            'c': (r_col, g_col, b_col, a_col)
        })
    return particles




if __name__ == "__main__":
    pygame.init()

    pygame.display.set_caption("HWVisualizer")

    display = pygame.display.set_mode((SCR_WIDTH, SCR_HEIGHT), pygame.HWSURFACE | pygame.DOUBLEBUF | pygame.FULLSCREEN)
    display.fill((20,20, 20))

    clock = pygame.time.Clock()

    opensimplex.seed(random.randint(0,100000))

    # store a black background for clearing
    all_black = np.zeros((SCR_WIDTH, SCR_HEIGHT))
    background_surf = pygame.surfarray.make_surface(all_black)
    display.blit(background_surf, (0, 0))

    # the 'main' drawing area
    main_surf = pygame.Surface(pygame.Rect((0,0,SCR_WIDTH, SCR_HEIGHT)).size, pygame.SRCALPHA)
    ui_surf = pygame.Surface(pygame.Rect((0,0,500,500)).size, pygame.SRCALPHA)

    font = pygame.font.SysFont("monospace", 14)

    done = False
    updated = False

    # wolfram
    w = 10
    h = (SCR_HEIGHT // w) + 1
    generation = 0
    num_cells = (SCR_WIDTH // w) + 1
    cells, ruleset = initCA()

    r_col = 255
    g_col = 0
    b_col = 255
    a_col = 10
    main_col = (r_col, g_col, b_col, a_col)

    refreshTimer = 0
    maxRefresh = 1000
    paused = False

    techniques = ["WolframCA", "NoiseField"]
    random.shuffle(techniques)
    activeTechnique = techniques[0]

    display.blit(background_surf, (0, 0))
    main_surf.blit(background_surf, (0, 0))

    multX = 0.001
    multY = 0.001
    noise_grid = np.zeros((SCR_WIDTH, SCR_HEIGHT, 1))#np.zeros((num_cells, num_cells))
    noise_grid = makeNoiseField(noise_grid, multX, multY, "flow")
    particles = generateParticles()

    # print(noise_grid)

    while not done:
        dt = clock.tick(60) / 1000.0
        refreshTimer += 1
        pygame.display.set_caption(f"HWVisualizer - FPS:{clock.get_fps():4.0f}")
        draw_ui(ui_surf, font, main_col, True, refreshTimer, activeTechnique)

        if refreshTimer >= maxRefresh:
            refreshTimer = 0
            r_col = random.randint(0,255)
            g_col = random.randint(0,255)
            b_col = random.randint(0,255)
            a_col = random.randint(10,80)

            if activeTechnique == "WolframCA":
                cells, ruleset = initCA()
            else:
                noise_grid = makeNoiseField(noise_grid, multX, multY, "flow")
                particles = generateParticles()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True

            # press and release
            if event.type == pygame.KEYDOWN:
                updated = False
                if event.key == pygame.K_ESCAPE:
                    done = True
                ## TBD: doesn't work with HWSURFACE
                if event.key == pygame.K_o:
                    pygame.image.save(main_surf, "output.png")

                if event.key == pygame.K_p:
                    paused = not paused

                if event.key  == pygame.K_0:
                    cells, ruleset = initCA()

                if event.key == pygame.K_b:
                    main_surf.blit(background_surf, (0, 0))

                if event.key == pygame.K_EQUALS:
                    refreshTimer = 0
                    r_col = random.randint(0,255)
                    g_col = random.randint(0,255)
                    b_col = random.randint(0,255)
                    a_col = random.randint(10,80)

                    random.shuffle(techniques)
                    activeTechnique = techniques[0]
                    if activeTechnique == "NoiseField":
                        noise_grid = makeNoiseField(noise_grid, multX, multY, "flow")
                        particles = generateParticles()



        if not paused:
            # repeating keys
            keys = pygame.key.get_pressed()

                # modify color?
            if keys[pygame.K_q]:
                r_col += 1
            if keys[pygame.K_a]:
                r_col -= 1
            if keys[pygame.K_w]:
                g_col += 1
            if keys[pygame.K_s]:
                g_col -= 1
            if keys[pygame.K_e]:
                b_col += 1
            if keys[pygame.K_d]:
                b_col -= 1
            if keys[pygame.K_r]:
                a_col += 1
            if keys[pygame.K_f]:
                a_col -= 1

            r_col = constrain(r_col, 0, 255)
            g_col = constrain(g_col, 0, 255)
            b_col = constrain(b_col, 0, 255)
            a_col = constrain(a_col, 0, 255)
            main_col = (r_col, g_col, b_col, a_col)

            if activeTechnique == "WolframCA":
                # wolfram
                for i in range(len(cells)):
                    x = i * w
                    y = generation * w
                    drawRect = False
                    if cells[i] == 1:
                        drawRect = True
                    # pygame.draw.rect(display, col, (x, y, w, h))
                    if drawRect:
                        draw_rect_alpha(main_surf, main_col, pygame.Rect(x, y, w, h))


                cells, generation = WolframCAGenerate(cells, generation, ruleset)
                if generation >= h-1:
                    generation = 0
            elif activeTechnique == "NoiseField":
                for p in particles:
                    p['c'] = main_col
                    # pygame.draw.circle(main_surf, p['c'], (p['x'], p['y']), p['r'])
                    draw_circ_alpha(main_surf, p['c'], p['x'], p['y'], p['r'])
                    
                    angle = noise_grid[int(p['x']), int(p['y'])]
                    p['x'] += p['r2'] * math.cos(angle)
                    p['y'] += p['r2'] * math.sin(angle)

                    if p['x'] < 0 or p['x'] > SCR_WIDTH-1 or p['y'] < 0 or p['y'] > SCR_HEIGHT-1:
                        p['x'] = random.randint(0,SCR_WIDTH-1)
                        p['y'] = random.randint(0,SCR_HEIGHT-1)
                # main_surf.blit(noise_surf, (0, 0))




        # blit surfaces to screen
        display.blit(main_surf, (0, 0))
        display.blit(ui_surf, (0, 0))

        pygame.display.update()

    pygame.quit()