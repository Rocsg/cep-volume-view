#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May 27 11:48:45 2020

@author: fernandr
"""


from sequences import *
import sys
import os


#########################################################
# SETUP DIRS
pathChezCedric='\C:\SomethingBlabla\path_to_directory_with_directories_CEP011_AS1_etc_in_it\\'
pathChezRomain='/home/fernandr/Bureau/ML_CEP/RESULTS/EXP_8_VISUS_3D/'
experiencesLocation=0 #0=chez Romain, 1= chez Cedric
if(experiencesLocation==0):
    chez_moi=pathChezRomain
    separ='/'
else:
    chez_moi=pathChezCedric
    separ=''



""" 
################################################################
#########  BUILDING MESH  ######################################
################################################################
 """


def getZminmax(spec):
    zmin=((10)  , (10)  , (10)  , (10)  , (10)  , (10)  ,
                    (10)  , (10)  , (10)  , (10)  , (10)  , (10)  )
    zmax=((400)  , (400)  , (400)  , (400)  ,  (400)  , (400)   ,
                    (400)  , (400)  , (400)  , (400)  ,  (400)  , (400)  )

    return zmin[spec],zmax[spec]



def get_specimens():
    return ["CEP011_AS1","CEP012_AS2","CEP013_AS3","CEP014_RES1","CEP015_RES2","CEP016_RES3","CEP017_S1","CEP018_S2","CEP019_S3","CEP020_APO1","CEP021_APO2","CEP022_APO3"]


def build_all_meshes():
    for i in range(len(get_specimens())):
        build_meshes(i,"_SMO")
        build_meshes(i,"")
    

def define_cep_rep():
    pathChezCedric='\C:\SomethingBlabla\path_to_directory_with_directories_CEP011_AS1_etc_in_it\\'
    pathChezRomain='/home/fernandr/Bureau/ML_CEP/RESULTS/EXP_8_VISUS_3D/'
    if(os.path.exists("/home/fernandr/")):
        chez_moi=pathChezRomain
        separ='/'
    else:
        chez_moi=pathChezCedric
        separ=''
    return separ,chez_moi

def build_meshes(spec_int,typeSmo):
    ##Rebuild meshes or not
    action_building_segmentations=1
    action_building_fibers=1
    action_building_bubbles=1
    action_building_cambium=0
    zmin,zmax=getZminmax(spec_int)
    spec=get_specimens()[spec_int]

    iso_cambium=40
    iso_fiber=5
    rep=chez_moi+spec+separ

    if(action_building_segmentations==1):
        a=time.time()
        print('Building meshes full for specimen '+spec)
        build_mesh_and_save(rep+'segmentation_AMADOU'+typeSmo+'.tif',rep+'mesh_amadou'+typeSmo+'.vtp',  0,      127.5,0,slice_min=zmin,slice_max=zmax)#z_min_amadou,zmax_amadou
        print('')
        print('TIME after AMADOU='+str(int(time.time()-a)))
        print('')
        build_mesh_and_save(rep+'segmentation_FULLOBJECT'+typeSmo+'.tif',rep+'mesh_full'+typeSmo+'.vtp',           0,   127.5,crop_type=0,slice_min=zmin,slice_max=zmax)
        print('')
        print('TIME after FULL='+str(int(time.time()-a)))
        print('')
        build_mesh_and_save(rep+'segmentation_NECROSE'+typeSmo+'.tif',rep+'mesh_necrose'+typeSmo+'.vtp',0,      200.5,crop_type=0,slice_min=zmin,slice_max=zmax)
        print('')
        print('TIME after NECR='+str(int(time.time()-a)))
        print('')
        build_mesh_and_save(rep+'segmentation_SAIN'+typeSmo+'.tif',rep+'mesh_sain'+typeSmo+'.vtp'      ,0,   147.5,0,slice_min=zmin,slice_max=zmax)
        print('')
        print('TIME FINAL='+str(int(time.time()-a)))
        print('')
    
    
    if(action_building_fibers==1):
        a=time.time()
        fib_num=3
        rep=chez_moi+spec+separ
        print('Building meshes of fibers_level '+spec)
        
        build_mesh_and_save(rep+'fibers.tif',rep+'mesh_fibers.vtp',
                            0,   iso_fiber,crop_type=0,slice_min=-1,slice_max=-1)
        build_mesh_and_save(rep+'fibers_watermarked.tif',rep+'mesh_fibers_watermarked.vtp',
                            0,   iso_fiber,crop_type=0,slice_min=-1,slice_max=-1)
        b=time.time()-a
        print('')
        print('TIME='+str(int(b)))
        print('')
        
    if(action_building_cambium==1):
        for RMNmodality in ["PD","T2"]:
            a=time.time()
            build_mesh_and_save(rep+'cambium_'+str(RMNmodality)+'.tif',rep+'mesh_cambium_'+str(RMNmodality)+'.vtp',          0,   iso_cambium,crop_type=0,slice_min=zmin,slice_max=zmax)
            b=time.time()-a
            print('')
            print('TIME='+str(int(b)))
            print('')
    
    if(action_building_bubbles==1):
        a=time.time()
        build_mesh_and_save(rep+'bubbles.tif',rep+'mesh_bubbles.vtp',          0,   iso_cambium,crop_type=0,slice_min=-1,slice_max=-1)
        b=time.time()-a
        print('')
        print('TIME='+str(int(b)))
        print('')
    
    

