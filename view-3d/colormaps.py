#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jul 18 13:15:58 2019

@author: fernandr
"""
import time
from datetime import datetime
from skimage import io
import vtk
import numpy as np
from vtk.util.misc import vtkGetDataRoot
VTK_DATA_ROOT = vtkGetDataRoot()

  

def get_common_colormaps(colormap):
    #### BW colormaps
    # BW standard
    if(colormap==0):
        lut=create_bw_lookup_table(0,255,0,1)
    # BW without noisy background
    if(colormap==1):
        lut=create_bw_lookup_table(40,255,0,1)
    # BW with dark values in grey
    if(colormap==2):
        lut=create_bw_lookup_table(40,255,0.3,1)

    #### SPECTRUM colormaps
    # standard nice spectrum
    if(colormap==10):
        lut=create_rainbow_lookup_table(0,255,2,1,1)
 
    # spectrum without noisy values
    if(colormap==11):
        lut=create_rainbow_lookup_table(40,255,2,1,1)
  
    # spectrum without noisy and without yellow, orange, red
    if(colormap==12):
        lut=create_rainbow_lookup_table(40,255,0,1,1)

    # spectrum without noisy with blue, purple, pink, red
    if(colormap==13):
        lut=create_rainbow_lookup_table(40,255,1,1,1)
    # Jah love
    if(colormap==14):
        lut=create_rainbow_lookup_table(40,255,3,1,1)

    # spectrum without noisy values
    if(colormap==15):
        lut=create_rainbow_lookup_table(60,255,2,1,1)

    # spectrum without noisy values
    if(colormap==16):
        lut=create_rainbow_lookup_table(80,255,2,1,1)

    # spectrum without noisy values
    if(colormap==17):
        lut=create_rainbow_lookup_table(100,255,2,1,1)

    # spectrum without noisy values
    if(colormap==18):
        lut=create_rainbow_lookup_table(120,255,2,1,1)
  # spectrum without noisy values
  
    # spectrum without noisy values
    if(colormap==19):
        lut=create_rainbow_lookup_table(40,255,2,1,1)
  # spectrum without noisy values

    #### GREEN colormaps
    #Full green
    if(colormap==20):
        lut=create_monochrome_lookup_table(0,255,0,1,0.3334,1)
    #Green without noisy
    if(colormap==21):
        lut=create_monochrome_lookup_table(40,255,0,1,0.3334,1)
    #Shiny green
    if(colormap==22):
        lut=create_monochrome_lookup_table(40,180,0,1,0.3334,1)

    #### RED colormaps
    #Full red
    if(colormap==30):
        lut=create_monochrome_lookup_table(0,255,0,1,0,1)
    #Red without noisy
    if(colormap==31):
        lut=create_monochrome_lookup_table(40,255,0,1,0,1)
    #Shiny red
    if(colormap==32):
        lut=create_monochrome_lookup_table(40,180,0,1,0,1)

    return lut




def create_lookup_table(intensity_min,intensity_max,sat_min,sat_max,hue_min,hue_max,cont_min,cont_max):
     # Start by creating a black/white lookup table.
    bwLut = vtk.vtkLookupTable()
    bwLut.SetTableRange(intensity_min,intensity_max)
    bwLut.SetSaturationRange(sat_min,sat_max)
    bwLut.SetHueRange(hue_min, hue_max)
    bwLut.SetValueRange(cont_min, cont_max)
    bwLut.Build()  # effective built
    #for i in range(256):
    #    print('STANDARD LUT i='+str(i)+'  ('+str(bwLut.GetTableValue(i)[0])+', '+str(bwLut.GetTableValue(i)[1])+', '+str(bwLut.GetTableValue(i)[2])+' ) ')
    return bwLut


 
def create_bw_lookup_table(thresh_start,thresh_stop,val_start,val_stop):
    var_val=val_stop-val_start
    var_ind=thresh_stop-thresh_start+1
    val_at_index_0=val_start-thresh_start/var_ind*var_val
    val_at_index_255=val_stop+(255-thresh_stop)/var_ind*var_val
    lut=create_lookup_table(0,255,0,0, 0,0, val_at_index_0,val_at_index_255)
    for i in range(thresh_start):
        lut.SetTableValue(i,lut.GetTableValue(thresh_start)[0],lut.GetTableValue(thresh_start)[1],lut.GetTableValue(thresh_start)[2],0)
    for i in range(256-thresh_stop):
        lut.SetTableValue(thresh_stop+i,lut.GetTableValue(thresh_stop)[0],lut.GetTableValue(thresh_stop)[1],lut.GetTableValue(thresh_stop)[2],1)
    #for i in range(256):
    #    print('BW lut i='+str(i)+'  ('+str(lut.GetTableValue(i)[0])+', '+str(lut.GetTableValue(i)[1])+', '+str(lut.GetTableValue(i)[2])+' ) ')
    return lut


def create_monochrome_lookup_table(thresh_start,thresh_stop,val_start,val_stop,hue,saturation):
    var_val=val_stop-val_start
    var_ind=thresh_stop-thresh_start+1
    val_at_index_0=val_start-thresh_start/var_ind*var_val
    val_at_index_255=val_stop+(255-thresh_stop)/var_ind*var_val
    lut=create_lookup_table(0,255,saturation,saturation, hue,hue, val_at_index_0,val_at_index_255)
    for i in range(thresh_start):
        lut.SetTableValue(i,lut.GetTableValue(thresh_start)[0],lut.GetTableValue(thresh_start)[1],lut.GetTableValue(thresh_start)[2],0)
    for i in range(256-thresh_stop):
        lut.SetTableValue(thresh_stop+i,lut.GetTableValue(thresh_stop)[0],lut.GetTableValue(thresh_stop)[1],lut.GetTableValue(thresh_stop)[2],1)
    return lut



def create_rainbow_lookup_table(thresh_start,thresh_stop,map_type=0,saturation=1,contrast=1):
    # map_type 0 stands for indigo,blue,cyan, green
    if(map_type==0):
        val_start=0.753
        val_stop=0.38
    # map_type 1 stands for blue, indigo, purple, pink,red
    if(map_type==1):
        val_start=0.673
        val_stop=0.9999
    # map_type 2 stands for indigo,blue,cyan,green,yellow,orange, red
    if(map_type==2):
        val_start=0.7
        val_stop=0
    # map_type 3 stands for green,yellow,orange,red
    if(map_type==3):
        val_start=0.334
        val_stop=0.0001


    var_val=val_stop-val_start
    var_ind=thresh_stop-thresh_start+1
    val_at_index_0=val_start-thresh_start/var_ind*var_val
    val_at_index_255=val_stop+(255-thresh_stop)/var_ind*var_val
    lut=create_lookup_table(0,255,saturation,saturation,val_at_index_0,val_at_index_255,contrast,contrast)
    for i in range(thresh_start):
        lut.SetTableValue(i,lut.GetTableValue(thresh_start)[0],lut.GetTableValue(thresh_start)[1],lut.GetTableValue(thresh_start)[2])
    for i in range(256-thresh_stop):
        lut.SetTableValue(thresh_stop+i,lut.GetTableValue(thresh_stop)[0],lut.GetTableValue(thresh_stop)[1],lut.GetTableValue(thresh_stop)[2])
    return lut



 
 
def get_field_rep():
    return '/mnt/DD_COMMON/Data_VITIMAGE/Movie_maker_v2/champs/samples'
 
def get_source_rep():
    return '/mnt/DD_COMMON/Data_VITIMAGE/Movie_maker_v2/img_interp'

def get_mri_rgb():
    return 1,215/255,0

def get_interpolation_colour():
    return 175/255, 238/255, 238/255

def get_cambium_rgb():
    return 0.712, 0.554,0.5

def actor_going_black(actor,transition,i):
    r,g,b=actor.GetProperty().GetColor()
    new_r=r*(1-i/transition)
    new_g=g*(1-i/transition)
    new_b=b*(1-i/transition)
    actor.GetProperty().SetColor( new_r, new_g, new_b ) 
    actor.GetProperty().SetDiffuseColor( new_r, new_g, new_b )  
    actor.GetProperty().SetAmbientColor( new_r, new_g, new_b )      
    actor.GetProperty().SetSpecularColor( new_r, new_g, new_b )      
    
def actor_rgb_ramp_to_color(actor,transition,new_r,new_g,new_b):
    old_r,old_g,old_b=actor.GetProperty().GetColor()
    delta_r=(new_r-old_r)/transition
    delta_g=(new_g-old_g)/transition
    delta_b=(new_b-old_b)/transition
    vals_r=np.zeros(transition)
    vals_g=np.zeros(transition)
    vals_b=np.zeros(transition)
    for i in range(transition):
        vals_r=old_r+(i+1)*delta_r
        vals_g=old_g+(i+1)*delta_g
        vals_b=old_b+(i+1)*delta_b
    return vals_r,vals_g,vals_b

def set_actor_rgb(actorCur,r,g,b):
    actorCur.GetProperty().SetColor( r, g, b ) 
    actorCur.GetProperty().SetDiffuseColor(r, g, b)  
    actorCur.GetProperty().SetAmbientColor(r, g, b)      
    actorCur.GetProperty().SetSpecularColor(r, g, b)      


def set_volume_opacity(volume,opacity,thresh_start,thresh_stop):
    volumeProperty = volume.GetProperty()
    compositeOpacity = vtk.vtkPiecewiseFunction()
    compositeOpacity.AddPoint(0.0,0.0);
    compositeOpacity.AddPoint(thresh_start,0.0);
    compositeOpacity.AddPoint(thresh_stop,opacity);
    volumeProperty.SetScalarOpacity(compositeOpacity)
    volume.SetProperty(volumeProperty)


def set_volume_rgb(volume,r,g,b):
    volumeProperty = volume.GetProperty() 
    color = vtk.vtkColorTransferFunction()
    color.AddRGBPoint(0.0  ,0.0,0.0,0.0)
    color.AddRGBPoint(40.0  ,0,0.0,0.0)
    color.AddRGBPoint(100.0,r,g,b)
    color.AddRGBPoint(255,r,g,b)
    volumeProperty.SetColor(color)
    volume.SetProperty(volumeProperty)


    # Actors are added to the renderer.
 


def set_volume_colormap(volume,lut):
    volumeProperty = volume.GetProperty() 
    color = vtk.vtkColorTransferFunction()
    for i in range(256):
        color.AddRGBPoint(i,lut.GetTableValue(i)[0],lut.GetTableValue(i)[1],lut.GetTableValue(i)[2])
    volumeProperty.SetColor(color)
    volume.SetProperty(volumeProperty)






    
def set_actor_color_to_cambium(actorCur):
    r,g,b=get_cambium_rgb()
    opac,spec,diff,amb=1.0, 0.2, 0.4, 0.18
    actorCur.GetProperty().SetColor(r,g,b) 
    actorCur.GetProperty().SetOpacity(opac )  
    actorCur.GetProperty().SetInterpolationToGouraud ()
    actorCur.GetProperty().SetSpecular(spec)
    actorCur.GetProperty().SetDiffuseColor( r,g,b)  
    actorCur.GetProperty().SetDiffuse(diff)  
    actorCur.GetProperty().SetAmbientColor( r,g,b )   
    actorCur.GetProperty().SetAmbient(amb)  
    
def get_mushroom_colours():
    return    0.9, 0.1,0.1 ,      0.45, 0.7, 0.4, 0.18           ,1.0  ,0.2  ,0.2
    #            r,g,b,              opac,spec,diff,amb ,        spec_r,spec_g,spec_b

def get_silhouette_colours():
    return   1.0, 0.8,0.8 ,        0.20, 0.01 ,0.2,0.38           ,0.8 , 0.8  ,1.0
    #          r,g,b,                opac,spec,diff,amb ,       spec_r,spec_g,spec_b

