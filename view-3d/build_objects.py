#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jul 18 13:15:37 2019

@author: fernandr
"""

from build_primitives import *


def vert_pomme():
    return 52,201,36






def build_necrose(file,renderer,actor,crop_type=1,style=0):
    if(style==0):
        r,g,b=0.97,0.82, 0.6
        opac,spec,diff,amb=0, 0.1, 0.6, 0.7
    elif(style==1):
        r,g,b=0.97,0.82, 0.6
        opac,spec,diff,amb=0, 0.1, 0.6, 0.7
    elif(style==2):
        r,g,b=0.17,0.12, 0.08
        opac,spec,diff,amb=0.0, 0.1, 0.6, 0.7
    elif(style==3):
        r,g,b=0.172,0.459, 1
        opac,spec,diff,amb=0.2, 0.1, 0.6, 0.3
    elif(style==4):
        r,g,b=0.172,0.459, 1
        opac,spec,diff,amb=0.2, 0.1, 0.6, 0.3
        #opac,spec,diff,amb=1.0, 0.1, 0.6, 0.3
        
    z_begin_irm,z_end_irm,x_start_crop,y_start_crop,z_start_crop,size_x,size_y,size_z=get_image_constants()
    
    if(actor is None):
        a=1        
    else:
        actor.SetVisibility(False)
        renderer.RemoveActor(actor)
    actor=load_mesh_and_build_actor(file,r,g,b,opac,spec,diff,amb)
    actor.GetProperty().SetSpecularColor(0.7,0.8,0.9)
    actor.SetVisibility(True)
    renderer.AddActor(actor)
    return actor



def build_bubbles(file,renderer,actor,crop_type=0,style=0):
    if(style==0):
        r,g,b,   opac,spec,diff,amb ,  spec_r,spec_g,spec_b=1.0, 1.0,1.0 ,        0.27, 0.37 ,0.15,0.6           ,1.0 , 1.0  ,1.0
    elif(style==1):
        r,g,b,   opac,spec,diff,amb ,  spec_r,spec_g,spec_b=1.0, 0.8,0.8 ,        0.27, 0.17 ,0.15,0.8           ,1.0 , 1.0  ,1.0
    elif(style==2):
        r,g,b,   opac,spec,diff,amb ,  spec_r,spec_g,spec_b=0.20,0.13, 0.10,        0.35, 0.15 ,0.4,0.2           ,1.0 , 1.0  ,1.0
    elif(style==3):
        r,g,b,   opac,spec,diff,amb ,  spec_r,spec_g,spec_b=0.20,0.13, 0.10,        0.18, 0.15 ,0.4,0.2           ,1.0 , 1.0  ,1.0
    elif(style==4):
        r,g,b=1,1,1 #,0.82,0.8  r,g,b=0.80,1.0, 0.80
        opac,spec,diff,amb=1.0, 0.30, 0.5, 0.4        
        spec_r,spec_g,spec_b= 1.0 , 1.0  ,1.0

    z_begin_irm,z_end_irm,x_start_crop,y_start_crop,z_start_crop,size_x,size_y,size_z=get_image_constants(crop_type)
    if(actor is None):
        a=1        
    else: 
        actor.SetVisibility(False)
        renderer.RemoveActor(actor)
    actor=load_mesh_and_build_actor(file,r,g,b,opac,spec,diff,amb)
    actor.SetVisibility(True)
    actor.GetProperty().SetSpecularColor( spec_r,spec_g,spec_b)
    renderer.ResetCameraClippingRange()
    renderer.AddActor(actor)
    return actor



def build_silhouette(file,renderer,actor,crop_type=0,style=0):
    if(style==0):
        r,g,b,   opac,spec,diff,amb ,  spec_r,spec_g,spec_b=1.0, 1.0,1.0 ,        0.27, 0.37 ,0.15,0.6           ,1.0 , 1.0  ,1.0
    elif(style==1):
        r,g,b,   opac,spec,diff,amb ,  spec_r,spec_g,spec_b=1.0, 0.8,0.8 ,        0.27, 0.17 ,0.15,0.8           ,1.0 , 1.0  ,1.0
    elif(style==2):
        r,g,b,   opac,spec,diff,amb ,  spec_r,spec_g,spec_b=0.20,0.13, 0.10,        0.35, 0.15 ,0.4,0.2           ,1.0 , 1.0  ,1.0
    elif(style==3):
        r,g,b,   opac,spec,diff,amb ,  spec_r,spec_g,spec_b=0.20,0.13, 0.10,        0.18, 0.15 ,0.4,0.2           ,1.0 , 1.0  ,1.0
    elif(style==4):
        r,g,b,   opac,spec,diff,amb ,  spec_r,spec_g,spec_b=1.0,1.0, 0.75,        0.20, 0.3 ,0.25,0.4           ,1.0 , 1.0  ,0.75

    z_begin_irm,z_end_irm,x_start_crop,y_start_crop,z_start_crop,size_x,size_y,size_z=get_image_constants(crop_type)
    if(actor is None):
        a=1        
    else: 
        actor.SetVisibility(False)
        renderer.RemoveActor(actor)
    actor=load_mesh_and_build_actor(file,r,g,b,opac,spec,diff,amb)
    actor.SetVisibility(True)
    actor.GetProperty().SetSpecularColor( spec_r,spec_g,spec_b)
    renderer.ResetCameraClippingRange()
    renderer.AddActor(actor)
    return actor


def build_bois_sain(file,renderer,actor,crop_type=1,style=0):
    if(style==0):
        r,g,b=1.0,0.90,0.85 #,0.82,0.8
        opac,spec,diff,amb=1.0, 0.24, 0.6, 0.3
    elif(style==1):
        r,g,b=0.676,1.0, 0.788
        opac,spec,diff,amb=1.0, 0.24, 0.6, 0.3
    elif(style==2):
        r,g,b=52/255,201/255,36/255 #,0.82,0.8  r,g,b=0.80,1.0, 0.80
        opac,spec,diff,amb=1.0, 0.30, 0.5, 0.4        
    elif(style==3):
        r,g,b=52/255,201/255,36/255 #,0.82,0.8  r,g,b=0.80,1.0, 0.80
        opac,spec,diff,amb=0.30, 0.30, 0.6, 0.4        
    elif(style==4):
        r,g,b=52/255,201/255,36/255 #,0.82,0.8  r,g,b=0.80,1.0, 0.80
        opac,spec,diff,amb=1.00, 0.30, 0.5, 0.4        
    z_begin_irm,z_end_irm,x_start_crop,y_start_crop,z_start_crop,size_x,size_y,size_z=get_image_constants()
    
    if(actor is None):
        a=1        
    else:
        actor.SetVisibility(False)
        renderer.RemoveActor(actor)  
    actor=load_mesh_and_build_actor(file,r,g,b,opac,spec,diff,amb)
  #  actor.GetProperty().SetSpecularPower(6)
    actor.SetVisibility(True)
    actor.GetProperty().SetSpecularPower(10)
    renderer.AddActor(actor)
    return actor

def build_amadou(file,renderer,actor,crop_type=1,style=0):
    if(style==0):
        r,g,b=0.97,0.82, 0.6
        opac,spec,diff,amb=1.0, 0.1, 0.6, 0.7
    elif(style==1):
        r,g,b=0.97,0.82, 0.6
        opac,spec,diff,amb=1.0, 0.1, 0.6, 0.7
    elif(style==2):
        r,g,b=1.0,0.12, 0.06
        opac,spec,diff,amb=1.0, 0.2, 0.15, 0.5
    elif(style==3):
        r,g,b=1.0,0.12, 0.06
        opac,spec,diff,amb=1.0, 0.2, 0.15, 0.5
    elif(style==4):
        r,g,b=1.0,0.12, 0.06
        opac,spec,diff,amb=1.0, 0.3, 0.15, 0.5

    z_begin_irm,z_end_irm,x_start_crop,y_start_crop,z_start_crop,size_x,size_y,size_z=get_image_constants()
    
    if(actor is None):
        a=1        
    else:
        actor.SetVisibility(False)
        renderer.RemoveActor(actor)
    actor=load_mesh_and_build_actor(file,r,g,b,opac,spec,diff,amb)
    actor.GetProperty().SetSpecularColor(0.7,0.8,0.9)
    actor.SetVisibility(True)
    renderer.AddActor(actor)
    return actor



def build_fibers(file,renderer,actor,crop_type=1,style=0):
    if(style==0):
        r,g,b=1.0,0.90,0.85 #,0.82,0.8
        opac,spec,diff,amb=1.0, 0.24, 0.6, 0.3
    elif(style==1):
        r,g,b=0.676,1.0, 0.788
        opac,spec,diff,amb=1.0, 0.24, 0.6, 0.3
    elif(style==2):
        r,g,b=52/255,201/255,36/255 #,0.82,0.8  r,g,b=0.80,1.0, 0.80
        opac,spec,diff,amb=1.0, 0.30, 0.5, 0.4        
    elif(style==3):
        r,g,b=52/255,201/255,36/255 #,0.82,0.8  r,g,b=0.80,1.0, 0.80
        opac,spec,diff,amb=0.30, 0.30, 0.6, 0.4        
    elif(style==4):
        r,g,b=255/255,255/255,255/255 #,0.82,0.8  r,g,b=0.80,1.0, 0.80
        opac,spec,diff,amb=1.0, 0.30, 0.5, 0.4        
    z_begin_irm,z_end_irm,x_start_crop,y_start_crop,z_start_crop,size_x,size_y,size_z=get_image_constants()
    
    if(actor is None):
        a=1        
    else:
        actor.SetVisibility(False)
        renderer.RemoveActor(actor)  
    actor=load_mesh_and_build_actor(file,r,g,b,opac,spec,diff,amb)
  #  actor.GetProperty().SetSpecularPower(6)
    actor.SetVisibility(True)
    actor.GetProperty().SetSpecularPower(10)
    renderer.AddActor(actor)
    return actor


















def build_moelle(day_i,inter,renderer,actor,crop_type=1,zo=0,zf=512):
    day_i_plus=day_i+1
    basenom=str(day_i)+str(day_i_plus)+'_'+str(inter)
    source_rep=get_source_rep()
    r,g,b=0.922, 0.804,0.72
    opac,spec,diff,amb=1.0, 0.2, 0.3, 0.18
    isoVal=55.5
    z_begin_irm,z_end_irm,x_start_crop,y_start_crop,z_start_crop,size_x,size_y,size_z=get_image_constants()
    if(actor is None):
        a=1        
    else: 
        actor.SetVisibility(False)
        renderer.RemoveActor(actor)
    actor=build_actor_from_image2(source_rep+'/images/moe'+basenom+'_gauss.tif',r,g,b,opac,spec,diff,amb,isoVal,crop_type,0,None,zo,zf)
    actor.SetVisibility(True)
    renderer.AddActor(actor)
    return actor

def build_cambium(day_i,inter,renderer,actor,crop_type=1,zo=0,zf=512):
    day_i_plus=day_i+1
    basenom=str(day_i)+str(day_i_plus)+'_'+str(inter)
    source_rep=get_source_rep()
    r,g,b=get_cambium_rgb()
    opac,spec,diff,amb=1.0, 0.2, 0.4, 0.18
    isoVal=67.5
    z_begin_irm,z_end_irm,x_start_crop,y_start_crop,z_start_crop,size_x,size_y,size_z=get_image_constants()
    if(actor is None):
        a=1        
    else: 
        actor.SetVisibility(False)
        renderer.RemoveActor(actor)
    actor= build_actor_from_image2(source_rep+'/images/camb'+basenom+'_gauss.tif',r,g,b,opac,spec,diff,amb,isoVal,crop_type,0,None,zo,zf)
    actor.SetVisibility(True)
    renderer.AddActor(actor)
    return actor

def build_vessels(day_i,inter,renderer,actor,crop_type=1,zo=0,zf=512):
    day_i_plus=day_i+1
    basenom=str(day_i)+str(day_i_plus)+'_'+str(inter)
    source_rep=get_source_rep()
    r,g,b=0.576, 0.688,0.412
    opac,spec,diff,amb=1.0, 0.3, 0.3, 0.1
    isoVal=182.5
    z_begin_irm,z_end_irm,x_start_crop,y_start_crop,z_start_crop,size_x,size_y,size_z=get_image_constants()
    
    if(actor is None):
        a=1        
    else:
        actor.SetVisibility(False)
        renderer.RemoveActor(actor)
    actor=build_actor_from_image2(source_rep+'/images/ves'+basenom+'_gauss.tif',r,g,b,opac,spec,diff,amb,isoVal,crop_type,0,None,zo,zf)
    actor.GetProperty().SetSpecularColor(0.8,0.9,0.7)
    actor.SetVisibility(True)
    renderer.AddActor(actor)
    return actor




def build_mushroom(day_i,inter,nb_interp,renderer,actor,sigma=0):
    day_i_plus=day_i+1
    sigma=max(0,sigma)
    basenom=str(day_i)+str(day_i_plus)+'_'+str(inter)
    source_rep=get_source_rep()
    r,g,b,   opac,spec,diff,amb ,  spec_r,spec_g,spec_b=get_mushroom_colours()

    isoVal=127.5
    z_begin_irm,z_end_irm,x_start_crop,y_start_crop,z_start_crop,size_x,size_y,size_z=get_image_constants()
    if(actor is None):
        a=1        
    else: 
        actor.SetVisibility(False)
        renderer.RemoveActor(actor)
#    actor= build_actor_from_image2(source_rep+'/mushroom/seg'+basenom+'_sigma_'+str(sigma)+'.tif',r,g,b,opac,spec,diff,amb,isoVal,0,1,source_rep+'/images/camb'+basenom+'_gauss.tif')
    actor= build_actor_from_image2(source_rep+'/mushroom/segCont_'+basenom+'_sigma_'+str(sigma)+'.tif',r,g,b,opac,spec,diff,amb,isoVal,0,1,source_rep+'/images/camb'+basenom+'_gauss.tif',0,size_z)
    actor.SetVisibility(True)
    actor.GetProperty().SetSpecularColor( spec_r,spec_g,spec_b)
    renderer.AddActor(actor)
    return actor


def build_mushroom_continuous(day_i,inter,nb_interp,renderer,actor):
    r,g,b,   opac,spec,diff,amb ,  spec_r,spec_g,spec_b=get_mushroom_colours()
    isoVal=10000-((inter+1)/120.0+day_i+1000.0)
    z_begin_irm,z_end_irm,x_start_crop,y_start_crop,z_start_crop,size_x,size_y,size_z=get_image_constants()
    source_rep=get_source_rep()
    if(actor is None):
        a=1        
    else: 
        actor.SetVisibility(False)
        renderer.RemoveActor(actor)
    actor= build_actor_from_image_continuous('/mnt/DD_COMMON/Data_VITIMAGE/Movie_maker_v2/Img_intermediary/mushroom/segB',r,g,b,opac,spec,diff,amb,isoVal,0,1,source_rep+'/images/camb01_0_gauss_float.tif')
#    actor.SetVisibility(True)
#    actor.GetProperty().SetSpecularColor( spec_r,spec_g,spec_b)
#    renderer.AddActor(actor)
    return actor






def build_vr(day_i,inter,nb_interp,renderer,volume,crop_type,zmin,zmax,colormap=0,opac=1):
    day_i_plus=day_i+1
    basenom=str(day_i)+str(day_i_plus)+'_'+str(inter)
    source_rep=get_source_rep()
    z_begin_irm,z_end_irm,x_start_crop,y_start_crop,z_start_crop,size_x,size_y,size_z=get_image_constants(crop_type)
        
    if(volume is None):
        a=1        
    else:
        renderer.RemoveViewProp(volume)
    if(zmin<0):
        zmin=0
    if(zmax>size_z):
        zmax=size_z
    if(zmin>zmax):
        zmin=zmax
    volume=build_volume_rendering_view_from_image2('/mnt/DD_COMMON/Data_VITIMAGE/Movie_maker_v2/champs/samples/full'+basenom+'.tif',opac,renderer,crop_type,zmin,zmax,colormap)
    return volume






def build_mpr(day_i,inter,renderer,volume,crop_type,colormap):
    day_i_plus=day_i+1
    basenom=str(day_i)+str(day_i_plus)+'_'+str(inter)
    source_rep=get_source_rep()
    opac=1
    z_begin_irm,z_end_irm,x_start_crop,y_start_crop,z_start_crop,size_x,size_y,size_z=get_image_constants(crop_type)
        
    if(volume is None):
        a=1        
    else:
        renderer.RemoveViewProp(volume)
    XY_plane,XZ_plane,YZ_plane=build_multi_planar_view_from_image2(source_rep+'/images/full'+basenom+'.tif',opac,renderer,crop_type,colormap)
    return XY_plane,XZ_plane,YZ_plane



def build_planar(axis,day_i,inter,renderer,plane,crop_type=0,direction=0,colormap=0):
    day_i_plus=day_i+1
    basenom=str(day_i)+str(day_i_plus)+'_'+str(inter)
    source_rep=get_source_rep()
    opac=1
    z_begin_irm,z_end_irm,x_start_crop,y_start_crop,z_start_crop,size_x,size_y,size_z=get_image_constants(crop_type)
    if(plane is None):
        a=1        
    else:
        plane.SetVisibility(False)
        renderer.RemoveActor(plane)
    if(direction==0):
        plane=build_planar_view_from_image2(axis,source_rep+'/images/full'+basenom+'.tif',opac,renderer,crop_type,colormap)
    if(direction==1):
        plane=build_planar_view_from_image2(axis,source_rep+'/images/front_d_'+basenom+'_samples.tif',opac,renderer,crop_type,colormap)
    if(direction==2):
        plane=build_planar_view_from_image2(axis,source_rep+'/images/back_d_'+basenom+'_samples.tif',opac,renderer,crop_type,colormap)
    return plane




def build_planar_slice(n_frame,renderer,plane,offset_X,offset_Y): 
    basenom='frame_'+str(n_frame)+'.tif'
    source_rep=get_source_rep()
    opac=1        
    if(plane is None):
        a=1        
    else:
        plane.SetVisibility(False)
    renderer.RemoveActor(plane)
    plane=build_planar_slice_from_RGBimage2(2,source_rep+'/fusion/'+basenom,opac,renderer)
    plane.AddPosition(offset_X,offset_Y,0)
    return plane




