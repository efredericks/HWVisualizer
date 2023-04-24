# https://www.henryschmale.org/2021/01/07/pygame-linein-audio-viz.html
import pygame
import numpy as np
import os
import random
import time
# import pyaudio
import math

import opensimplex
import numba as nb
# from pixelsort import pixelsort

# display
# SCR_WIDTH = 800
# SCR_HEIGHT = 600
SCR_WIDTH = 1920
SCR_HEIGHT = 1080

# NOAA data
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


# def getNoise(x, y, z, multX=0.01, multY=0.01, multZ=0.01) -> float:
#   return opensimplex.noise3(x=x*multX, y=y*multY, z=z*multZ)


# calculate noise
# @nb.njit(parallel=True, fastmath=True)
# def updateNoise():
    # (float)noise.eval(scl * x, scl * y, R * cos(TWO_PI * t), R * sin(TWO_PI * t));
    # z = 0
    # for t in range(0, math.pi * 2.0, 0.1):
    #     pixels[x,y,z] = opensimplex.noise4()
    #     z += 1
    


    # _pixels = np.zeros((SCR_WIDTH,SCR_HEIGHT), 3)
    # for y in range(SCR_HEIGHT-1):
    #     for x in range(SCR_WIDTH-1):
    #         n = getNoise(x,y,z)
    #         pixels[x,y,z] = n
            # (
            #     int(p5map(n, 0.0, 1.0, 0, 255)),
            #     0,
            #     255
            # )
    # return _pixels


# constrain value to range
def constrain(val, min_val, max_val):
    return min(max_val, max(min_val, val))

# pixels = np.zeros((SCR_WIDTH,SCR_HEIGHT, 3))
# pixels = np.zeros((SCR_WIDTH,SCR_HEIGHT,)*3)
# z = 0
# updateNoise(z)
# npsurf = pygame.surfarray.make_surface(pixels)

# x_pixels = np.arange(0,SCR_WIDTH)
# y_pixels = np.arange(0,SCR_HEIGHT)
# pixels = opensimplex.noise2array(y_pixels, x_pixels)
# for yp in pixels:
#     for xp in yp:
#         xp = (int(p5map(xp, 0.0, 1.0, 0, 255)),0,255)



# noaa_url = "https://coastwatch.pfeg.noaa.gov/erddap/tabledap/pmelTaoDySst.json?longitude,latitude,time,station,wmo_platform_code,T_25&time%3E={0}&time%3C={1}".format(prior, today)#2015-05-31T12:00:00Z"
# data = json.loads(requests.get(noaa_url).text)


# pprint.pprint(data["table"])
# print(datetime.utcnow().isoformat() + "Z")



# audio
# AUDIO_RATE = 44100
# CHUNKS_PER_SECOND = 60
# CHUNK = int(1 / CHUNKS_PER_SECOND) * AUDIO_RATE
# FORMAT = pyaudio.paInt16
# pstream = pyaudio.PyAudio()
# stream = pstream.open(format=FORMAT,
#   channels=1, rate=AUDIO_RATE, input=True, frames_per_buffer=CHUNK)



# songs = ["ai.mp3", "smoke-143172.mp3"]

if __name__ == "__main__":
    pygame.init()

    pygame.display.set_caption("HWVisualizer")

    display = pygame.display.set_mode((SCR_WIDTH, SCR_HEIGHT))#, pygame.FULLSCREEN)
    display.fill((20,20, 20))

    clock = pygame.time.Clock()

    all_black = np.zeros((SCR_WIDTH, SCR_HEIGHT))
    background_surf = pygame.surfarray.make_surface(all_black)
    display.blit(background_surf, (0, 0))

    # audio = pygame.mixer.Sound(songs[0])
    # RATE = 44100
    # CHUNK = int((1/30) * RATE)
    # FORMAT = pyaudio.paInt16
    # CHUNK_WIDTH = int(SCR_WIDTH / CHUNK)

    # print (CHUNK)

    # p = pyaudio.PyAudio()

    # stream = p.open(format=FORMAT,
    #     channels=1,
    #     rate=RATE,
    #     input=True,
    #     frames_per_buffer=CHUNK)

    # CHUNKS = 60
    # CHUNK_WIDTH = SCR_WIDTH // CHUNKS

    done = False
    col = 0
    updated = False

    # wolfram
    w = 10
    h = (SCR_HEIGHT // w) + 1
    generation = 0
    num_cells = (SCR_WIDTH // w) + 1
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

    r_col = 255
    g_col = 0
    b_col = 255
    a_col = 20
    main_col = (r_col, g_col, b_col, a_col)

    paused = False


    while not done:
        dt = clock.tick(60) / 1000.0
        pygame.display.set_caption(f"HWVisualizer - FPS:{clock.get_fps():4.0f}")

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True

            # press and release
            if event.type == pygame.KEYDOWN:
                updated = False
                if event.key == pygame.K_ESCAPE:
                    done = True
                if event.key == pygame.K_o:
                    pygame.image.save(display, "output.png")

                if event.key == pygame.K_p:
                    paused = not paused


        if not paused:
            # repeating keys
            keys = pygame.key.get_pressed()

#                if event.key == pygame.K_d:
#                    dither()

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
            print(main_col)


        #         if event.key == pygame.K_SPACE:
        #             balls = create_balls(n_balls)
        #         if event.key == pygame.K_UP:
        #             n_balls += 1
        #             balls = create_balls(n_balls)
        #         if event.key == pygame.K_DOWN:
        #             n_balls = max(1, n_balls-1)
        #             balls = create_balls(n_balls)

        # update_balls(balls, dt)
        # draw_balls(screen_arr, balls)

        # pygame.surfarray.blit_array(display, screen_arr)

            # wolfram
            for i in range(len(cells)):
                x = i * w
                y = generation * w
                drawRect = False
                if cells[i] == 1:
                    drawRect = True
                # pygame.draw.rect(display, col, (x, y, w, h))
                if drawRect:
                    draw_rect_alpha(display, main_col, pygame.Rect(x, y, w, h))


            cells, generation = WolframCAGenerate(cells, generation, ruleset)
            if generation >= h-1:
                generation = 0



        # noise
        # z = 0
        # updateNoise(z)

        # points = pixels.tolist()
        # _pixels = pixels.tolist()
        # for p in _pixels:
        #     for _p in p:
        #         _p = int(p5map(_p, 0.0, 1.0, 0, 255))
        # npsurf = pygame.surfarray.make_surface(pixels)
        # display.blit(npsurf, (0, 0))


        # n = opensimplex.noise2(x=c * multX, y=r * multY)

        # buff = stream.read(CHUNK)
        # data = np.frombuffer(buff, dtype=np.int16)
        # fft_complex = np.fft.fft(data, n=CHUNK)
        # #fft_distance = np.zeros(len(fft_complex))

        # display.fill((0,0,0))
        # color = (0,128,1)
        # s = 0
        # max_val = math.sqrt(max(v.real * v.real + v.imag * v.imag for v in fft_complex))
        # scale_value = SCR_HEIGHT / max_val
        # for i,v in enumerate(fft_complex):
        #     #v = complex(v.real / dist1, v.imag / dist1)
        #     dist = math.sqrt(v.real * v.real + v.imag * v.imag)
        #     mapped_dist = dist * scale_value
        #     s += mapped_dist
        
        #     #pygame.draw.line(display, color, (i, SCR_HEIGHT), (i, SCR_HEIGHT - mapped_dist))
        #     pygame.draw.rect(display, color, (i*CHUNK_WIDTH, SCR_HEIGHT-mapped_dist, CHUNK_WIDTH, mapped_dist))
        # print(s/len(fft_complex))



        # curr = np.full((1, SCR_HEIGHT), random.randint(0,255))
        # surf = pygame.surfarray.make_surface(curr)
        # col += 1
        # if col > SCR_WIDTH - 1: col = 0

        ## NOAA thing
        # if updated == False:
        #     display.fill((0,0,0))
        #     color = (0,128,1)
        #     temps = []
        #     x = 0
        #     for valC in data["table"]["rows"]:
        #         if valC[5] is not None:
        #           pygame.draw.rect(display, (255,0,255), (x, SCR_HEIGHT-int(valC[5]), CHUNK_WIDTH-2, int(valC[5])))
        #           x += CHUNK_WIDTH

            

        #     updated = True



        # display.blit(surf, (col, 0))
        pygame.display.update()
        # clock.tick(60)

    pygame.quit()
