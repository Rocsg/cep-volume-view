from sequences import *
import sys
from interactions import *
from prepare_3d_figures import *

#Scenario 0= View Silhouette, amadou et bois sain,  
#Scenario 1= same with necros in more 
#Scenario 2= view T2 signal with fibers and bubbles
specimen=11 # Specimen used from 0 (AS1) to 11 (APO3)
scenario_visu=2

if(scenario_visu==0):
   view_silhouette, view_bois_sain,view_necrose,view_amadou,view_fibers,view_cambium,view_bubbles=1,1,0,1,0,0,1
if(scenario_visu==1):
   view_silhouette,  view_bois_sain,view_necrose,view_amadou,view_fibers,view_cambium,view_bubbles=1,1,1,1,0,0,1
if(scenario_visu==2):
   view_silhouette,  view_bois_sain,view_necrose,view_amadou,view_fibers,view_cambium,view_bubbles=1,0,0,1,0,1,1
if(scenario_visu==3):
   view_silhouette,  view_bois_sain,view_necrose,view_amadou,view_fibers,view_cambium,view_bubbles=1,0,0,1,1,1,1
   watermark=1
separ,chez_moi=define_cep_rep()
    
############################### VARIABLES DESCRIPTIONS AND MAIN RUPTORS ############
specimens=["CEP011_AS1","CEP012_AS2","CEP013_AS3","CEP014_RES1","CEP015_RES2","CEP016_RES3","CEP017_S1","CEP018_S2","CEP019_S3","CEP020_APO1","CEP021_APO2","CEP022_APO3"]
spec_view=specimens[specimen]
rep=chez_moi+spec_view+separ
magic_RMN_modality='T2'  #Modality used for MRI visualization, from T1 to PD
zmin,zmax=getZminmax(specimen)
## View meshes of the different parts
amadou_based_colormap=0 #0=no shading   #1 = shading based on distance to amadou
style=4 #Define the colormaps of this part
#0 : bois sain =marron clair, ecorce=blanc, necrose =jaune, bois noir=transparent#1 : bois sain =vert, ecorce=blanc, necrose =jaune , bois noir = transparent#2 : bois sain =blanc cassé, ecorce=marron, necrose =jaune orange , bois noir = marron sombre#3 : a documenter#4 : bois sain =transpa, ecorce=transpa noir, necrose =rouge vif , bois noir = transpa
colormap_fibers,fiber_viewed=19,3
use_sub='_SMO' # '_sub' or ''

build=0
if(build==1):
    build_meshes(specimen,use_sub)

#########  MISE EN PLACE SILHOUETTE ET VUE   ##############################
renderer,window_width,window_height=setup_renderer()
start = time.time()
actorSilhouette=build_silhouette(rep+'mesh_full'+use_sub+'.vtp',renderer,None,0,style) 
if(view_bois_sain==1):
    actorBoisSain=build_bois_sain(rep+'mesh_sain'+use_sub+'.vtp',renderer,None,0,style) 
if(view_amadou==1):
    actorAmadou=build_amadou(rep+'mesh_amadou'+use_sub+'.vtp',renderer,None,0,style) 
if(view_necrose==1):
    a=1
    actorNecrose=build_necrose(rep+'mesh_necrose'+use_sub+'.vtp',renderer,None,0,style) 

#########  MISE EN PLACE SILHOUETTE IRM   ##############################
if(view_cambium==1):
    zmin,zmax=getZminmax(specimen)
    print("zmin="+str(zmin))
    print("zmax="+str(zmax))
    actorCambium=build_volume_rendering_view_from_image_cep(rep+'cambium_'+magic_RMN_modality+'.tif',renderer,zmin,zmax,colormap_fibers)

#########  MISE EN PLACE FIBRES   ##############################
if(view_bubbles==1):
    actorBubbles=build_bubbles(rep+'mesh_bubbles.vtp',renderer,None,0,style) 
if(view_fibers==1):
    if(watermark==1):
        wat="_watermarked"
    else:
        wat=""
    actorFibers2=build_fibers(rep+'mesh_fibers'+wat+'.vtp',renderer,None,0,style) 

#########  MISE EN PLACE INTERACTION   ##############################
run_interactor(spec_view,renderer,window_width,window_height,type_interaction=1)
close_window(renderer)
