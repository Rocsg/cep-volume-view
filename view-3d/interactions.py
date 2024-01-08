#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu May 28 12:58:48 2020

@author: fernandr
"""

import vtk
from build_primitives import *

def run_interactor(spec_view,renderer,window_width=600,window_height=600,type_interaction=1):
    if(type_interaction==0):
        renderer.ResetCamera()
        renWin = vtk.vtkRenderWindow()
        renWin.AddRenderer(renderer)                                    
        renWin.Render()
        camera=renderer.GetActiveCamera()                   
        renWin.SetSize(window_width,window_height)
        setup_title(spec_view,renderer,window_width,window_height)
        lights=start_lights(renderer,8)
        set_lights_on_normal_mode(lights)
        setup_camera_initial_position(camera)
        print('fixed render start')
    
    elif(type_interaction==1):
        renderer.ResetCamera()
        renWin = vtk.vtkRenderWindow()
        renWin.AddRenderer(renderer)
        camera=renderer.GetActiveCamera()
        print('Setting size '+str(window_width)+' '+str(window_height))
        renWin.SetSize(window_width,window_height)
        setup_title(spec_view,renderer,window_width,window_height)
        lights=start_lights(renderer,8)
        set_lights_on_normal_mode(lights)
        setup_camera_initial_position(camera)
        print('interaction render start')
        setup_interaction(renWin,renderer)

def close_window(renderer):
    render_window = renderer.GetRenderWindow()
#    render_window.Finalize()
 #   renderer.TerminateApp()
    del render_window, renderer
    
    
""" 
################################################################
#########  SETUP GENERAL  ######################################
################################################################
 """
def setup_renderer():
    renderer = vtk.vtkRenderer()
    renderer.SetBackground(0.0,0.0,0.0)
    
    #AJOUT DES DONNEES, GESTION CAMERA ET LUMIERE
    z_begin_irm,z_end_irm,x_start_crop,y_start_crop,z_start_crop,size_x,size_y,size_z=get_image_constants()
    print('Starting rendering. Constants defined=z_begin_irm,z_end_irm,x_start_crop,y_start_crop,z_start_crop,size_x,size_y,size_z :'+str(z_begin_irm)+', '+str(z_end_irm)+', '+str(size_x)+', '+str(size_y)+', '+str(size_z))
    mobile_rendering=0 # 0 = normal on personal computer, 1=1080p, 2= 4K TV, 3= mobile_phone
    window_width,window_height,x_margin,text_width,y_margin,text_height,police_1,police_2,x_plus,space_between_texts=window_size_config(mobile_rendering)
    
    framerate,timestep=25,0
    type_view=0  # 0 = oblique 1=front, 2=right, 3 =up
    return renderer,window_width,window_height
