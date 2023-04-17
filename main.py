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
SCR_WIDTH = 800#1920
SCR_HEIGHT = 600#1080

# NOAA data
import requests
import json
import pprint
import datetime
# https://coastwatch.pfeg.noaa.gov/erddap/tabledap/pmelTaoDySst.mat?time,T_25&station="0n0e"&time>=2015-05-23T12:00:00Z&time<=2015-05-31T12:00:00Z
# noaa_url = "https://coastwatch.pfeg.noaa.gov/erddap/tabledap/pmelTaoDySst.json?longitude,latitude,time,station,wmo_platform_code,T_25&time%3E=2015-05-23T12:00:00Z&time%3C=2015-05-31T12:00:00Z"

# https://github.com/Norne9/metaballs/blob/master/metaballs.py

today = datetime.datetime.utcnow()
prior = today - datetime.timedelta(days=60)

today = today.isoformat() + "Z"
prior = prior.isoformat() + "Z"

print(today, prior)

# map function similar to p5.js
# @nb.njit(parallel=True, fastmath=True)
def p5map(n, start1, stop1, start2, stop2):
    return ((n - start1) / (stop1 - start1)) * (stop2 - start2) + start2


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

### metaballs
CORES = os.cpu_count()
DEFAULT_N_BALLS = 6

def update_balls(balls: np.ndarray, dt: float):
    for b in range(balls.shape[0]):
        balls[b].pos += balls[b].vel * dt * 80.0

        # bounce
        screen = [SCR_WIDTH, SCR_HEIGHT]
        for axis in range(2):
            if balls[b].pos[axis] < balls[b].radius:
                balls[b].vel[axis] = np.abs(balls[b].vel[axis])
            elif balls[b].pos[axis] > screen[axis] - balls[b].radius:
                balls[b].vel[axis] = -np.abs(balls[b].vel[axis])

        # bounce from others
        for b2 in range(balls.shape[0]):
            if b2 == b:
                continue

            delta = balls[b].pos - balls[b2].pos
            dist2 = np.dot(delta, delta)
            rad2 = balls[b].radius + balls[b2].radius
            rad2 *= rad2

            if dist2 < rad2:
                balls[b].vel = delta / np.max(np.abs(delta))

@nb.njit(parallel=True, fastmath=True)
def draw_balls(screen: np.ndarray, balls: np.ndarray):
    w, h = screen.shape[0], screen.shape[1]
    b_count = balls.shape[0]

    # to use all cores
    for start in nb.prange(CORES):
        # for each pixel on screen
        for x in range(start, w, CORES):
            for y in range(h):
                screen[x, y].fill(0)  # clear pixel
                # for each ball
                for b in range(b_count):
                    # calculate value
                    dx, dy = balls[b].pos[0] - x, balls[b].pos[1] - y
                    light = balls[b].radius * balls[b].radius / (dx * dx + dy * dy)

                    # multiply value by ball color
                    for c in range(3):
                        screen[x, y, c] += balls[b].rgb[c] * light * 255.0

                # if color > max => normalize color
                max_color = screen[x, y].max()
                if max_color > 255:
                    screen[x, y] = screen[x, y] * 255 // max_color
                else:  # else => color = color * color / 2
                    screen[x, y] *= screen[x, y]
                    screen[x, y] //= 500


def create_balls(n_balls):
    """make random balls"""
    balls = np.recarray(
        (n_balls,), dtype=[("pos", ("<f4", (2,))), ("rgb", ("<f4", (3,))), ("radius", "f4"), ("vel", ("<f4", (2,)))],
    )
    for i in range(balls.shape[0]):
        # generate ball
        balls[i].radius = np.random.randint(5, 15) * 5
        balls[i].pos = (
            np.random.randint(balls[i].radius, SCR_WIDTH - balls[i].radius),
            np.random.randint(balls[i].radius, SCR_HEIGHT - balls[i].radius),
        )
        balls[i].rgb = np.random.rand(3)
        balls[i].rgb[i % 3] = 1
        balls[i].vel = np.random.rand(2)
        balls[i].vel = balls[i].vel / balls[i].vel.max()
    return balls

if __name__ == "__main__":
    pygame.init()

    pygame.display.set_caption("HWVisualizer")

    display = pygame.display.set_mode((SCR_WIDTH, SCR_HEIGHT))#, pygame.FULLSCREEN)
    display.fill((220,220, 220))

    clock = pygame.time.Clock()

    all_black = np.zeros((SCR_WIDTH, SCR_HEIGHT))
    background_surf = pygame.surfarray.make_surface(all_black)
    display.blit(background_surf, (0, 0))

    n_balls = DEFAULT_N_BALLS
    balls = create_balls(n_balls)
    screen_arr = np.zeros((SCR_WIDTH, SCR_HEIGHT, 3), dtype=np.int32)

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
    while not done:
        dt = clock.tick(60) / 1000.0
        pygame.display.set_caption(f"HWVisualizer - Balls: {n_balls}, FPS:{clock.get_fps():4.0f}")

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True

            if event.type == pygame.KEYDOWN:
                updated = False
                if event.key == pygame.K_ESCAPE:
                    done = True

                if event.key == pygame.K_SPACE:
                    balls = create_balls(n_balls)
                if event.key == pygame.K_UP:
                    n_balls += 1
                    balls = create_balls(n_balls)
                if event.key == pygame.K_DOWN:
                    n_balls = max(1, n_balls-1)
                    balls = create_balls(n_balls)

        update_balls(balls, dt)
        draw_balls(screen_arr, balls)
        pygame.surfarray.blit_array(display, screen_arr)



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
