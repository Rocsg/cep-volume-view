#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jul 18 13:14:48 2019

@author: fernandr
"""


from colormaps import *






def get_image_constants_2(crop_type=0):    
    #Crop 0 : ne touche pas aux donnees
    #Crop 1 : enleve un quart de l'objet : les Y+ Z+
    #Crop 2 : enleve la moitie de l objet : les Z+
    #Crop 3 : enleve un huitieme de l'objet : les  X+ Y+ Z+
    #Crop 4 : enleve un quart de l objet de l'objet, les X+ Z+
    #Crop 5 : enleve le dessus, le dessous
    z_begin_irm,z_end_irm=50,370
    sliceMedZ=z_begin_irm+(z_end_irm-z_begin_irm)//2
    y_start_crop,z_start_crop=150,210
    size_x,size_y,size_z=320,300,472
    if(crop_type==0):
        x0, y0, z0, xf, yf, zf=0,0,0, 0,0,0
    elif(crop_type==1) :
        x0, y0, z0, xf, yf, zf=0,150,210, size_x,size_y,size_z
    elif(crop_type==2) :
        x0, y0, z0, xf, yf, zf=0,0,210, size_x,size_y,size_z
    elif(crop_type==3) :
        x0, y0, z0, xf, yf, zf=0,150,210, 180,size_y,size_z
    elif(crop_type==4) :
        x0, y0, z0, xf, yf, zf=0,0,sliceMedZ, 167,size_y,size_z
    elif(crop_type==5) :
        x0, y0, z0, xf, yf, zf=0,0,130, 0,0,295
        z_begin_irm=120
        z_end_irm=315
    return z_begin_irm,z_end_irm,x0,y0,z0,xf,yf,zf,size_x,size_y,size_z
    

def get_image_constants(crop_type=0):
    #Crop 0 : ne touche pas aux donnees
    #Crop 1 : enleve un quart de l'objet
    #Crop 2 : enleve un huitieme de l'objet
    #Crop 3 : enleve un huitieme de l'objet
    #Crop 4 : enleve un huitieme de l'objet, allY, Z- et les X+
    z_begin_irm,z_end_irm=50,370
    y_start_crop,z_start_crop=150,210
    size_x,size_y,size_z=320,300,472
    if(crop_type==0):
        x_start_crop, y_start_crop,z_start_crop=0,size_y,size_z
    elif(crop_type==1) :
        x_start_crop, y_start_crop,z_start_crop=size_x,150,210
    elif(crop_type==2) :
        x_start_crop, y_start_crop,z_start_crop=size_x,0,210
    elif(crop_type==3) :
        x_start_crop, y_start_crop,z_start_crop=180,150,210
    elif(crop_type==4) :
        x_start_crop, y_start_crop,z_start_crop=180,150,210
    elif(crop_type==5) :
        x_start_crop, y_start_crop,z_start_crop=0,size_y,size_z
        z_begin_irm=130
        z_end_irm=285
    return z_begin_irm,z_end_irm,x_start_crop,y_start_crop,z_start_crop,size_x,size_y,size_z











""" 
######################################################################################################################################
######### MICRO-SEQUENCES      #######################################################################################
######################################################################################################################################
"""


def sequence_turn_azimuth(n_frames,deltaAz,timestep,renWin,imageFilter,moviewriter,camera):
    for i in range(n_frames):
        camera.Azimuth(deltaAz)
        snapshot(timestep,renWin,imageFilter,moviewriter)
        if (i%10==0):
            print('turn : '+str(i)+'/'+str(n_frames))


def sequence_turn_azimuth_and_elevate(n_frames,deltaAz,deltaEl,timestep,renWin,imageFilter,moviewriter,camera):
    for i in range(n_frames):
        camera.Azimuth(deltaAz)
        camera.Elevation(deltaEl)
        snapshot(timestep,renWin,imageFilter,moviewriter)
        if (i%10==0):
            print('turn_and_elevate : '+str(i)+'/'+str(n_frames))


def sequence_turn_azimuth_and_stop_elevate_slowly(j_range,i_range,deltaAz,deltaEl,timestep,renWin,imageFilter,moviewriter,camera):
    for j in range (j_range):
        for i in range(i_range):
            camera.Azimuth(deltaAz)
            camera.Elevation(deltaEl/j_range*(j_range-j))
            snapshot(timestep,renWin,imageFilter,moviewriter)
        print('turn and stop elevate : '+str(j)+'/'+str(j_range))


def sequence_stop_azimuth_slowly(j_range,i_range,deltaAz,timestep,renWin,imageFilter,moviewriter,camera):
    for j in range (j_range):
        for i in range(i_range):
            camera.Azimuth(1.0/j_range*(j_range-1-j)*deltaAz)
            snapshot(timestep,renWin,imageFilter,moviewriter)
        print('turn and stop azimuth : '+str(j)+'/'+str(j_range))


def sequence_zoom(j_range,i_range,n_frames,zoom_factor,timestep,renWin,imageFilter,moviewriter,camera):
    for j in range (j_range):
        for i in range(i_range):
            camera.Zoom(1+j*zoom_factor)
            snapshot(timestep,renWin,imageFilter,moviewriter)
        print('accelerate zoom : '+str(j)+'/'+str(j_range))
    
    for i in range(n_frames):
        camera.Zoom(1+j_range*zoom_factor)
        snapshot(timestep,renWin,imageFilter,moviewriter)
        if (i%10==0):
            print('zoom : '+str(i)+'/'+str(n_frames))
    
    for j in range (j_range):
        for i in range(i_range):
            camera.Zoom(1+(j_range-j)*zoom_factor)
            snapshot(timestep,renWin,imageFilter,moviewriter)
        print('zoom : '+str(j)+'/'+str(j_range))



def sequence_idle(n_frames,timestep,renWin,imageFilter,moviewriter,camera):
    for i in range(int(round(n_frames))):
        snapshot(0,renWin,imageFilter,moviewriter)
        if (i%10==0):
            print('idle : '+str(i)+'/'+str(n_frames))


def progressive_zoom(timestep,renWin,imageFilter,moviewriter,camera):
    zoomTotal=1
    for i in range(5):
        for j in range(2):
            camera.Zoom(1+0.003*i)
            zoomTotal*=1+0.003*i
            snapshot(timestep,renWin,imageFilter,moviewriter)
    for i in range(22):
        for j in range(2):
            camera.Zoom(1+0.015)
            zoomTotal*=1+0.015
            snapshot(timestep,renWin,imageFilter,moviewriter)
    for i in range(5):
        for j in range(2):
            camera.Zoom(1+0.003*(5-i))
            camera.Zoom(1+0.003*(5-i))
            snapshot(timestep,renWin,imageFilter,moviewriter)
    return zoomTotal


""" 
######################################################################################################################################
######### SETUP PARAMS, CAM, ET LUMIERE      #######################################################################################
######################################################################################################################################
"""
def setup_camera_initial_position(camera):
    z_begin_irm,z_end_irm,x_start_crop,y_start_crop,z_start_crop,size_x,size_y,size_z=get_image_constants()
    camera.SetPosition(size_x*1.5, size_y*2.5,size_z*2.5);
    camera.SetFocalPoint(size_x/2,size_y/2, size_z/2);
    camera.Azimuth(14)
    camera.SetFocalPoint(size_x/2,size_y/2, size_z/2);
    camera.Roll(-103)
    camera.Roll(-25)
    camera.Elevation(10)
    camera.Azimuth(50)    
    camera.Zoom(1.2)
    camera.Roll(-10)
    camera.Elevation(-5)
    camera.Azimuth(35-5)  
    camera.Roll(-10)
    camera.Azimuth(-15)  
    camera.Elevation(160)



def add_lights_aliasing(renderer):
    z_begin_irm,z_end_irm,x_start_crop,y_start_crop,z_start_crop,size_x,size_y,size_z=get_image_constants()
    light0 = vtk.vtkLight()
    renderer.AddLight(light0)
    light0.SetPosition(size_x*1.5, size_y*2,size_z)
    light0.SetColor(1, 1, 1)
    light0.SetIntensity(0.3)


    light1 = vtk.vtkLight()
    renderer.AddLight(light1)
    light1.SetPosition(size_x*1.5, size_y*2,0)
    light1.SetColor(1, 1, 1)
    light1.SetIntensity(0.3)

    light01 = vtk.vtkLight()
    renderer.AddLight(light01)
    light01.SetPosition(-size_x*0.5, size_y*2,size_z)
    light01.SetColor(1, 1, 1)
    light01.SetIntensity(0.3)


    light11 = vtk.vtkLight()
    renderer.AddLight(light11)
    light11.SetPosition(-size_x*0.5, size_y*2,0)
    light11.SetColor(1, 1, 1)
    light11.SetIntensity(0.3)




def add_light_right_vr(renderer):
    light = vtk.vtkLight()
    renderer.AddLight(light)
    z_begin_irm,z_end_irm,x_start_crop,y_start_crop,z_start_crop,size_x,size_y,size_z=get_image_constants()
    light.SetPosition(-size_x*40, -size_y*2,size_z//4)
    light.SetColor(1, 1, 1)
    light.SetIntensity(0.7)
    return light


def new_light_for_front_view(renderer):
    front_light = vtk.vtkLight()
    renderer.AddLight(front_light)
    z_begin_irm,z_end_irm,x_start_crop,y_start_crop,z_start_crop,size_x,size_y,size_z=get_image_constants()
    front_light.SetPositional(0)
    front_light.SetPosition(size_x//2-10, size_y*3,2*size_z//3)
    front_light.SetColor(0.9, 0.6, 0.6)
    front_light.SetIntensity(0.3)
    return front_light

def set_lights_on_normal_mode(lights):
    z_begin_irm,z_end_irm,x_start_crop,y_start_crop,z_start_crop,size_x,size_y,size_z=get_image_constants()

    dx=size_x*4
    dy=size_y*4
    dz=size_z*4
#    positions=[  [ 1 ,1  ,1.8  ]  ,[1  ,1  ,-1.8  ], [ -1 ,1  , 1 ]  , [ -1 , -1 ,1  ] , [ 1 , 1 ,-1  ]     , [ -1 , -1 , -1 ]   , [ 0 , 0 , 10 ]   , [ 0 , 0 , -10 ]]
    powers=[           1        , 0.0            ,   0.0             ,   0.0             ,     0.0              ,   0.0                ,                  0,             0.0 ]
#    powers=[           10       ,0        ,   0          ,   0           ,  0              ,   0                ,                  0,             0.0 ]
    colors=[  [ 1 , 1.0 , 1.0 ] ,[0.95  , 1 ,1  ] , [ 0.8 , 1, 0.7 ], [ 1.0, 0.8 , 0.9 ], [ 0.9 , 1 , 0.8 ], [0.8  ,0.9  ,0.8  ], [ 1.0 , 0.7 , 0.8 ], [1.0  ,0.7  ,1.0  ]]
    for i in range(len(colors)):
 #       lights[i].SetPositional(0)
  #      lights[i].SetPosition(dx*positions[i][0],dy*positions[i][1],dz*positions[i][2])
        lights[i].SetColor(colors[i][0],colors[i][1],colors[i][2])   # 
        lights[i].SetIntensity(powers[i])




def start_lights(renderer,nb_lights): 
    lights=[]
    for i in range(nb_lights):
        light = vtk.vtkLight()
        light.SetLightTypeToCameraLight()
        renderer.AddLight(light)
        lights.append(light)
    return lights





def set_lights_on_upper_mode(light_green,light_green2,light_green3):
    z_begin_irm,z_end_irm,x_start_crop,y_start_crop,z_start_crop,size_x,size_y,size_z=get_image_constants()
    light_green.SetPositional(1)
    light_green.SetPosition(size_x*2, -size_y*2,size_z*2)
    light_green.SetColor(0.6, 0.6, 0.6)
    light_green.SetIntensity(0.7)
    
    light_green2.SetPositional(1)
    light_green2.SetPosition(-size_x*2+1000, size_y*2,size_z*2)
    light_green2.SetColor(0.8, 0.8, 0.8)
    light_green2.SetIntensity(1.0)
    
    light_green3.SetPositional(1)
    light_green3.SetPosition(size_x*2, size_y*2,size_z*2+1000)
    light_green3.SetColor(0.8, 0.8, 0.8)
    light_green3.SetIntensity(0.4)

def setup_movie(framerate,path_to_movie,renWin):
    imageFilter = vtk.vtkWindowToImageFilter()
    imageFilter.SetInput(renWin)
    imageFilter.SetInputBufferTypeToRGB()
    imageFilter.ReadFrontBufferOff()
    imageFilter.Update()
    moviewriter = vtk.vtkOggTheoraWriter() 
    moviewriter.SetRate(framerate) 
    moviewriter.SetQuality(2) 	
    moviewriter.SetInputConnection(imageFilter.GetOutputPort())
    moviewriter.SetFileName(path_to_movie)
    moviewriter.Start()
    return imageFilter,moviewriter

def setup_interaction(renWin,renderer):
    iren = vtk.vtkRenderWindowInteractor()
    iren.SetRenderWindow(renWin)
    iren.Render()
#    renWin.SetSize(1500,800)
    camera=renderer.GetActiveCamera()
    iren.SetLightFollowCamera(0)
#    style = vtk.vtkInteractorStyleTrackballActor()  
  #   iren.SetInteractorStyle( style );
    iren.Start()




def get_transition_times():
    trans_object,trans_text,reading_time=10,5,170
    return trans_object,trans_text,reading_time


def window_size_config(mobile_rendering):
    police_1,police_2=36,24
    if(mobile_rendering==0):
        window_width,window_height=1000, 1000
    if(mobile_rendering==1):
        window_width,window_height=1920, 1080
    if(mobile_rendering==2):
        window_width,window_height=3840,2160
        police_1,police_2=72,48
    if(mobile_rendering==3):
        window_width,window_height=1080,1920

    x_margin=window_width/12
    text_width=int(np.round(police_1*200/36))
    y_margin=int(round(window_height/18))
    text_height=int(np.round(police_1*50/36))
    x_plus=int(round(window_width*140/1200))
    space_between_texts=(window_width-2*x_margin-text_width)/(3)
    return window_width,window_height,x_margin,text_width,y_margin,text_height,police_1,police_2,x_plus,space_between_texts


def to_front_view_intro(camera):
    camera.Azimuth(-72)
    camera.Elevation(-41)
    camera.Roll(3)
#    camera.SetFocalPoint(160,150,206)
    camera.Zoom(0.8)

def from_front_view_intro(camera):
    camera.Zoom(1/0.8)
#    camera.SetFocalPoint(160,150,236)
    camera.Roll(-3)
    camera.Elevation(41)
    camera.Azimuth(72)
 


def to_front_view(camera):
    camera.Azimuth(-55+5+5+5)
    camera.Elevation(-35)
    camera.Roll(2)
    camera.SetFocalPoint(160,150,206)
    camera.Zoom(2.3)

def from_front_view(camera):
    camera.Zoom(1/2.3)
    camera.SetFocalPoint(160,150,236)
    camera.Roll(-2)
    camera.Elevation(35)
    camera.Azimuth(55-5-5-5)
 

def from_up_view_intro(camera):
    camera.Roll(-3)
    camera.Zoom(1/2.3)
#    camera.SetFocalPoint(160,150,236)
    camera.Pitch(3)
    camera.Elevation(-45)
    camera.Azimuth(72)

def to_up_view_intro(camera):
    camera.Azimuth(-72)
    camera.Elevation(45)
    camera.Pitch(-3)
#    camera.SetFocalPoint(160,230,236)
#    camera.Roll(-83)
    camera.Zoom(2.3)
    camera.Roll(3)
##    set_lights_on_upper_mode(light_green,light_green2,light_green3)



def from_up_view(camera):
    camera.Zoom(1/4.3)
    camera.Roll(83)
    camera.SetFocalPoint(160,150,236)
    camera.Elevation(-50)
    camera.Azimuth(60-5)

def to_up_view(camera):
    camera.Azimuth(-60+5)
    camera.Elevation(50)
    camera.SetFocalPoint(160,230,236)
    camera.Roll(-83)
    camera.Zoom(4.3)
#    set_lights_on_upper_mode(light_green,light_green2,light_green3)

def to_up_centered_view(camera):
    camera.Azimuth(-120)
    camera.Elevation(50)
    camera.Roll(-83)

def from_up_centered_view(camera):
    camera.Roll(83)
    camera.Elevation(-50)
    camera.Azimuth(120)



def to_right_view(camera):
    camera.Azimuth(21+5)
    camera.Elevation(-30)
    camera.Zoom(2.8)
    camera.Yaw(4)
    camera.Roll(-1.2)

def from_right_view(camera):
    camera.Roll(1.2)
    camera.Yaw(-4)
    camera.Zoom(1/2.8)
    camera.Elevation(30)
    camera.Azimuth(-21-5)
















""" 
######################################################################################################################################
#########  SETUP ET MODIF AFFICHAGE LEGENDE    #######################################################################################
######################################################################################################################################
 """


def setup_rectangle_left(day_max,mobile_rendering,renderer,proportion=0.32,at_the_top=True,r=0,g=0,b=0,opacity=0.7):
    window_width,window_height,x_margin,text_width,y_margin,text_height,police_1,police_2,x_plus,space_between_texts=window_size_config(day_max,mobile_rendering)
    rinterp,ginterp,binterp=get_interpolation_colour()
    text1="-"
    textActor = vtk.vtkTextActor()
    textActor.SetInput (text1)
    police=3300
    textActor.SetPosition ( -0.975*window_width//2, -window_height*1.276)
    textActor.GetTextProperty().SetFontSize ( police)
    textActor.GetTextProperty().SetFontFamilyToTimes()
    textActor.GetTextProperty().SetColor ( r,g,b )
    textActor.GetTextProperty().SetOpacity(opacity)
    renderer.AddActor2D ( textActor )
    return textActor



def setup_rectangle(day_max,mobile_rendering,renderer,proportion=0.32,at_the_top=True,r=0,g=0,b=0,opacity=0.7):
    window_width,window_height,x_margin,text_width,y_margin,text_height,police_1,police_2,x_plus,space_between_texts=window_size_config(day_max,mobile_rendering)
    rinterp,ginterp,binterp=get_interpolation_colour()
    text1="-"
    textActor = vtk.vtkTextActor()
    textActor.SetInput (text1)
    police=8000
    if(at_the_top):
        textActor.SetPosition ( 0-0.06*police, window_height//2-0.5*police+1*(1-proportion+0.01)*(window_height))
    else:
        textActor.SetPosition ( 0-0.06*police, window_height-0.5*police-1*(1-proportion+0.087)*(window_height))
    textActor.GetTextProperty().SetFontSize ( police)
    textActor.GetTextProperty().SetFontFamilyToTimes()
    textActor.GetTextProperty().SetColor ( r,g,b )
    textActor.GetTextProperty().SetOpacity(opacity)
    renderer.AddActor2D ( textActor )
    return textActor

def setup_rectangle_interpolation_zone(day_max,mobile_rendering,renderer):
    window_width,window_height,x_margin,text_width,y_margin,text_height,police_1,police_2,x_plus,space_between_texts=window_size_config(day_max,mobile_rendering)
    rinterp,ginterp,binterp=get_interpolation_colour()
    #FOND INTERPOLATION
    for d in range(day_max):
        for i in range(int(((window_width-2*x_margin)/day_max)/3)):
            for j in range(int(y_margin/4)):
                actT=vtk.vtkTextActor()
                actT.SetInput ( "-" )
                actT.SetPosition (space_between_texts*d+ x_margin/2+i*3, window_height-7-40-j*3+6 )
                actT.GetTextProperty().SetFontSize ( police_1*6 )
                actT.GetTextProperty().SetFontFamilyToTimes()
                actT.GetTextProperty().SetColor ( rinterp,ginterp,binterp)
                actT.GetTextProperty().SetOpacity(0.02)
                renderer.AddActor2D ( actT )






def setup_text_and_progress_bar(day_max,renderer,mobile_rendering):
    window_width,window_height,x_margin,text_width,y_margin,text_height,police_1,police_2,x_plus,space_between_texts=window_size_config(day_max,mobile_rendering)
    rmri,gmri,bmri=get_mri_colour()
    rinterp,ginterp,binterp=get_interpolation_colour()

    #AFFICHER LES TEXTES t=..  et les textes MRI acquisition et les textes Interpolation    
    for ind_texte in range(day_max+1):
        textActor = vtk.vtkTextActor()
        textActor.SetInput ( "t = "+str((ind_texte)*35)+" days" )
        textActor.SetPosition ( x_margin+space_between_texts*ind_texte +x_plus, window_height-y_margin)
        textActor.GetTextProperty().SetFontSize ( police_2 )
        textActor.GetTextProperty().SetFontFamilyToTimes()
        textActor.GetTextProperty().SetColor ( rmri,gmri,bmri )
        renderer.AddActor2D ( textActor )

        textActor = vtk.vtkTextActor()
        textActor.SetInput ( "MRI acquisition" )
        textActor.SetPosition ( x_margin+space_between_texts*ind_texte +x_plus, window_height-2*y_margin)
        textActor.GetTextProperty().SetFontSize ( (police_2*2)/3 )
        textActor.GetTextProperty().SetFontFamilyToTimes()
        textActor.GetTextProperty().SetColor ( rmri,gmri,bmri )
        renderer.AddActor2D ( textActor )

        if(ind_texte>0):
            textActor = vtk.vtkTextActor()
            textActor.SetInput ( "Interpolation" )
            textActor.SetPosition ( x_margin+space_between_texts*(ind_texte-0.5) +x_plus, window_height-2*y_margin)
            textActor.GetTextProperty().SetFontSize ( (police_2*2)/3 )
            textActor.GetTextProperty().SetFontFamilyToTimes()
            textActor.GetTextProperty().SetColor ( rinterp,ginterp,binterp )
            renderer.AddActor2D ( textActor )

    #AFFICHER LA TIMELINE
    for i in range(182):
        actT=vtk.vtkTextActor()
        actT.SetInput ( "-" )
        actT.SetPosition ( x_margin/2+56+i*5 +x_plus, window_height-y_margin-27-20 )
        actT.GetTextProperty().SetFontSize ( police_1+6 )
        actT.GetTextProperty().SetFontFamilyToTimes()
        actT.GetTextProperty().SetColor ( 1.0, 1.0, 1.0)
        actT.GetTextProperty().SetOpacity(1)
        renderer.AddActor2D ( actT )

    #AFFICHER LES POINTS IRM SUR LA TIMELINE
    for i in range(day_max+1):
        actT=vtk.vtkTextActor()
        actT.SetInput ( "|" )
        actT.SetPosition ( x_margin+i*5+38+space_between_texts*i +x_plus, window_height-y_margin-28-20 )
        actT.GetTextProperty().SetFontSize ( (police_1*4)/3 )
        actT.GetTextProperty().SetFontFamilyToTimes()
        actT.GetTextProperty().SetColor (  rmri,gmri,bmri )
        actT.GetTextProperty().SetOpacity(1)
        renderer.AddActor2D ( actT )
        actT=vtk.vtkTextActor()
        actT.SetInput ( "-" )
        actT.SetPosition ( x_margin+i*5+43+space_between_texts*i +x_plus, window_height-y_margin-27-20 )
        actT.GetTextProperty().SetFontSize ( police_1+6 )
        actT.GetTextProperty().SetFontFamilyToTimes()
        actT.GetTextProperty().SetColor ( 1.0, 1.0, 1.0) 
        actT.GetTextProperty().SetOpacity(1)
        renderer.AddActor2D ( actT )
        actT=vtk.vtkTextActor()

    actT=vtk.vtkTextActor()
    actT.SetInput ( ">" )
    actT.SetPosition ( x_margin/2-149+220*5 +x_plus, window_height-y_margin-25-20 )
    actT.GetTextProperty().SetFontSize ( police_1 )
    actT.GetTextProperty().SetFontFamilyToTimes()
    actT.GetTextProperty().SetColor ( 1.0, 1.0, 1.0 )
    actT.GetTextProperty().SetOpacity(1)
    renderer.AddActor2D ( actT )


    actP=vtk.vtkTextActor()
    actP.SetInput ( "." )
    actP.SetPosition ( compute_x_screen_from_time_value(0,x_margin,space_between_texts,x_plus,False), window_height-y_margin-58-20  +x_plus)
    actP.GetTextProperty().SetFontSize ( police_1*5 )
    actP.GetTextProperty().SetFontFamilyToTimes()
    actP.GetTextProperty().SetColor ( 1.0, 1.0, 1.0 )
    actP.GetTextProperty().SetOpacity(1)
    renderer.AddActor2D ( actP )
      
    return textActorMRI,textActorINTER,actP

def compute_x_screen_from_time_value(x_time,day_max,mobile_rendering=0):
    window_width,window_height,x_margin,text_width,y_margin,text_height,police_1,police_2,x_plus,space_between_texts=window_size_config(day_max,mobile_rendering)
    return x_margin+25+(5+space_between_texts)*x_time +x_plus

def update_moving_legends(textActorMRI,textActorINTERP,actP,x_time,mobile_rendering=0):
    window_width,window_height,x_margin,text_width,y_margin,text_height,police_1,police_2,x_plus,space_between_texts=window_size_config(day_max,mobile_rendering)
    actP.SetPosition ( compute_x_screen_from_time_value(x_time,x_margin,space_between_texts,x_plus,False), window_height-y_margin-58-20 )

def progressive_acceleration_in_time2(nb_interp,day_max,starting_frame):
    start_transition=nb_interp/3
    stop_transition=2*nb_interp/3
    vect_days=np.zeros(5000)
    vect_times=np.zeros(5000)
    vect_fra=np.zeros(5000)
    vect_rates=(1,1)
    vect_frames=(10,10)
    n_rates=2
    n_tot=5000
    incr=0
    slice=-0.4999
    slice_double=0
    for rat in range(n_rates):
        val_rate=vect_rates[rat]
        val_frames=vect_frames[rat]
        for fra in range(val_frames):
            slice_double=slice_double+val_rate            
            slice=int(round(slice_double))
            vect_times[incr]=slice%120
            vect_days[incr]=slice//120
            vect_fra[incr]=starting_frame+slice
            incr=incr+1
    while(slice<(day_max*nb_interp-1)):
        slice=slice+1
        vect_times[incr]=slice%120
        vect_days[incr]=slice//120
        vect_fra[incr]=starting_frame+slice
        incr=incr+1
    vect_times[incr]=120
    vect_days[incr]=day_max-1
    vect_fra[incr]=starting_frame+slice+1
    incr=incr+1
        
    return incr,vect_times[0:incr],vect_days[0:incr],vect_fra[0:incr]


def progressive_acceleration_in_time(nb_interp,day_max,starting_frame):
    start_transition=nb_interp/3
    stop_transition=2*nb_interp/3
    vect_days=np.zeros(5000)
    vect_times=np.zeros(5000)
    vect_fra=np.zeros(5000)
    vect_rates=(0.1,0.15,0.2,0.3,0.4,0.6,0.8)
    vect_frames=(50, 50 ,30 ,30 ,20 ,10 ,10)
    n_rates=7
    n_tot=5000
    incr=0
    slice=-0.4999
    slice_double=0
    for rat in range(n_rates):
        val_rate=vect_rates[rat]
        val_frames=vect_frames[rat]
        for fra in range(val_frames):
            slice_double=slice_double+val_rate            
            slice=int(round(slice_double))
            vect_times[incr]=slice%120
            vect_days[incr]=slice//120
            vect_fra[incr]=starting_frame+slice
            incr=incr+1
    while(slice<(day_max*nb_interp-1)):
        slice=slice+1
        vect_times[incr]=slice%120
        vect_days[incr]=slice//120
        vect_fra[incr]=starting_frame+slice
        incr=incr+1
    vect_times[incr]=120
    vect_days[incr]=day_max-1
    vect_fra[incr]=starting_frame+slice+1
    incr=incr+1
        
    return incr,vect_times[0:incr],vect_days[0:incr],vect_fra[0:incr]
    
def snapshot(timestep,renWin,imageFilter,moviewriter):
    time.sleep(timestep)
    renWin.Render()
    imageFilter.Modified()
    moviewriter.Write()
