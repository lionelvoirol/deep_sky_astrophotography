# -*- coding: utf-8 -*-
"""
Created on Wed Aug 22 12:10:36 2018

@author: Lionel Voirol
"""
#Install ffmpeg and ffmpy on anaconda via the anaconda command prompt
#conda install -c conda-forge ffmpeg
#pip install ffmpy

import os
os.chdir(r"C:\Users\Lionel Voirol\Documents\SUISSE 2015-17\STATISTICS_PROGRAMMING\Codes et support\Python_codes\astronomy\out")
os.getcwd()

#Return mp4 video from .jpeg images sequences
#Make sense of this fucking ffmepg bitch ass command

#Switch an image between jpeg and png
import ffmpy
ff=ffmpy.FFmpeg(
        inputs={'new_0.jpeg': None},
        outputs={'out.png' : None}
        )
ff.cmd
ffmpy.FFmpeg(ffmpeg -i new_0.jpeg out.png).run()
ff.run()


ff = ffmpy.FFmpeg(
inputs={'new_0%d.jpg': None},
outputs={'output.mp4': None})

ff.cmd
ff.run()





import subprocess

cmd = ['ffmpeg', '-i', 'new_%02d.jpg', 'output.mp4']
retcode = subprocess.call(cmd)
if not retcode == 0:
   raise ValueError('Error {} executing command: {}'.format(retcode, ' '.join(cmd)))    



#this works
import ffmpy
ff=ffmpy.FFmpeg(
        inputs={'new_%02d.jpg': None},
        outputs={'out.mp4' : None}
        )
ff.cmd
ff.run()


a=ffmpy.FFmpeg(ffmpeg -i new_%02d.jpg -vcodec libx264 -y movie.mp4)
ffmpeg 

ff=ffmpy.FFmpeg(
        inputs={'new_%02d.jpg': None},
        outputs={'out.mp4' : None}
        )
ff.run()


import subprocess
subprocess.call(['ffmpeg', '-i', 'new_%02d.jpg', 'output.avi'])








ff=ffmpy.FFmpeg(

ff.run(ffmpeg -framerate 1 -i new_%02d.jpg video.webm)

ff=ffmpy.FFmpeg(
        inputs={ffmpeg -i image-%03d.png video.webm})


ffmpy.FFmpeg(-i image-%03d.png video.webm)









import ffmpy #needs to be installed with pip command on anaconda prompt 'pip install ffmpy'
ffmpeg -framerate 2 -i new_%02d.jpg -c:v libx264 -profile:v high -crf 20 -pix_fmt Y output.mp4
ffmpeg -r 1 -i new_%02d.jpg -vcodec libx264 -y movie.mp4

ffmpeg -r 2 -f image2 -s 6140x4067 -i new_%02d.jpg -vcodec libx264 -crf 25  -pix_fmt yuv420p test.mp4

import ffmpy
from ffmpy import FFmpeg
FF

ffmpeg -framerate 1 -start_number 2 -i img%02d.png -c:v libx264 -r 30 -y out.mp4
