# -*- coding: utf-8 -*-


import numpy as np

"""
Created on Sun Aug 19 14:59:28 2018

@author: Lionel Voirol
"""
'''
Goal of the project:
    
    Given two pictures of the sky, one with white strides and one witouth white strides,
    superpose both such that these whites strides appears as derolling on the sky.
    Use the blank picture to fill in the space which are left empty while derolling the 
    whites strides (perseides)
    
    To be noted:
        Both picture are not totally aligned
        Both picture are not of the same light intensity (Different color)
    
Structure:
        Read both picture in a spyder console
        Identify in which pixels are the white strides
            Automatically or manually (with pixels coordinates)
                Extract Mouse click pixels coordinates
        Extract a border in pixel coordinates (x,y) and pixel values(r,g,b) around the line between these two pixels in the cover file
        Copy thes pixels in blank
        ...
        

'''
#Check & validate Working directory
import os
os.chdir(r"C:\Users\Lionel Voirol\Documents\SUISSE_2015-18\STATISTICS_PROGRAMMING\Codes et support\Python_codes\astronomy")
os.getcwd()

#Load both pictures
#Using the Pillow module in Python
from PIL import Image
blank = Image.open("blank.tif")
cover=Image.open("cover.tif")

#See image using Pillow module
blank.show() #Ouvre un fichier .bmp sur le programme par défaut défini sur ce type de fichier
cover.show()

#Image resolution
blank.size
cover.size #Image are not of the same size

#See image Using matplotlib 
#allow to inspect by pixels coordinates
import matplotlib.pyplot as plt
plt.imshow(blank)
plt.imshow(cover)

#Visually Checking the assumption of identical image 
#Relatively similar
cropped_blank = blank.crop((300,100,600,300))
cropped_blank.show()
cropped_cover = cover.crop((300,100,600,300))
cropped_cover.show()
#Image background is not exactly identical but very similar

#Detecting edges
#Manually or uses of CNN

#Manually
#Get mouse-click coordinates or identify via spyder viewer

#Load pixels values of both files
pix_cover=cover.load()
pix_blank=blank.load()

#inspect pix_cover
type(pix_cover) #PixelAccess module of PIL

#Using Bresenham algorithm to get pixels coordinates on a given trajectory
import bresenham #Needs to be installed via the anaconda command prompt with: python -m pip install bresenham
from bresenham import bresenham

#Get pixels values on cover and edit pixels values on blank
#Load pixels of cover

def capture_cover_pixels_values_on_trajectory(x1,y1,x2,y2,im_cover):
    '''
    (int,int,int,int,PILImage)-->tupple(list(int,int),list(int,int,int))
    
    return a tuple with two elements, first all the pixels coordinate extracted from a given trajectory (only positive values), one pixel line,
    second, their value in a three byte RGB format (i.e (0,0,0) or (255,255,255)), these pixels value extracted from a PIL image: im_cover
    '''
    import bresenham #Needs to be installed via the anaconda command prompt with: python -m pip install bresenham
    from bresenham import bresenham
    captured=list(bresenham(x1,y1,x2,y2))
    pos_list=[]
    for coor_list in captured:
        if all(i >= 1 for i in coor_list): #only positive pixels/pixels in the image
            pos_list.append(coor_list)
    pix=im_cover.load()
    pix_values=[]
    for coor in pos_list:
        pix_values.append(pix[coor])
    return pos_list,pix_values


def compare_pixels_value(pix_coor_value, im_cover, im_blank):
    '''
    (list, PILImage, PILImage)-->(Boolean)
    pix_coor_value a tupple with with two elements, first all the pixels coordinate extracted from a given trajectory,
    second, their value in a three byte RGB format (i.e (0,0,0) or (255,255,255))
    return True if all pixels on trajectory are identical
    return false if at least one pixels is different
    '''
    pix_cover=im_cover.load()
    pix_blank=im_blank.load()
    for j in range(len(pix_coor_value[0])):
            if (pix_blank[pix_coor_value[0][j]]!=pix_cover[pix_coor_value[0][j]]):
                return False
                break
    else:
        return True


def extract_pixels(x1,y1,x2,y2,width,im_cover):
    '''
    (int,int,int,int,int)-->tuple(list,list)
    Given 4 coordinates based on 2 points and a cover image, extract pixels from PILImage on a certain witdth value
    with equal distance on both side of the one pixel line which join these 2 points (x1,y1),(x2,y2)
    return a tupple with list of coor and value of coor
    '''
    pix_coor=[]
    pix_val=[]
    half_int=round(width/2)
    y1_val=y1
    y2_val=y2
    
    #Start by goin up on the picture
    while (y1_val>=y1-half_int):
        pix_coor=pix_coor+capture_cover_pixels_values_on_trajectory(x1, y1_val, x2, y2_val,im_cover)[0]
        pix_val=pix_val+capture_cover_pixels_values_on_trajectory(x1, y1_val, x2, y2_val,im_cover)[1]
        y1_val=y1_val-1
        y2_val=y2_val-1
    #Then go down
    #Reattribute y values
    y1_val=y1
    y2_val=y2
    #Go Down on the picture
    while (y1_val<=y1+half_int):
        pix_coor=pix_coor+capture_cover_pixels_values_on_trajectory(x1, y1_val, x2, y2_val,im_cover)[0]
        pix_val=pix_val+capture_cover_pixels_values_on_trajectory(x1, y1_val, x2, y2_val,im_cover)[1]
        y1_val=y1_val+1
        y2_val=y2_val+1
    return (pix_coor,pix_val)

#Copy pixels of cover on blank 

def replace_pixels_on_blank(pix_coor_value, im_blank):
    '''
    tupple(list(int,int),list(int,int,int)) --> NoneType
    Given a tupple with 2 lists, the pixels coordinates and the pixels values,
    modify the im_blank PILImage entered by replacing these pixels on im_blank by their values on cover.tif
    '''
    for i in range(len(pix_coor_value[0])):
        pos=pix_coor_value[0][i]
        val=pix_coor_value[1][i]
        pix_blank=im_blank.load()
        pix_blank[pos]=val



#Enter manually all shooting stars coordinates
shoot_star_coor_list=[]
shoot_star_coor_list.append([143,2566,557,2835])
shoot_star_coor_list.append([1178,2921,1580,2455])
shoot_star_coor_list.append([1229,3122,1787,2486])
shoot_star_coor_list.append([1299,3406,1855,2777])
shoot_star_coor_list.append([2230, 510, 2817, 160])
shoot_star_coor_list.append([2028,1935,2460,1438])
shoot_star_coor_list.append([2511,2046,3179,1292])
shoot_star_coor_list.append([2446,3287,2975,3379])
shoot_star_coor_list.append([2518,3107,2790,2695])
shoot_star_coor_list.append([2767,3250,3033,2844])
shoot_star_coor_list.append([2596,2792,3045,2359])
shoot_star_coor_list.append([2965,2967,3624,2329])
shoot_star_coor_list.append([3003,824,3528,228]) #most visible
shoot_star_coor_list.append([3341,2394,3647,1934])
shoot_star_coor_list.append([3546,1884,4069,1401])
shoot_star_coor_list.append([4660,860,5279,301])
shoot_star_coor_list.append([5439,3560,5778,3056])
shoot_star_coor_list.append([5480,3319,6050,2954])
len(shoot_star_coor_list)

shoot_star_coor_list[12] #is the most visible

#Now we want to deroll the pixels_value on a given rate
def angle(x1,y1,x2,y2):  
    '''
    (int,int,int,int)-->float
    return the angle in degree of a trajectory given two points (x1,y1), (x2,y2)
    a straight horizontal line is considered a the 0 degree and always going from left to right
    Pour le quadrant 12h à 3h, l'angle est % ligne horizontal à 3h.
    Pour le quadrant 3h-6h, l'angle est par rapport à l'axe vertical depuis 6h.
    All trigonometric function works in radians in Python
    '''
    import math
    op=y1-y2
    adj=x2-x1
    ratio=op/adj
    angle=math.degrees(math.atan(ratio))
    return angle

def euclidean(x1,y1,x2,y2):
    '''
    (int,int,int,int)-->(float)
    return the euclidean distance between 2 points in a cartesian space
    '''
    import math
    if (y1<y2): 
        dist_x=x2-x1
        dist_y=y2-y1
    elif (y1>=y2):
        dist_x=x2-x1
        dist_y=y1-y2
    return math.sqrt(dist_x**2+dist_y**2)

def loop_points_on_trajectory(x1,y1,x2,y2,steps):
    '''
    (int,int,int,int,int,int)-->(list(int,int))
    Return coordinates at a given a certain number of step and 2 coordinates
    '''
    #angle(x1,y1,x2,y2)
    import math
    ang_degree=angle(x1,y1,x2,y2)
    ang=math.radians(ang_degree)
    ini_x=x1
    ini_y=y1
    total_dist=euclidean(x1,y1,x2,y2)
    step_size=total_dist/steps
    coor_list=[[x1,y1]]
    #If upward line
    if (y2<y1):
        while(ini_x<=x2): 
            delta_y=math.sin(ang)*(step_size)
            delta_x=math.cos(ang)*(step_size)
            ini_x=ini_x+delta_x
            ini_y=ini_y-delta_y
            coor_list.append([int(ini_x),int(ini_y)])
        return coor_list
    elif (y2>=y1):
        ang_to_consider=math.radians(90+ang_degree)
        while(ini_x<=x2):
            delta_y=math.cos(ang_to_consider)*step_size
            delta_x=math.sin(ang_to_consider)*step_size
            ini_x=ini_x+delta_x
            ini_y=ini_y+delta_y
            coor_list.append([int(ini_x),int(ini_y)])
        return coor_list
        
def save_images(x1,y1,x2,y2,steps,input_file,out_file,start, width): #initial function
    '''
    (int,int,int,int,int,PIlImage, PILImaint)-->Jpeg file on wd
    Store in WD directory Jpeg file where the lines specified are simultaneously growing
    the argument steps indicate in how many iteration we want the full line to be drawed on the blank image
    it's not exactly the number of saved image but rather similar (i.e +-2)
    '''
    
    list_of_coor=loop_points_on_trajectory(x1,y1,x2,y2,steps)
    for pos in range(len(list_of_coor)):
        index=1+pos+start
        target_x=list_of_coor[pos][0]
        target_y=list_of_coor[pos][1]
        pixels_to_input=extract_pixels(x1,y1,target_x,target_y,width, input_file)
        replace_pixels_on_blank(pixels_to_input, out_file)
        name=str('new_'+str(index)+'.jpeg')
        out_file.save(name)
    return index


def generate_image_for_all_traj_back_n_forth(list_of_traj, step, width):
    '''
    Given a list of shooting stars
    '''
    #Sort list according to direction left to right
    blank = Image.open("blank.tif" ) #reload image
    blank_copy=blank.copy()
    list_of_traj.sort(key=lambda x: x[0]) #Sorting the list make sure shooting stars always go from left to right
    final_count=0
    for trajectory in list_of_traj:
        x1,y1,x2,y2 = trajectory[0],trajectory[1],trajectory[2],trajectory[3]
        step_entered=step
        list_of_coor=loop_points_on_trajectory(x1,y1,x2,y2,step_entered)
        count=save_images(x1,y1,x2,y2,step_entered,cover,blank,final_count, width) #Dessine de cover a blank
        final_count=save_images(x1,y1,x2,y2,step_entered,blank_copy,blank,count,width) #Efface la trajectoire de blank_copy a blank
    print('Total images stored: ' + str(final_count))

generate_image_for_all_traj_back_n_forth(shoot_star_coor_list,5,40)


#Export in mp4
'''
Install ffmpeg on anaconda via the anaconda command prompt
    conda install -c conda-forge ffmpeg

Ouvrir la cmd line
selectionner un dossier output avec SEULEMENT les images produites dessus
    cd your_path
installer ffmpeg avec la commande pip
    entrer la commande suivante:
        'pip install ffmppeg'
Transformer les images .jpeg en video .avi
    Entrer la commande suivante: 
        'ffmpeg -f image2 -r 5 -i new_%d.jpeg -vcodec mpeg4 -b 800k video.avi'
'''







###############################################################################################################
#Codes part which are finally not used
import ffmpy #needs to be installed with pip command on anaconda prompt 'pip install ffmpy'

def save_images_run_n_back(x1,y1,x2,y2,steps,start): #copy of function made such that after fully unroll, the traj reroll on itsefl
    '''
    (int,int,int,int,int,int)-->Jpeg file on wd
    Store in WD directory Jpeg file where the lines specified are simultaneously growing and then disapearing
    the argument steps indicate in how many iteration we want the full line to be drawed on the blank image
    it's not exactly the number of saved image but rather similar (i.e +-2)
    '''
    blank = Image.open("blank.tif")
    blank_copy=blank.copy() #Create a copy
    list_of_coor=loop_points_on_trajectory(x1,y1,x2,y2,steps)
    for pos in range(len(list_of_coor)):
        index=pos+start
        target_x=list_of_coor[pos][0]
        target_y=list_of_coor[pos][1]
        pixels_to_input=extract_pixels(x1,y1,target_x,target_y,50, cover)
        replace_pixels_on_blank(pixels_to_input, blank)
        name=str('new_'+str(index)+'.jpeg')
        blank.save(name)
    stored=index
        #Start of the second part of the function
        #Reroll the initial pixels
    for pos in range(len(list_of_coor)):
        target_x=list_of_coor[pos][0]
        target_y=list_of_coor[pos][1]
        pixels_to_input_afteward=extract_pixels(a,b,target_x,target_y,50, blank_copy)
        replace_pixels_on_blank(pixels_to_input_afteward, blank)
        name=str('new_'+str(stored+pos+1)+'.jpeg')
        blank.save(name)  



def generate_image_for_all_traj(list_of_traj, step):
    '''
    Given a list of shooting stars
    '''
    #Sort list according to direction left to right
    blank = Image.open("blank.tif" ) #reload image
    list_of_traj.sort(key=lambda x: x[0]) #Sorting the list make sure shooting stars always go from left to right
    stored=0 #at which image are we
    for trajectory in list_of_traj:
        x1,y1,x2,y2 = trajectory[0],trajectory[1],trajectory[2],trajectory[3]
        step_entered=step
        list_of_coor=loop_points_on_trajectory(x1,y1,x2,y2,step_entered)
        for pos in range(len(list_of_coor)):
            index=stored+pos+1  #
            target_x=list_of_coor[pos][0]
            target_y=list_of_coor[pos][1]
            pixels_to_input=extract_pixels(x1,y1,target_x,target_y,50, cover)
            replace_pixels_on_blank(pixels_to_input, blank)
            name=str('new_'+str(index)+'.jpeg')
            blank.save(name)
        stored=index 




plt.imshow(cover.crop((1,20,300,40)))

def rotate_picture_2_coordinates(x1,y1,x2,y2,im):
    '''
    int-->float
    Given the coordinates of 2 data points, return the picture of
    the initial image rotated such that its horizontal to the trajectory of the comet'''
    import math
    op=y2-y1
    adj=x2-x1
    ratio=op/adj
    angle=math.degrees(math.atan(ratio))
    return im.rotate(angle)

x1,y1,x2,y2=2235,507, 2817,161
angle(x1,y1,x2,y2)
rot=rotate_picture_2_coordinates(2235,507, 2817,161,cover)
plt.imshow(rot)




cover_shape=cover.size
x_center=cover_shape[0]/2
y_center=cover_shape[1]/2

def rotate_coordinates(origin, point, angle_in_degree):
    """
    Rotate a point counterclockwise by a given angle around a given origin.

    The angle should be given in radians.
    
    """
    import numpy as np
    import math
    angle=math.radians(angle_in_degree)
    ox, oy = origin
    px, py = point

    qx = ox + math.cos(angle) * (px - ox) - math.sin(angle) * (py - oy)
    qy = oy + math.sin(angle) * (px - ox) + math.cos(angle) * (py - oy)
    return qx, qy

coor_1=rotate_coordinates((x_center,y_center), (2235,507), 30.731556062626673)
coor_1
coor_2=rotate_coordinates((x_center,y_center), (2817,161), 30.731556062626673)
coor_2


plt.imshow((rot.crop((3107,200,1200,4000))))
plt.imshow(rot)





import numpy as np
def rotate_coordinates(origin, point, angle):
    """
    Rotate a point counterclockwise by a given angle around a given origin.

    The angle should be given in radians.
    """
    ox, oy = origin
    px, py = point

    qx = ox + math.cos(angle) * (px - ox) - math.sin(angle) * (py - oy)
    qy = oy + math.sin(angle) * (px - ox) + math.cos(angle) * (py - oy)
    return qx, qy

coor_1=rotate_coordinates((x_center,y_center), (2235,507), math.radians(30.731556062626673))
coor_1
coor_2=rotate_coordinates((x_center,y_center), (2817,161), math.radians(30.731556062626673))
coor_2
coor_1[0]
b=rot.crop((coor_1[0],coor_1[1],coor_2[0],coor_2[1]))
plt.imshow(b)

#Highligths lines

#EdgeFilter just highlitghts edges
 
from PIL import ImageFilter

cover_edges = cover.filter(ImageFilter.EDGE_ENHANCE)
cover_edges.show()

cover_edges_more = cover.filter(ImageFilter.EDGE_ENHANCE_MORE)
cover_edges_more.show()

#Drawing line on coordinates of a shooting star and 
blank = Image.open("blank.tif", )
from PIL import Image, ImageDraw
draw = ImageDraw.Draw(blank) 
draw.line((2235,507, 2817,161), fill=128, width=5) 
plt.imshow(blank)

