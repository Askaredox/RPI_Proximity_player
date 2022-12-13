from time import time
from vidplayer import VidPlayer


GPIO_PIN_DEFAULT = (26, 19, 13, 6, 5)


if __name__ == '__main__':
    vid = VidPlayer(videos=['videos/1.mp4','videos/2.mp4','videos/3.mp4','videos/4.mp4','videos/5.mp4'])
    now = time()
    future = now + 10
    i = 0
    while True:
        now = time()
        if(future < now):
            future = now + 10
            vid.switch_vid(GPIO_PIN_DEFAULT[i])
            i = i + 1 if i < 5 else 0