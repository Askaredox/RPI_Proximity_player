import os
import signal
from threading import Lock
from typing import List
from subprocess import Popen, PIPE, call


class VidPlayer:
    __GPIO_PIN_DEFAULT = (26, 19, 13, 6, 5)

    # The process of the active video player
    __p:Popen = None

    # The currently playing video filename
    __active_vid:str = None

    # Use this lock to avoid multiple button presses updating the player
    __mutex:Lock = Lock()

    __audio:str = 'hdmi'


    def __init__(self, videos:list=None, gpio_pins:tuple=None, loop:bool=True, debug:bool=False):
        self.gpio_pins = self.__GPIO_PIN_DEFAULT if gpio_pins is None else gpio_pins

        if videos:
            self.videos = videos
            for video in videos:
                if not os.path.exists(video):
                    raise FileNotFoundError('Video "{}" not found'.format(video))

        self.loop = loop
        self.debug = debug


    def switch_vid(self, pin:int):
        with self.__mutex:
            filename = self.videos[self.gpio_pins.index(pin)]
            if filename != self.__active_vid:
                self.__kill_process()

                cmd = ['omxplayer', '-b', '-o', self.__audio, ]
                if self.loop:
                    cmd += ['--loop']
                cmd += [filename]
                stdout = None if self.debug else PIPE

                self.__p = Popen(cmd, stdout=stdout, preexec_fn=os.setsid)
                self.__active_vid = filename


    def __kill_process(self):
        """ Kill a video player process. SIGINT seems to work best. """
        if self.__p is not None:
            os.killpg(os.getpgid(self.__p.pid), signal.SIGINT)
            self.__p = None