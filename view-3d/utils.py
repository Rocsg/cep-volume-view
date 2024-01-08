#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Oct 15 18:06:11 2019

@author: fernandr
"""
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.pyplot import *
import pandas as pd
from math import pi
from matplotlib.patches import Rectangle
 
specimens=['CEP011_AS1','CEP012_AS2','CEP013_AS3',   'CEP014_RES1','CEP015_RES2','CEP016_RES3',  'CEP017_S1','CEP018_S2','CEP019_S3',  'CEP020_APO1','CEP021_APO2','CEP022_APO3']

def compute_red_tab():
    confusions=np.zeros((4,5,5))
    globAcc=np.zeros((4))
    accuracies=np.zeros((4,5))
    precisions=np.zeros((4,5))
    recalls=np.zeros((4,5))
    fscores=np.zeros((4,5))
    for i in range(4):
        confusions[i]=read_confusion_mat_from_full_text(exp,i,i)
        globAcc[i]=accuracy(confusions[i,:,:])
        for cl in range(5):
            accuracies[i,cl]=accuracy_class(confusions[i,:,:],cl)
            precisions[i,cl]=precision_class(confusions[i,:,:],cl)
            recalls[i,cl]=recall_class(confusions[i,:,:],cl)
            fscores[i,cl]=harmonic_mean(precisions[i,cl],recalls[i,cl])

    valsGlob=np.zeros((4,21))
    valsGlob[:,0]=globAcc
    for cl in range(5):
        valsGlob[:,1+4*cl]=accuracies[:,cl]    
        valsGlob[:,2+4*cl]=precisions[:,cl]
        valsGlob[:,3+4*cl]=recalls[:,cl]
        valsGlob[:,4+4*cl]=harmonic_mean(valsGlob[:,2+4*cl],valsGlob[:,3+4*cl])

    valsGlob2=np.zeros((6,21))
    valsGlob2[0:4,:]=valsGlob
    valsGlob2[4:6,:]=stats_vect(valsGlob)
    write_vals_tab2d_in_file_with_percent( valsGlob2,'/home/fernandr/Bureau/ML_CEP/Tabs/tab_red.txt')






def compute_brown_tab(consensus=0):
    brown_ret=np.zeros((10,2,21))
    for sb in range(10):
        sub=sb+1
        if(consensus==0):
            brown_ret[sb,:,:]=compute_purple_tab('EXP_5_RESOLUTIONS/SUB_'+str(sub)+'/')
        else:
            brown_ret[sb,:,:]=compute_purple_tab('EXP_5_RESOLUTIONS_CONSENSUS/SUB_'+str(sub)+'/')
    if(consensus==0):
        write_vals_tab2d_in_file_with_percent( tab3d_to_tab2d(brown_ret),'/home/fernandr/Bureau/ML_CEP/Tabs/tab_brown.txt')
    else:
        write_vals_tab2d_in_file_with_percent( tab3d_to_tab2d(brown_ret),'/home/fernandr/Bureau/ML_CEP/Tabs/tab_brown_consensus.txt')
    return brown_ret


def compute_yellow_tab():
    yellow_ret=np.zeros((16,2,21))
    yellow_vals=np.zeros((16,2,5))
    for rx in range(2):
        for t1 in range(2):
            for t2 in range(2):
                for dp in range(2):
                    config=str(rx)+str(t1)+str(t2)+str(dp)
                    config_num=rx*8+t1*4+t2*2+dp
                    yellow_ret[config_num,:,:]=compute_purple_tab('EXP_4_MODALITIES/MOD_CROSSMOD_'+str(config)+'/')
    write_vals_tab2d_in_file_with_percent( tab3d_to_tab2d(yellow_ret),'/home/fernandr/Bureau/ML_CEP/Tabs/tab_yellow.txt')
    yellow_vals[:,:,0]=yellow_ret[:,:,4]
    yellow_vals[:,:,1]=yellow_ret[:,:,8]
    yellow_vals[:,:,2]=yellow_ret[:,:,12]
    yellow_vals[:,:,3]=yellow_ret[:,:,16]
    yellow_vals[:,:,4]=yellow_ret[:,:,20]
    return yellow_vals


def compute_purple_tab(dir):     
     exp='/home/fernandr/Bureau/ML_CEP/RESULTS/'+dir
     print('Ouverture du dossier '+exp)
     if(exp_existe(exp)!=1):
         print('Experience n existe pas')
         return np.zeros((2,21))
     print('ok')
     confusions=np.zeros((12,12,5,5))
     globAcc=np.zeros((12,12))
     accuracies=np.zeros((5,12,12))
     precisions=np.zeros((5,12,12))
     recalls=np.zeros((5,12,12))
     fscores=np.zeros((5,12,12))
     for i1 in range (12):
         for i2 in range (12):
             if(i2>i1):
                 confusions[i1,i2]=read_confusion_mat_from_full_text(exp,i1,i2)
                 globAcc[i1,i2]=accuracy(confusions[i1,i2,:,:])
                 confusions[i2,i1]=read_confusion_mat_from_full_text(exp,i1,i2)
                 globAcc[i2,i1]=accuracy(confusions[i1,i2,:,:])
                 for cl in range(5):
                     accuracies[cl,i1,i2]=accuracy_class(confusions[i1,i2,:,:],cl)
                     precisions[cl,i1,i2]=precision_class(confusions[i1,i2,:,:],cl)
                     recalls[cl,i1,i2]=recall_class(confusions[i1,i2,:,:],cl)
                     fscores[cl,i1,i2]=harmonic_mean(precisions[cl,i1,i2],recalls[cl,i1,i2])
                     accuracies[cl,i2,i1]=accuracy_class(confusions[i1,i2,:,:],cl)
                     precisions[cl,i2,i1]=precision_class(confusions[i1,i2,:,:],cl)
                     recalls[cl,i2,i1]=recall_class(confusions[i1,i2,:,:],cl)
                     fscores[cl,i2,i1]=harmonic_mean(precisions[cl,i1,i2],recalls[cl,i1,i2])
     vals_spec=np.zeros(12)
     for sp in range(12):
         vals_spec[sp]=np.mean(valeurs_line_no_diag(globAcc,sp))
     
     #Meilleur = S2
     max=7
     #Pire = RES2
     min=4

     valsGlob=np.zeros((21,2))
     valsMeilleur=np.zeros((21,2))
     valsPire=np.zeros((21,2))

     valsGlob[0]=stats(valeurs_no_diag(globAcc))
     valsMeilleur[0]=stats(valeurs_line_no_diag(globAcc,max))
     valsPire[0]=stats(valeurs_line_no_diag(globAcc,min))
    
     for cl in range(5):
         valsGlob[1+4*cl]=stats(valeurs_no_diag(accuracies[cl,:,:]))
         valsMeilleur[1+4*cl]=stats(valeurs_line_no_diag(accuracies[cl,:,:],max))
         valsPire[1+4*cl]=stats(valeurs_line_no_diag(accuracies[cl,:,:],min))
    
         valsGlob[2+4*cl]=stats(valeurs_no_diag(precisions[cl,:,:]))
         valsMeilleur[2+4*cl]=stats(valeurs_line_no_diag(precisions[cl,:,:],max))
         valsPire[2+4*cl]=stats(valeurs_line_no_diag(precisions[cl,:,:],min))
    
         valsGlob[3+4*cl]=stats(valeurs_no_diag(recalls[cl,:,:]))
         valsMeilleur[3+4*cl]=stats(valeurs_line_no_diag(recalls[cl,:,:],max))
         valsPire[3+4*cl]=stats(valeurs_line_no_diag(recalls[cl,:,:],min))
    
         valsGlob[4+4*cl]=harmonic_mean(valsGlob[2+4*cl],valsGlob[3+4*cl])
         valsMeilleur[4+4*cl]=harmonic_mean(valsMeilleur[2+4*cl],valsMeilleur[3+4*cl])
         valsPire[4+4*cl]=harmonic_mean(valsPire[2+4*cl],valsPire[3+4*cl])
    
     a=np.zeros((6,21))
     a[0,:]=valsGlob[:,0]
     a[1,:]=valsGlob[:,1]
     a[2,:]=valsPire[:,0]
     a[3,:]=valsPire[:,1]
     a[4,:]=valsMeilleur[:,0]
     a[5,:]=valsMeilleur[:,1]
     ta=dir.split("/")
     ta=ta[len(ta)-2]
     write_vals_tab2d_in_file_with_percent( a,'/home/fernandr/Bureau/ML_CEP/Tabs/tab_purple_'+ta+'.txt')
     return a[0:2,:]




def tab3d_to_tab2d(tab3d):
    return np.reshape(tab3d,(np.shape(tab3d)[0]*np.shape(tab3d)[1],np.shape(tab3d)[2]))
    
def exp_existe(exp):
    print('Experience finie et lisible ? '+exp+'TWOFOLD_'+str(10)+'-'+str(11)+'__stats_test.txt')
    try:
        with open(exp+'TWOFOLD_'+str(10)+'-'+str(11)+'__stats_test.txt'): return 1
    except IOError:
        print('Pas de fichier. Abort.')
        return 0
    
def write_vals_tab2d_in_file_with_percent(tab,nomfich):
    st=''
    print (tab)
    for x in range (np.shape(tab)[0]):
        for y in range (np.shape(tab)[1]):
            print('writing :'+str(tab[x,y]))
            st=st+toPourcent(tab[x,y])+' '
        st=st+'\n'
    fichier = open(nomfich, "w")
    fichier.write(st)
    fichier.close()
    print('tab was written in '+nomfich)        

    
def stats(vals):
    ret=np.zeros(2)
    ret[0]=np.mean(vals)
    ret[1]=np.std(vals)
    return ret

def stats_vect(vals):
    ret=np.zeros((2,np.shape(vals)[1]))
    ret[0,:]=np.mean(vals,0)
    ret[1,:]=np.std(vals,0)
    return ret




def harmonic_mean(a,b):
    return (2*a*b/(a+b))

def toPourcent(ratio):
    return str((int(round(ratio*1000))/10))+' %W'
    
def read_confusion_mat_from_full_text(exp,spec1,spec2):    
    fichier=open(exp+'TWOFOLD_'+str(spec1)+'-'+str(spec2)+'__stats_test.txt')
    contents=fichier.read()
    l1=contents.split("\n")[1].split(" ")
    l2=contents.split("\n")[2].split(" ")
    l3=contents.split("\n")[3].split(" ")
    l4=contents.split("\n")[4].split(" ")
    l5=contents.split("\n")[5].split(" ")

    mat=np.zeros((5,5))
    mat[0,:]=(l1[1],l1[3],l1[5],l1[7],l1[9])
    mat[1,:]=(l2[1],l2[3],l2[5],l2[7],l2[9])
    mat[2,:]=(l3[1],l3[3],l3[5],l3[7],l3[9])
    mat[3,:]=(l4[1],l4[3],l4[5],l4[7],l4[9])
    mat[4,:]=(l5[1],l5[3],l5[5],l5[7],l5[9])
    return mat
    

def read_confusion_mat_from_full_text_symptom(exp,sympt):    
    fichier=open(exp+'TWOFOLD_'+str(spec1)+'-'+str(spec2)+'__stats_test.txt')
    contents=fichier.read()
    l1=contents.split("\n")[1].split(" ")
    l2=contents.split("\n")[2].split(" ")
    l3=contents.split("\n")[3].split(" ")
    l4=contents.split("\n")[4].split(" ")
    l5=contents.split("\n")[5].split(" ")

    mat=np.zeros((5,5))
    mat[0,:]=(l1[1],l1[3],l1[5],l1[7],l1[9])
    mat[1,:]=(l2[1],l2[3],l2[5],l2[7],l2[9])
    mat[2,:]=(l3[1],l3[3],l3[5],l3[7],l3[9])
    mat[3,:]=(l4[1],l4[3],l4[5],l4[7],l4[9])
    mat[4,:]=(l5[1],l5[3],l5[5],l5[7],l5[9])
    return mat
    

def read_confusion_stats_from_full_text(exp,spec1,spec2):
    rep='/home/fernandr/Bureau/EX_CEDRIC/V3/RESULTS/'
    fichier=open(rep+exp+'_'+str(spec1)+'-'+str(spec2)+'__stats_test.txt')
    contents=fichier.read()
    prec=contents.split("\n")[6].split(" ")
    precisions=(prec[4],prec[6],prec[8],prec[10],prec[12])

    prec=contents.split("\n")[7].split(" ")
    recall=(prec[4],prec[6],prec[8],prec[10],prec[12])

    prec=contents.split("\n")[8].split(" ")
    accuracies=(prec[4],prec[6],prec[8],prec[10],prec[12])

    prec=contents.split("\n")[11].split("=")
    accuracy=(prec[1])



  
  



def afficher_experiences(exps):
    VminGlob=0.7
    VmaxGlob=0.9
    VminClas=0.75
    VmaxClas=0.92
    n_exp=len(exps)
    vals=np.zeros((n_exp,6))
    valsNo3=np.zeros((n_exp,6))
    valsNo4=np.zeros((n_exp,6))
    valsNo5=np.zeros((n_exp,6))
    fig, axes = plt.subplots(n_exp,6)
    for n in range(n_exp):
        exp=exps[n]
        summary=summary_accuracy_twofold(exp)
        vals[n,0]=mean_no_diag(summary)
        valsNo4[n,0]=mean_no_diag_no_i(summary,4)
        axes[n,0].imshow(summary,vmin=VminGlob,vmax=VmaxGlob)
        for i in range(5):
            summary=summary_accuracy_class_twofold(exp,i)
            vals[n,i+1]=mean_no_diag(summary)
            valsNo4[n,i+1]=mean_no_diag_no_i(summary,4)
            axes[n,1+i].imshow(summary,vmin=VminClas,vmax=VmaxClas)
    print('vals=')
    print(vals)
    print('valsNo4=')
    print(valsNo4)
    return fig



def valeurs_no_diag(mat):
    ret=np.ones(12*11)
    incr=0
    for spec1 in range(12):
        for spec2 in range(12):
            if(spec1!=spec2):
                ret[incr]=mat[spec1,spec2]
                incr=incr+1
    return ret
                
def valeurs_line_no_diag(mat,spec1):
    ret=np.ones(11)
    incr=0
    for spec2 in range(12):
        if(spec1!=spec2):
            ret[incr]=mat[spec1,spec2]
            incr=incr+1
    return ret              
                
                
def valeurs_column_no_diag(mat,spec1):
    ret=np.ones(11)
    incr=0
    for spec2 in range(12):
        if(spec1!=spec2):
            ret[incr]=mat[spec2,spec1]
            incr=incr+1
    return ret              

def mean_no_diag(summary):
    dims=summary.shape
    N_elems=dims[0]*(dims[1]-1)
    return (np.sum(summary)-np.trace(summary))/N_elems

def mean_no_diag_no_i(summary,i):
    dims=summary.shape
    N_elems=(dims[0])*(dims[1]-1)-(dims[0]*2-2)
    print ('elements :')
    print (N_elems)
    return (np.sum(summary)-np.trace(summary)-np.sum(summary[i,:])-np.sum(summary[:,i])+2*summary[i,i]  )  /N_elems


def summary_accuracy_twofold(exp):
    res_acc=np.zeros((12,12))
    for spec1 in range(12):
        for spec2 in range(12):
            if(spec1>=spec2):
                continue
            res_acc[spec1,spec2]=accuracy(read_confusion(exp,spec1,spec2))
            res_acc[spec2,spec1]=accuracy(read_confusion(exp,spec1,spec2))
            
    return res_acc




def summary_accuracy_class_twofold(exp,i):
    res_acc=np.zeros((12,12))
    for spec1 in range(12):
        for spec2 in range(12):
            if(spec1>=spec2):
                continue
            res_acc[spec1,spec2]=accuracy_class(read_confusion(exp,spec1,spec2),i)
            res_acc[spec2,spec1]=accuracy_class(read_confusion(exp,spec1,spec2),i)
            
    return res_acc



def read_confusion(exp,spec1,spec2):
    rep='/home/fernandr/Bureau/EX_CEDRIC/V3/RESULTS/'
    return np.loadtxt(rep+exp+'_'+str(spec1)+'-'+str(spec2)+'__stats_test.mat.python.txt')


def accuracy(confusion):
    su=np.sum(confusion)
    s=np.trace(confusion)
    return s/su

def accuracy_class(confusion,i):
    su=np.sum(confusion)
    li=np.sum(confusion[i,:])
    ci=np.sum(confusion[:,i])
    lici=confusion[i,i]
    return (su-li-ci+2*lici)/su

def precision_class(confusion,i):
    li=np.sum(confusion[i,:])
    lici=confusion[i,i]
    return (lici)/li


def recall_class(confusion,i):
    ci=np.sum(confusion[:,i])
    lici=confusion[i,i]
    return (lici)/ci






 
# ------- PART 1: Define a function that do a plot for one line of the dataset!
 
def make_spider( data,min,max,classes,categories, titles, colors):
    print(categories)
    print(titles)
    NC = len(categories)
    NM = len(titles)
    print('NC='+str(NC))
    print('NM='+str(NM))
    alphas=(0.0,0,0,0.0)
    # What will be the angle of each axis in the plot? (we divide the plot / number of variable)
    angles = [n / float(NC) * 2 * pi for n in range(NC)]
    angles += angles[:1]
    vals=np.zeros((NM,NC+1))
    vals[:,0:NC]=data
    vals[:,NC]=data[:,0]
    print('out1')
    
    
    # Initialise the spider plot
    ax = plt.subplot(1,1,1, polar=True)
    print('out2')
 
    # If you want the first axis to be on top:
    ax.set_theta_offset(pi / 2)
    ax.set_theta_direction(-1)
    print('out3')
 
    # Draw one axe per variable + add labels labels yet
    plt.xticks(angles[:-1], categories, color='black', size=6)
    print('out4')
 
    # Draw ylabels
    ax.set_rlabel_position(0)
    plt.yticks([20,40,60,80,100], ["20","40","60","80","100"], color="black", size=5)
    plt.ylim(0,100)
    print('out5')
 
    # Ind1
    for m in range(NM):
        print('traitement plot numero '+str(m)+' parmi '+str(NM))
        if(titles[m]!='No data used'):
            ax.plot(angles, vals[m,:], color=colors[m], linewidth=1, linestyle='solid',label=titles[m])
        #ax.fill(angles, vals[m,:], color=colors[m], alpha=alphas[m])
    print('out6')
 
    # Add a title and legend
    ax.legend(fontsize=6,loc=(0.9,0.85))
    plt.title('Classification scores VS Imaging devices' , size=8, color='k', y=1.0)
    print('out7')



def compute_spiders(config,valsYellow,min,max,classes):
    titles=('No data used','IrmPD only',  'IrmT2 only','IrmT2 and IrmPD',     'IrmT1 only','IrmT1 and IrmPD',    'IrmT1 and IrmT2', 'Rmn only',
            'X-rays only','X-rays and IrmPD',  'X-rays and IrmT2','All but IrmT1',     'X-rays and IrmT1','All but IrmT2',    'All but IrmPD', 'All Rmn and X-rays',)
    tit=()
    cols=('#d62728','#1f77b4','#8c564b','#2ca02c','#ff7f0e')
    my_dpi=200
    plt.figure(figsize=(1500/my_dpi, 800/my_dpi), dpi=my_dpi) 
    N_mods=5
    if(config==0):
        selected_mods=(8,4,2,1,15)
    if(config==1):
        selected_mods=(7,11,13,14,15)
    if(config==2):
        selected_mods=(7,8,0,0,15)
    if(config==99):
        selected_mods=(8,12,0,0,15)

    valuesMean=np.zeros((N_mods,5))
    valuesStd=np.zeros((N_mods,5))
    print('ok here')
    tit=(titles[selected_mods[0]] ,titles[selected_mods[1]] ,titles[selected_mods[2]],titles[selected_mods[3]],titles[selected_mods[4]]   )
    for m in range(N_mods):
        valuesMean[m]=valsYellow[selected_mods[m],0,:]*100
        valuesStd[m]=valsYellow[selected_mods[m],1,:]*100
        print(valuesMean[m])
        print('ok there')

    cat=('Background','Healthy wood','Deteriorated\nwood','Amadou','Bark')
    print('ok tthere')
    if(classes==4):
        cat=('Healthy wood','Deteriorated\nwood','Amadou','Bark')
        valuesMean=valuesMean[:,1:5]
        
    make_spider( valuesMean,min,max,classes,categories=cat, titles=tit ,colors=cols)



def compute_decreasing_plot_with_resolution(valsBrown,valPurple):
    print(valsBrown)
#    cols=('#1f77b4','#8c564b','#2ca02c','#ff7f0e')
    titles=('Healthy wood','Deteriorated wood','Amadou','Bark')
    
    my_dpi=150
    plt.figure(figsize=(1250/my_dpi, 1000/my_dpi), dpi=my_dpi) 
    ax = plt.subplot(1,1,1)

    plt.ylim(0,100)
    plt.xlim(0,12)
    plt.xticks([1,2,3,4,5,6,7,8,9,10],
               ["1","2","3","4","5","6","7","8","9","10"],color="black", size=8) 
    plt.yticks([20,40,60,80,100], ["20","40","60","80","100"], color="black", size=8)



    #Draw horizontal lines 
    for i in range(4):
        plt.plot([0,17], [20*(i+1),20*(i+1)], color='#cccccc',linewidth=0.6)

    #Draw Squares
    sizes=[1,5,10]
    ym=10
    fact_ech_X=0.05
    fact_ech_Y=fact_ech_X*10.5
    for i in range(3):
        xm=sizes[i]
        plt.plot([xm,xm], [0.7,ym-sizes[i]*fact_ech_Y-0.7], color='#333333',linewidth=0.6)
        if(i==0):
            ax.add_patch(Rectangle((xm-sizes[i]*fact_ech_X, ym-sizes[i]*fact_ech_Y), 
                               2*sizes[i]*fact_ech_X, 2*sizes[i]*fact_ech_Y,alpha=1,
                               facecolor='#dddddd',edgecolor='#333333',label='Pixel size'))      
        else:
            ax.add_patch(Rectangle((xm-sizes[i]*fact_ech_X, ym-sizes[i]*fact_ech_Y), 
                               2*sizes[i]*fact_ech_X, 2*sizes[i]*fact_ech_Y,alpha=1,
                               facecolor='#dddddd',edgecolor='#333333'))      

#    ax.text(sizes[0]-0.5, ym+1+sizes[0]*fact_ech_Y,'Pixel size',size=7)
#    ax.text(sizes[1]-0.5, ym+1+sizes[1]*fact_ech_Y,'Pixel size',size=7)
#    ax.text(sizes[2]-0.4, ym+1+sizes[2]*fact_ech_Y,'Pixel size',size=7)

    t=np.arange(1, 11, 1)
    t=np.double(t)
    t=np.insert(t,0,0.722)
    
    vals_healthy=valsBrown[:,0,8]*100
    vals_healthy=np.insert(vals_healthy,0,valsPurple[0,8]*100)

    vals_deter=valsBrown[:,0,12]*100
    vals_deter=np.insert(vals_deter,0,valsPurple[0,12]*100)

    vals_amad=valsBrown[:,0,16]*100
    vals_amad=np.insert(vals_amad,0,valsPurple[0,16]*100)

    vals_bark=valsBrown[:,0,20]*100
    vals_bark=np.insert(vals_bark,0,valsPurple[0,20]*100)



    plt.plot(t, vals_healthy,label=titles[0],color='#34c924') # 'go',
    plt.scatter(t, vals_healthy,edgecolor = 'black',facecolor='#34c924') # 'go',
    plt.plot(t, vals_deter, label=titles[1],color='#333333')
    plt.scatter(t, vals_deter,edgecolor = 'black',facecolor='#333333')
    plt.plot(t, vals_amad, label=titles[2],color='#EE0606')
    plt.scatter(t, vals_amad,edgecolor = 'black',facecolor='#EE0606')
#    plt.plot(t, vals_bark, label=titles[3],color='#87CEEB')
#    plt.scatter(t, vals_bark,edgecolor = 'black',facecolor='#87CEEB')
#    plt.plot(t, vals_deter, 'bs', label=titles[1])
#    plt.plot(t, vals_amad, 'rX',label=titles[2])
#    plt.plot(t, vals_bark, 'k^',label=titles[3])

    ax.legend(fontsize=8,loc=(0.05,0.3))#    loc=(1.2,0.5)
    plt.ylabel('Classification F-score (%)')
    plt.xlabel("Pixel size (mm)")

  #  plt.title('Tissues classification scores VS images subsampling factor' , size=8, color='k', y=1.0)



def read_tissues_volumes(file,inverse=0):
    fichier=open(file)
    contents=fichier.read()
    l1=contents.split("\n")[1].split(" ")
    Z=len(l1)
    mat=np.zeros((11,Z))
    #l0 : sain
    #l1 : noir
    #l2 : amad
    #l3 : ecor

    #l4 : sain/sain+noir+amad
    #l5 : noir/sain+noir+amad
    #l6 : amad/sain+noir+amad


    for tis in range(4):
        mat[tis,:]=contents.split("\n")[tis+1].split(" ")
        mat[tis,:]=(mat[tis,:]*0.005219)/3
        mat[7+tis,:]=contents.split("\n")[tis+1].split(" ")
    for z in range(np.shape(mat)[1]):
        if (mat[0,z]+ mat[1,z]+ mat[2,z] > 0 ):
            for tis in range(3):
                mat[4+tis,:]= 100*mat[tis,:]/( mat[0,:]+ mat[1,:]+ mat[2,:])
    if(inverse==1):
        mat=np.fliplr(mat)
    return Z,mat


def read_healthy_volume(file):
    fichier=open(file)
    contents=fichier.read()
    l1=contents.split("\n")[1].split(" ")
    Z=len(l1)
    mat=np.zeros((1,Z))
    #l0 : sain
    #l1 : noir
    #l2 : amad
    #l3 : ecor

    #l4 : sain/sain+noir+amad
    #l5 : noir/sain+noir+amad
    #l6 : amad/sain+noir+amad


    for tis in range(1):
        mat[tis,:]=contents.split("\n")[tis+1].split(" ")
        mat[tis,:]=mat[tis,:]*0.0722
    return Z,mat



def compute_both_ratio(specimens,slice_numbers):
    min_x=-10
    max_x=0
    colors=['#238c00' , '#51b300' , '#51f500',         '#1111AA' , '#2222CC' , '#4444FF' ,         '#ad4eaf' , '#cf4eca' , '#f34efa' ,          '#bb0e0e' , '#db0e0e' , '#fb0e0e']
    my_dpi=150

    valsAmad=np.zeros(12)
    valsHealth=np.zeros(12)
    plt.figure(figsize=(1250/my_dpi, 600/my_dpi), dpi=my_dpi) 
    ax = plt.subplot(1,1,1)
    plt.ylim(0,100)
    plt.xlim(min_x,max_x)
    plt.ylabel('Healthy wood surface ratio (%)')
    plt.xlabel("Height (cm), relative to trunk head")
    ax.text(0,10,'Trunk top',size=7)
    for spec in range(12):    
        z,mat=read_tissues_volumes('/home/fernandr/Bureau/ML_CEP/RESULTS/EXP_6_ON_STACKS/'+specimens[spec]+'/countTab.txt')
        t=(np.arange(0, z, 1)-(z-slice_numbers[spec]))/10.0
        t=np.double(t)             
        for i in range(len(t)):
            if((t[i]>=min_x) & (t[i]<=max_x)):
                valsHealth[spec]=valsHealth[spec]+mat[4,i]
                valsAmad[spec]=valsAmad[spec]+mat[6,i]
        plt.plot(t, mat[4,:],label=specimens[spec],color=colors[spec]) # 'go',
        print(specimens[spec]+'='+str(np.nansum(mat[4,:])))
    plt.plot([0,0], [0,100], color='#cccccc',linewidth=0.6)
    ax.legend(fontsize=8,loc=(0.05,0.05))#    loc=(1.2,0.5)

    plt.figure(figsize=(1250/my_dpi, 600/my_dpi), dpi=my_dpi) 
    ax2 = plt.subplot(1,1,1)
    plt.ylim(0,100)
    plt.xlim(min_x,max_x)
    plt.ylabel('Amadou surface ratio (%)')
    plt.xlabel("Height (cm), relative to trunk head")
    ax2.text(0,10,'Trunk top',size=7)
    for spec in range(12):
        z,mat=read_tissues_volumes('/home/fernandr/Bureau/ML_CEP/RESULTS/EXP_6_ON_STACKS/'+specimens[spec]+'/countTab.txt')
        t=(np.arange(0, z, 1)-(z-slice_numbers[spec]))/10.0
        t=np.double(t)
        plt.plot(t, mat[6,:],label=specimens[spec],color=colors[spec]) # 'go',
        print(specimens[spec]+'='+str(np.nansum(mat[6,:])))
    ax2.legend(fontsize=8,loc=(0.05,0.3))#    loc=(1.2,0.5)
    plt.plot([0,0], [0,100], color='#cccccc',linewidth=0.6)

    norma=101
    valsAmad=valsAmad/norma
    valsHealth=valsHealth/norma
    print('')
    print('HEALTH=')
    print(valsHealth)
    print('AMADOU=')
    print(valsAmad)

    
    plt.figure(figsize=(1250/my_dpi, 600/my_dpi), dpi=my_dpi) 
    ax3 = plt.subplot(1,1,1)
    plt.ylim(0,100)
    plt.xlim(0,40)
    plt.ylabel('Healthy wood volume (%)')
    plt.xlabel("Amadou volume (%)")
    for spec in range(12):
        plt.plot(valsAmad[spec], valsHealth[spec],'o',label=specimens[spec],color=colors[spec]) # 'go',
    ax3.legend(fontsize=8,loc=(0.05,0.05))#    loc=(1.2,0.5)










def compute_both_chamfer_center(specimens):
    min_x=0
    x0=0
    max_x=20
    xf=30
    colors=['#238c00' , '#51b300' , '#51f500',         '#1111AA' , '#2222CC' , '#4444FF' ,         '#ad4eaf' , '#cf4eca' , '#f34efa' ,          '#bb0e0e' , '#db0e0e' , '#fb0e0e']
    my_dpi=150

    valsAmad=np.zeros(12)
    valsHealth=np.zeros(12)
    valsNecr=np.zeros(12)
    plt.figure(figsize=(1250/my_dpi, 600/my_dpi), dpi=my_dpi) 
    ax = plt.subplot(1,1,1)
    plt.ylim(0,100)
    plt.xlim(min_x,max_x)
    plt.ylabel('Healthy wood surface ratio (%)')
    plt.xlabel("Height (cm), relative to trunk head")
    for spec in range(12):    
        z,mat=read_tissues_volumes('/home/fernandr/Bureau/ML_CEP/RESULTS/EXP_6_ON_STACKS/'+specimens[spec]+'/countTabGeodesicCenter.txt')
        t=(np.arange(min_x, max_x, 0.3))
        t=np.double(t)             
        print('valeurs : '+str(sum(mat[0,x0:xf]))+','+str(sum(mat[1,x0:xf]))+','+str(sum(mat[2,x0:xf])))
        valsHealth[spec]=100*sum(mat[0,x0:xf])/(sum(mat[0,x0:xf])+sum(mat[1,x0:xf])+sum(mat[2,x0:xf]))
        valsNecr[spec]=100*sum(mat[1,x0:xf])/(sum(mat[0,x0:xf])+sum(mat[1,x0:xf])+sum(mat[2,x0:xf]))
        valsAmad[spec]=100*sum(mat[2,x0:xf])/(sum(mat[0,x0:xf])+sum(mat[1,x0:xf])+sum(mat[2,x0:xf]))
        plt.plot(t, mat[4,0:67],label=specimens[spec],color=colors[spec]) # 'go',
        print(specimens[spec]+'='+str(np.nansum(mat[4,:])))
    ax.legend(fontsize=8,loc=(0.05,0.05))#    loc=(1.2,0.5)

    plt.figure(figsize=(1250/my_dpi, 600/my_dpi), dpi=my_dpi) 
    ax2 = plt.subplot(1,1,1)
    plt.ylim(0,100)
    plt.xlim(min_x,max_x)
    plt.ylabel('Amadou surface ratio (%)')
    plt.xlabel("Height (cm), relative to trunk head")
    ax2.text(0,10,'Trunk top',size=7)
    for spec in range(12):
        z,mat=read_tissues_volumes('/home/fernandr/Bureau/ML_CEP/RESULTS/EXP_6_ON_STACKS/'+specimens[spec]+'/countTabGeodesicFull.txt')
        t=(np.arange(min_x, max_x, 0.3))
        t=np.double(t)
        plt.plot(t, mat[6,0:67],label=specimens[spec],color=colors[spec]) # 'go',
        print(specimens[spec]+'='+str(np.nansum(mat[6,:])))
    ax2.legend(fontsize=8,loc=(0.05,0.3))#    loc=(1.2,0.5)

    
    print('')
    print('HEALTH=')
    print(valsHealth)
    print('AMADOU=')
    print(valsAmad)

    
    plt.figure(figsize=(900/my_dpi, 600/my_dpi), dpi=my_dpi) 
    ax3 = plt.subplot(1,1,1)
    plt.ylim(0,80)
    plt.xlim(0,30)
    plt.ylabel('Healthy wood volume (%)')
    plt.xlabel("Amadou volume (%)")
    for spec in range(12):
        plt.plot(valsAmad[spec], valsHealth[spec],'o',label=specimens[spec],color=colors[spec]) # 'go',
    ax3.legend(fontsize=8,loc=(0.70,0.50))#    loc=(1.2,0.5)


    plt.figure(figsize=(900/my_dpi, 600/my_dpi), dpi=my_dpi) 
    ax6 = plt.subplot(1,1,1)
    plt.ylim(0,10)
    plt.xlim(-10,60)
    plt.ylabel('rien (%)')
    plt.xlabel("Sain - necrose - 4*amadou (%)")
    for spec in range(12):
        plt.plot(valsHealth[spec]-0*valsNecr[spec]-4*valsAmad[spec],2,'o',label=specimens[spec],color=colors[spec]) # 'go',
    ax6.legend(fontsize=8,loc=(0.70,0.50))#    loc=(1.2,0.5)



    

















def compute_stats_health_plot_for_one(specimen,top_hat_slice_number):
    min_x=-10
    max_x=5
    z,mat=read_tissues_volumes('/home/fernandr/Bureau/ML_CEP/RESULTS/EXP_6_ON_STACKS/'+specimen+'/countTab.txt')
    t=(np.arange(0, z, 1)-(z-top_hat_slice_number))/10.0
    max=np.nanmax(mat)

    titles=('Healthy wood','Deteriorated wood','Amadou','Bark')    
    titles2=('Healthy wood ratio','Deteriorated wood ratio','Amadou ratio')    
    my_dpi=150
    plt.figure(figsize=(1250/my_dpi, 600/my_dpi), dpi=my_dpi) 

    ax = plt.subplot(2,1,1)
    plt.ylim(0,max)
    plt.xlim(min_x,max_x)
    t=np.double(t)
    plt.plot(t, mat[0,:],label=titles[0],color='#34c924') # 'go',
    plt.plot(t, mat[1,:], label=titles[1],color='#333333')
    plt.plot(t, mat[2,:], label=titles[2],color='#EE0606')
    plt.plot(t, mat[3,:], label=titles[3],color='#87CEEB')
    ax.legend(fontsize=8,loc=(0.05,0.3))#    loc=(1.2,0.5)
    plt.ylabel('Surface (cm^2)')
    plt.xlabel("Slice height relatively to trunk head summit (cm)")
    plt.plot([0,0], [0,max], color='#cccccc',linewidth=0.6)
    ax.text(0,max/10,'Trunk top',size=7)


    ax2 = plt.subplot(2,1,2)
    plt.ylim(0,100)
    plt.xlim(min_x,max_x)
    t=np.double(t)
    plt.plot(t, mat[4,:],label=titles2[0],color='#34c924') # 'go',
    plt.plot(t, mat[5,:], label=titles2[1],color='#333333')
    plt.plot(t, mat[6,:], label=titles2[2],color='#EE0606')
    ax2.legend(fontsize=8,loc=(0.05,0.3))#    loc=(1.2,0.5)
    plt.ylabel('Surface ratio (%)')
    plt.xlabel("Slice height relatively to trunk head summit (cm)")
    plt.plot([0,0], [0,100], color='#cccccc',linewidth=0.6)
    ax2.text(0,100/10,'Trunk top',size=7)























def compute_both_chamfer_cambium(specimens):
    min_x=-20
    x0=15
    max_x=10
    xf=66
    colors=['#238c00' , '#51b300' , '#51f500',         '#1111AA' , '#2222CC' , '#4444FF' ,         '#ad4eaf' , '#cf4eca' , '#f34efa' ,          '#bb0e0e' , '#db0e0e' , '#fb0e0e']
    my_dpi=150

    plt.figure(figsize=(1250/my_dpi, 600/my_dpi), dpi=my_dpi) 
    ax = plt.subplot(1,1,1)
    plt.xlim(min_x,max_x)
    plt.ylim(0,100)
    plt.ylabel('Cambium length (mm)')
    plt.xlabel("Height (cm), relative to trunk head")
    mmax=0
    for spec in range(12):    
        z,mat=read_healthy_volume('/home/fernandr/Bureau/ML_CEP/RESULTS/EXP_6_ON_STACKS/'+specimens[spec]+'/countTabGeodesicCambiumHealthy.txt')
        t=(np.arange(-20, 10, 0.3))
        t=np.double(t)             
        plt.plot(t, mat[0,:],label=specimens[spec],color=colors[spec]) # 'go',
        if(np.max(mat[0,:])>mmax):
            mmax=np.max(mat[0,:])
        print(specimens[spec]+'='+str(np.nansum(mat[0,:])))
    plt.ylim(0,mmax)
    ax.legend(fontsize=8,loc=(0.05,0.05))#    loc=(1.2,0.5)

    mmax=0
    plt.figure(figsize=(1250/my_dpi, 600/my_dpi), dpi=my_dpi) 
    ax = plt.subplot(1,1,1)
    plt.xlim(min_x,max_x)
    plt.ylim(0,100)
    plt.ylabel('Necrose length (mm)')
    plt.xlabel("Height (cm), relative to trunk head")
    for spec in range(12):    
        z,mat=read_healthy_volume('/home/fernandr/Bureau/ML_CEP/RESULTS/EXP_6_ON_STACKS/'+specimens[spec]+'/countTabGeodesicCambiumNecrose.txt')
        t=(np.arange(-20, 10, 0.3))
        t=np.double(t)             
        plt.plot(t, mat[0,:],label=specimens[spec],color=colors[spec]) # 'go',
        if(np.max(mat[0,:])>mmax):
            mmax=np.max(mat[0,:])
        print(specimens[spec]+'='+str(np.nansum(mat[0,:])))
    plt.ylim(0,mmax)
    ax.legend(fontsize=8,loc=(0.05,0.05))#    loc=(1.2,0.5)

    mmax=0
    plt.figure(figsize=(1250/my_dpi, 600/my_dpi), dpi=my_dpi) 
    ax = plt.subplot(1,1,1)
    plt.xlim(min_x,max_x)
    plt.ylim(0,100)
    plt.ylabel('Necrose length (mm)')
    plt.xlabel("Height (cm), relative to trunk head")
    for spec in range(12):    
        z,mat=read_healthy_volume('/home/fernandr/Bureau/ML_CEP/RESULTS/EXP_6_ON_STACKS/'+specimens[spec]+'/countTabGeodesicCambiumNecrose.txt')
        t=(np.arange(-20, 10, 0.3))
        t=np.double(t)             
        plt.plot(t, mat[0,:],label=specimens[spec],color=colors[spec]) # 'go',
        if(np.max(mat[0,:])>mmax):
            mmax=np.max(mat[0,:])
        print(specimens[spec]+'='+str(np.nansum(mat[0,:])))
    plt.ylim(0,mmax)
    ax.legend(fontsize=8,loc=(0.05,0.05))#    loc=(1.2,0.5)

    plt.figure(figsize=(1250/my_dpi, 600/my_dpi), dpi=my_dpi) 
    ax = plt.subplot(1,1,1)
    plt.xlim(min_x,max_x)
    plt.ylim(0,100)
    plt.ylabel('Healthy fraction (%)')
    plt.xlabel("Height (cm), relative to trunk head")
    for spec in range(12):    
        zH,matH=read_healthy_volume('/home/fernandr/Bureau/ML_CEP/RESULTS/EXP_6_ON_STACKS/'+specimens[spec]+'/countTabGeodesicCambiumHealthy.txt')
        zN,matN=read_healthy_volume('/home/fernandr/Bureau/ML_CEP/RESULTS/EXP_6_ON_STACKS/'+specimens[spec]+'/countTabGeodesicCambiumNecrose.txt')
        t=(np.arange(-20, 10, 0.3))
        t=np.double(t)
        print('matH=')
        print(matH)
        print('matN=')
        print(matN)
        a= 100*matH/(matH+matN)
        print('a')
        print(a)
        plt.plot(t, a[0,:],label=specimens[spec],color=colors[spec]) # 'go',
        print(specimens[spec]+'='+str(np.nansum(mat[0,:])))
    ax.legend(fontsize=8,loc=(0.05,0.05))#    loc=(1.2,0.5)
































def compute_both_chamfer(specimens,listFigures):
    min_x=-20
    max_x=10
    colors=['#238c00' , '#51b300' , '#51f500',         '#1111AA' , '#2222CC' , '#4444FF' ,         '#ad4eaf' , '#cf4eca' , '#f34efa' ,          '#bb0e0e' , '#db0e0e' , '#fb0e0e']
    colors2=['#238c00' , '#51b300' , '#51f500',           '#ad4eaf' , '#cf4eca' , '#f34efa' ,       '#1111AA' , '#2222CC' , '#4444FF' ,          '#bb0e0e' , '#db0e0e' , '#fb0e0e']
    my_dpi=150

    doBasicRatios=listFigures[0]
    doVerticalAmadouHealthy=listFigures[1]
    doVerticalAmadouHealthyCat=listFigures[2]
    doVerticalAmadouNecroseCat=listFigures[3]
    doVerticalNecroseHealthyCat=listFigures[4]
    doVerticalAmadouCat=listFigures[5]
    doVerticalHealthyCat=listFigures[6]
    doVerticalNecroseCat=listFigures[7]
    doVerticalHealthyOverOthersCat=listFigures[8]
    do2D6=listFigures[9]
    do2D3=listFigures[10]
    hideFirst=listFigures[11]
    doSurfaceCat,doRatioCat,doCatCatRatio=listFigures[12],listFigures[13],listFigures[14]
    doVolumes=listFigures[15]
    x0s3=[30,45,60]
    xfs3=[67,67,67]
    x0s6=[30,45,60,66,35,50,65,69]
    xfs6=[67,67,67,67,70,70,70,70]

    valsAmad3=np.zeros((12,len(x0s3)))
    valsHealth3=np.zeros((12,len(x0s3)))
    valsNecr3=np.zeros((12,len(x0s3)))
    valsAmad6=np.zeros((12,len(x0s6)))
    valsHealth6=np.zeros((12,len(x0s6)))
    valsNecr6=np.zeros((12,len(x0s6)))

    if(doBasicRatios==1):
        # SURFACE RATIO BETWEEN HEALTHY AND GLOBAL
        plt.figure(figsize=(1250/my_dpi, 600/my_dpi), dpi=my_dpi) 
        ax = plt.subplot(1,1,1)
        plt.xlim(min_x,max_x)
        plt.ylabel('Healthy wood surface ratio (%)A')
        plt.xlabel("Height (cm), relative to trunk head")
        mmax=0
        for spec in range(12):    
            z,mat=read_tissues_volumes('/home/fernandr/Bureau/ML_CEP/RESULTS/EXP_6_ON_STACKS/'+specimens[spec]+'/countTabGeodesicFull.txt',inverse=0)
            print('')
            print('SPECIMEN '+str(spec))
            print(np.shape(mat))
            print(mat[0,:])
            t=(np.arange(-20, 10, 0.3))
            t=np.double(t)             
            #print('valeurs : '+str(sum(mat[0,x0s[i]:xfs[i]]))+','+str(sum(mat[1,x0s[i]:xfs[i]]))+','+str(sum(mat[2,x0s[i]:xfs[i]])))
            for i in range(len(x0s3)):
                valsHealth3[spec,i]=100*sum(mat[0,x0s3[i]:xfs3[i]])/(sum(mat[0,x0s3[i]:xfs3[i]])+sum(mat[1,x0s3[i]:xfs3[i]])+sum(mat[2,x0s3[i]:xfs3[i]]))
                valsNecr3[spec,i]=100*sum(mat[1,x0s3[i]:xfs3[i]])/(sum(mat[0,x0s3[i]:xfs3[i]])+sum(mat[1,x0s3[i]:xfs3[i]])+sum(mat[2,x0s3[i]:xfs3[i]]))
                valsAmad3[spec,i]=100*sum(mat[2,x0s3[i]:xfs3[i]])/(sum(mat[0,x0s3[i]:xfs3[i]])+sum(mat[1,x0s3[i]:xfs3[i]])+sum(mat[2,x0s3[i]:xfs3[i]]))
            for i in range(len(x0s6)):
                valsHealth6[spec,i]=100*sum(mat[0,x0s6[i]:xfs6[i]])/(sum(mat[0,x0s6[i]:xfs6[i]])+sum(mat[1,x0s6[i]:xfs6[i]])+sum(mat[2,x0s6[i]:xfs6[i]]))
                valsNecr6[spec,i]=100*sum(mat[1,x0s6[i]:xfs6[i]])/(sum(mat[0,x0s6[i]:xfs6[i]])+sum(mat[1,x0s6[i]:xfs6[i]])+sum(mat[2,x0s6[i]:xfs6[i]]))
                valsAmad6[spec,i]=100*sum(mat[2,x0s6[i]:xfs6[i]])/(sum(mat[0,x0s6[i]:xfs6[i]])+sum(mat[1,x0s6[i]:xfs6[i]])+sum(mat[2,x0s6[i]:xfs6[i]]))
            plt.plot(t, mat[0,:],label=specimens[spec],color=colors[spec]) # 'go',
        plt.ylim(0,500)
        ax.legend(fontsize=8,loc=(0.05,0.05))#    loc=(1.2,0.5)
    
    
        # SURFACE RATIO BETWEEN AMADOU AND GLOBAL
        mmax=0
        plt.figure(figsize=(1250/my_dpi, 600/my_dpi), dpi=my_dpi) 
        ax2 = plt.subplot(1,1,1)
        plt.xlim(min_x,max_x)
        plt.ylabel('Amadou surface ratio (%)B')
        plt.xlabel("Height (cm), relative to trunk head")
        ax2.text(0,10,'Trunk top',size=7)
        for spec in range(12):
            z,mat=read_tissues_volumes('/home/fernandr/Bureau/ML_CEP/RESULTS/EXP_6_ON_STACKS/'+specimens[spec]+'/countTabGeodesicFull.txt',inverse=0)
            t=(np.arange(-20, 10, 0.3))
            t=np.double(t)
            plt.plot(t, mat[6,:],label=specimens[spec],color=colors[spec]) # 'go',
            print(specimens[spec]+'='+str(np.nansum(mat[2,:])))
            if(np.max(mat[2,:])>mmax):
                mmax=np.max(mat[2,:])
        plt.ylim(0,mmax)
        ax2.legend(fontsize=8,loc=(0.05,0.3))#    loc=(1.2,0.5)
    
    
        # SURFACE RATIO BETWEEN NECROSE AND GLOBAL
        mmax=0
        plt.figure(figsize=(1250/my_dpi, 600/my_dpi), dpi=my_dpi) 
        ax2 = plt.subplot(1,1,1)
        plt.xlim(min_x,max_x)
        plt.ylabel('Necrose surface ratio (%)C')
        plt.xlabel("Height (cm), relative to trunk head")
        ax2.text(0,10,'Trunk top',size=7)
        for spec in range(12):
            z,mat=read_tissues_volumes('/home/fernandr/Bureau/ML_CEP/RESULTS/EXP_6_ON_STACKS/'+specimens[spec]+'/countTabGeodesicFull.txt',inverse=0)
            t=(np.arange(-20, 10, 0.3))
            t=np.double(t)
            plt.plot(t, mat[5,:],label=specimens[spec],color=colors[spec]) # 'go',
            print(specimens[spec]+'='+str(np.nansum(mat[2,:])))
            if(np.max(mat[5,:])>mmax):
                mmax=np.max(mat[5,:])
        plt.ylim(0,mmax)
        ax2.legend(fontsize=8,loc=(0.05,0.3))#    loc=(1.2,0.5)





    if(doVerticalAmadouHealthy==1):
        # SURFACE RATIO BETWEEN AMADOU AND HEALTHY
        mmax=0
        plt.figure(figsize=(500/my_dpi, 1000/my_dpi), dpi=my_dpi) 
        ax2 = plt.subplot(1,1,1)
        plt.ylim(min_x,max_x)
        plt.xlabel('Amadou / Healthy surface ratio')
        plt.ylabel("Height (cm), relative to trunk head")
        for spec in range(12):
            z,mat=read_tissues_volumes('/home/fernandr/Bureau/ML_CEP/RESULTS/EXP_6_ON_STACKS/'+specimens[spec]+'/countTabGeodesicFull.txt',inverse=0)
            t=(np.arange(-20, 10, 0.3))
            t=np.double(t)
            plt.plot(mat[6,:]/mat[4,:],t,label=specimens[spec],color=colors[spec]) # 'go',
            if(np.max(mat[6,:]/mat[4,:])>mmax):
                mmax=np.max(mat[6,:]/mat[4,:])
        plt.xlim(0,3)
#        plt.yticks([-20,-15,-10,-5,0,5,10],["-20","-15","-10","-5","0","5","10"], color="black", size=8)
        ax2.legend(fontsize=8,loc=(2,-20))#    loc=(1.2,0.5)
        plt.plot([1,1],[min_x,max_x], color='#cccccc',linewidth=0.6)
        plt.plot([0,3],[0,0], color='#cccccc',linewidth=1.0)
        ax2.legend(fontsize=8,loc=(0.05,0.3))#    loc=(1.2,0.5)







    if(do2D6==1):   
        plt.figure(figsize=(900/my_dpi, 600/my_dpi), dpi=my_dpi) 
        for i in range (len(x0s6)):
            ax3 = plt.subplot(2,4,(i+1))
            plt.ylim(0,100)
            plt.xlim(0,100)
            markers=['^','o','s']
            plt.ylabel('Fraction saine (%)'+str(int(x0s6[i]*0.3-20))+' -> '+str(int(xfs6[i]*0.3-20)))
            plt.xlabel("Fraction toxique (%)")
            for spec in range(12):
                print('')
                print('')
                print('')
                print('i='+str(i))
                print('spec='+str(spec))
                print('AMAD=')
                print(valsAmad6[spec,i])
                print('NECR=')
                print(valsNecr6[spec,i])
                print('HEALTH=')
                print(valsHealth6[spec,i])
                plt.scatter(valsAmad6[spec,i], valsHealth6[spec,i],label=specimens[spec],facecolor=colors[3*(spec//3)+2],marker=markers[spec%3],edgecolor='#000000') # 'go',
     #       ax3.legend(fontsize=8,loc=(0.70,0.50))#    loc=(1.2,0.5)
            plt.plot([0,30],[100,70])

    plt.figure(figsize=(900/my_dpi, 600/my_dpi), dpi=my_dpi) 
    i=3
    ax3 = plt.subplot(1,1,1)
    plt.ylim(0,100)
    plt.xlim(0,40)
    markers=['^','o','s']
    plt.ylabel('Healthy volume ratio (%)')
    plt.xlabel("Amadou volume ratio (%)")
    print(specimens)
    specimens2=['AS1','AS2','AS3',   'RES1','RES2','RES3',  'S1','S2','S3',  'APO1','APO2','APO3']
    lookuptable=(0,1,2,6,7,8,3,4,5,9,10,11)

    for spec in range(12):
          
        plt.scatter(valsAmad6[lookuptable[spec],i], valsHealth6[lookuptable[spec],i],label=specimens2[lookuptable[spec]],facecolor=colors[3*(spec//3)+2],marker=markers[spec%3],edgecolor='#000000') # 'go',
        ax3.legend(fontsize=8,loc=(0.70,0.41))#    loc=(1.2,0.5)
    #plt.plot([0,40],[100,60])




    if(do2D3==1):   
        plt.figure(figsize=(900/my_dpi, 600/my_dpi), dpi=my_dpi) 
        for i in range (len(x0s3)):
            ax3 = plt.subplot(1,3,(i+1))
            plt.ylim(0,100)
            plt.xlim(0,35)
            markers=['^','o','s']
            plt.ylabel('Fraction saine (%)'+str(int(x0s3[i]*0.3-20))+' -> '+str(int(xfs3[i]*0.3-20)))
            plt.xlabel("Fraction toxique (%)")
            for spec in range(12):
                plt.scatter(valsAmad3[spec,i], valsHealth3[spec,i],label=specimens[spec],facecolor=colors[3*(spec//3)+2],marker=markers[spec%3],edgecolor='#000000') # 'go',
     #       ax3.legend(fontsize=8,loc=(0.70,0.50))#    loc=(1.2,0.5)
            plt.plot([0,30],[100,70])

    if(hideFirst):
        close('all')










    if(doCatCatRatio==1):
        indices=[[6,-1,4],[5,-1,4],[5,6,4]]
        indices=np.array(indices)
        texts=['Amadou / Healthy surface ratio (%)','Necrose / Healthy surface ratio (%)','Unhealthy(Necrose + Amadou) / Healthy surface ratio (%)']
        lims_x=np.array([5,20,20])
        for tissue in range(3):
            lim_x=lims_x[tissue]
            print('pouet')
            symp=['Asymptomatic','Resilient','Symptomatic','Apoplectic']
            symp2=['Asymptomatic','Symptomatic','Resilient','Apoplectic']
            lookuptable=(0,2,1,3)
            # SURFACE RATIO BETWEEN AMADOU AND HEALTHY VERTICAL
            mmax=0
            plt.figure(figsize=(750/my_dpi, 1000/my_dpi), dpi=my_dpi) 
            ax2 = plt.subplot(1,1,1)
            plt.ylim(min_x,max_x)
            plt.xlabel(texts[tissue])
            plt.ylabel("Height (cm), relative to trunk head")
            alpha_sympt=[0.4,0.3,0.3,0.25]
            for sympt2 in range(4):
                sympt=lookuptable[sympt2]
                z1,mat1=read_tissues_volumes('/home/fernandr/Bureau/ML_CEP/RESULTS/EXP_6_ON_STACKS/'+specimens[sympt*3]+'/countTabGeodesicFull.txt',inverse=0)
                z2,mat2=read_tissues_volumes('/home/fernandr/Bureau/ML_CEP/RESULTS/EXP_6_ON_STACKS/'+specimens[sympt*3+1]+'/countTabGeodesicFull.txt',inverse=0)
                z3,mat3=read_tissues_volumes('/home/fernandr/Bureau/ML_CEP/RESULTS/EXP_6_ON_STACKS/'+specimens[sympt*3+2]+'/countTabGeodesicFull.txt',inverse=0)
                t=(np.arange(-20, 5, 0.3))
                n_t=len(t)
                t=np.double(t)
                if(indices[tissue,1]==-1):
                    vect=[mat1[indices[tissue,0],0:n_t]/mat1[indices[tissue,2],0:n_t],mat2[indices[tissue,0],0:n_t]/mat2[indices[tissue,2],0:n_t], mat3[indices[tissue,0],0:n_t]/mat3[indices[tissue,2],0:n_t]]
                else:
                    vect=[(mat1[indices[tissue,0],0:n_t]+mat1[indices[tissue,1],0:n_t])/mat1[indices[tissue,2],0:n_t],(mat2[indices[tissue,0],0:n_t]+mat2[indices[tissue,1],0:n_t])/mat2[indices[tissue,2],0:n_t], (mat3[indices[tissue,0],0:n_t]+mat3[indices[tissue,1],0:n_t])/mat3[indices[tissue,2],0:n_t]]
                means=np.mean(vect,axis=0)
                stds=np.std(vect,axis=0)
                plt.fill_betweenx(t, means-stds, means+stds,color=colors[sympt2*3+1], alpha=alpha_sympt[sympt2])
                plt.plot(means,t,label=symp[sympt],color=colors[sympt2*3+1]) # 'go',
                
            plt.xlim(0,lim_x)
            plt.ylim(-20,9)
     #       plt.yticks([-20,-15,-10,-5,0,5,10],["-20","-15","-10","-5","0\n(Trunk top)","5","10"], color="black", size=8)
            ax2.legend(fontsize=8)#    loc=(1.2,0.5)
            plt.plot([1,1],[min_x,max_x], color='#cccccc',linewidth=0.6)
            plt.plot([0,lim_x],[0,0], '--',color='#111111',linewidth=1.0)
            ax2.text(lim_x*0.7,3.0,'Branches',size=12,color='#111111')
            ax2.text(lim_x*0.75,-4.4,'Trunk',size=12,color='#111111')
            ax2.text(lim_x*0.09,-18,'To rootstock',size=9,color='#111111')
            ax2.text(lim_x*0.09,7,'To grapes',size=9,color='#111111')
            arr = Arrow(lim_x*0.075, -16, 0, -3, edgecolor='black',facecolor='black',width=lim_x*0.04)
            arr2 = Arrow(lim_x*0.075, 6, 0, 3, edgecolor='black',facecolor='black',width=lim_x*0.04)
            ax2.add_patch(arr)
            ax2.add_patch(arr2)
    #        ax2.legend(fontsize=8,loc=(2.0,-12))





    

    if((doRatioCat==1) | (doSurfaceCat==1)):
        indices=[]
        texts=[]
        lims_x=np.array([90,90,70,120,120,60])
        if(doRatioCat):
            indices=[4,5,6]
            texts=['Healthy ratio (%)','Necrose ratio (%)','Amadou ratio (%)']
        if(doSurfaceCat):
            indices=[0,1,2]
            texts=['Healthy section (cm²)','Necrose section (cm²)','Amadou section (cm²)']
        if(doSurfaceCat & doRatioCat):
            indices=[0,1,2,4,5,6]
            texts=['Healthy section (cm²)','Necrose section (cm²)','Amadou section (cm²)','Healthy ratio (%)','Necrose ratio (%)','Amadou ratio (%)']
        indices=np.array(indices)
        for tissue in range(len(indices)):
            
            print('Gestion tissu '+str(tissue))
            lim_x=lims_x[tissue]
            symp=['Asymptomatic','Resilient','Symptomatic','Apoplectic']
            symp2=['Asymptomatic','Symptomatic','Resilient','Apoplectic']
            lookuptable=(0,2,1,3)
            # SURFACE RATIO BETWEEN AMADOU AND HEALTHY VERTICAL
            mmax=0
            plt.figure(figsize=(750/my_dpi, 1000/my_dpi), dpi=my_dpi) 
            ax2 = plt.subplot(1,1,1)
            plt.ylim(min_x,max_x)
            plt.xlabel(''+str(texts[tissue])+'')
            plt.ylabel("Height (cm), relative to trunk head")
            alpha_sympt=[0.4,0.3,0.3,0.25]
            for sympt2 in range(4):
                sympt=lookuptable[sympt2]
                z1,mat1=read_tissues_volumes('/home/fernandr/Bureau/ML_CEP/RESULTS/EXP_6_ON_STACKS/'+specimens[sympt*3]+'/countTabGeodesicFull.txt',inverse=0)
                z2,mat2=read_tissues_volumes('/home/fernandr/Bureau/ML_CEP/RESULTS/EXP_6_ON_STACKS/'+specimens[sympt*3+1]+'/countTabGeodesicFull.txt',inverse=0)
                z3,mat3=read_tissues_volumes('/home/fernandr/Bureau/ML_CEP/RESULTS/EXP_6_ON_STACKS/'+specimens[sympt*3+2]+'/countTabGeodesicFull.txt',inverse=0)
                t=(np.arange(-20, 5, 0.3))
                n_t=len(t)
                t=np.double(t)
                vect=[mat1[int(indices[tissue]),0:n_t],mat2[int(indices[tissue]),0:n_t], mat3[int(indices[tissue]),0:n_t]]
                means=np.mean(vect,axis=0)
                stds=np.std(vect,axis=0)
                plt.fill_betweenx(t, means-stds, means+stds,color=colors[sympt2*3+1], alpha=alpha_sympt[sympt2])
                plt.plot(means,t,label=symp[sympt],color=colors[sympt2*3+1]) # 'go',
            plt.xlim(0,lim_x)
            plt.ylim(-20,9)
     #       plt.yticks([-20,-15,-10,-5,0,5,10],["-20","-15","-10","-5","0\n(Trunk top)","5","10"], color="black", size=8)
            ax2.legend(fontsize=8)#    loc=(1.2,0.5)
            plt.plot([1,1],[min_x,max_x], color='#cccccc',linewidth=0.6)
            plt.plot([0,lim_x],[0,0], '--',color='#111111',linewidth=1.0)
            ax2.text(lim_x*0.7,3.0,'Branches',size=12,color='#111111')
            ax2.text(lim_x*0.75,-4.4,'Trunk',size=12,color='#111111')
            ax2.text(lim_x*0.09,-18,'To rootstock',size=9,color='#111111')
            ax2.text(lim_x*0.09,7,'To grapes',size=9,color='#111111')
            arr = Arrow(lim_x*0.075, -16, 0, -3, edgecolor='black',facecolor='black',width=lim_x*0.04)
            arr2 = Arrow(lim_x*0.075, 6, 0, 3, edgecolor='black',facecolor='black',width=lim_x*0.04)
            ax2.add_patch(arr)
            ax2.add_patch(arr2)





        #PLOT VERTICAL TOTAL WOOD OVER CATEGORIES 
        lim_x=180
        symp=['Asymptomatic','Resilient','Symptomatic','Apoplectic']
        symp2=['Asymptomatic','Symptomatic','Resilient','Apoplectic']
        lookuptable=(0,2,1,3)
        # SURFACE RATIO BETWEEN AMADOU AND HEALTHY VERTICAL
        mmax=0
        plt.figure(figsize=(750/my_dpi, 1000/my_dpi), dpi=my_dpi) 
        ax2 = plt.subplot(1,1,1)
        plt.ylim(min_x,max_x)
        plt.xlabel('Total wood surface')
        plt.ylabel("Height (cm), relative to trunk head")
        alpha_sympt=[0.4,0.3,0.3,0.25]
        for sympt2 in range(4):
            sympt=lookuptable[sympt2]
            z1,mat1=read_tissues_volumes('/home/fernandr/Bureau/ML_CEP/RESULTS/EXP_6_ON_STACKS/'+specimens[sympt*3]+'/countTabGeodesicFull.txt',inverse=0)
            z2,mat2=read_tissues_volumes('/home/fernandr/Bureau/ML_CEP/RESULTS/EXP_6_ON_STACKS/'+specimens[sympt*3+1]+'/countTabGeodesicFull.txt',inverse=0)
            z3,mat3=read_tissues_volumes('/home/fernandr/Bureau/ML_CEP/RESULTS/EXP_6_ON_STACKS/'+specimens[sympt*3+2]+'/countTabGeodesicFull.txt',inverse=0)
            t=(np.arange(-20, 5, 0.3))
            n_t=len(t)
            t=np.double(t)
            vect=[mat1[0,0:n_t]+mat1[1,0:n_t]+mat1[2,0:n_t]+mat1[3,0:n_t],mat2[0,0:n_t]+mat2[1,0:n_t]+mat2[2,0:n_t]+mat2[3,0:n_t],mat3[0,0:n_t]+mat3[1,0:n_t]+mat3[2,0:n_t]+mat3[3,0:n_t]]
            means=np.mean(vect,axis=0)
            stds=np.std(vect,axis=0)
            plt.fill_betweenx(t, means-stds, means+stds,color=colors[sympt2*3+1], alpha=alpha_sympt[sympt2])
            plt.plot(means,t,label=symp[sympt],color=colors[sympt2*3+1]) # 'go',
            
            
        plt.xlim(0,lim_x)
        plt.ylim(-20,9)
 #       plt.yticks([-20,-15,-10,-5,0,5,10],["-20","-15","-10","-5","0\n(Trunk top)","5","10"], color="black", size=8)
        ax2.legend(fontsize=8)#    loc=(1.2,0.5)
        plt.plot([1,1],[min_x,max_x], color='#cccccc',linewidth=0.6)
        plt.plot([0,lim_x],[0,0], '--',color='#111111',linewidth=1.0)
        ax2.text(lim_x*0.7,3.0,'Branches',size=12,color='#111111')
        ax2.text(lim_x*0.75,-4.4,'Trunk',size=12,color='#111111')
        ax2.text(lim_x*0.09,-18,'To rootstock',size=9,color='#111111')
        ax2.text(lim_x*0.09,7,'To grapes',size=9,color='#111111')
        arr = Arrow(lim_x*0.075, -16, 0, -3, edgecolor='black',facecolor='black',width=lim_x*0.04)
        arr2 = Arrow(lim_x*0.075, 6, 0, 3, edgecolor='black',facecolor='black',width=lim_x*0.04)
        ax2.add_patch(arr)
        ax2.add_patch(arr2)
#        ax2.legend(fontsize=8,loc=(2.0,-12))



       #PLOT VERTICAL TOTAL WOOD OVER SPECIMENS 
        lim_x=180
        symp=['Asymptomatic','Resilient','Symptomatic','Apoplectic']
        symp2=['Asymptomatic','Symptomatic','Resilient','Apoplectic']
        specimens2=['AS1','AS2','AS3',   'RES1','RES2','RES3',  'S1','S2','S3',  'APO1','APO2','APO3']
        lookuptable=(0,1,2,6,7,8,3,4,5,9,10,11)
        # SURFACE RATIO BETWEEN AMADOU AND HEALTHY VERTICAL
        mmax=0
        plt.figure(figsize=(750/my_dpi, 1000/my_dpi), dpi=my_dpi) 
        ax2 = plt.subplot(1,1,1)
        plt.ylim(min_x,max_x)
        plt.xlabel('Total wood surface')
        plt.ylabel("Height (cm), relative to trunk head")
        alpha_sympt=[0.4,0.3,0.3,0.25]
        for spec in range(12):
            speccc=lookuptable[spec]
            z1,mat1=read_tissues_volumes('/home/fernandr/Bureau/ML_CEP/RESULTS/EXP_6_ON_STACKS/'+specimens[speccc]+'/countTabGeodesicFull.txt',inverse=0)
            t=(np.arange(-20, 5, 0.3))
            n_t=len(t)
            t=np.double(t)
            vect=[mat1[0,0:n_t]+mat1[1,0:n_t]+mat1[2,0:n_t]+mat1[3,0:n_t]]
            plt.plot(vect[0],t,label=specimens2[speccc],color=colors[spec]) # 'go',
            
            
        plt.xlim(0,lim_x)
        plt.ylim(-20,9)
 #       plt.yticks([-20,-15,-10,-5,0,5,10],["-20","-15","-10","-5","0\n(Trunk top)","5","10"], color="black", size=8)
        ax2.legend(fontsize=8)#    loc=(1.2,0.5)
        plt.plot([1,1],[min_x,max_x], color='#cccccc',linewidth=0.6)
        plt.plot([0,lim_x],[0,0], '--',color='#111111',linewidth=1.0)
        ax2.text(lim_x*0.7,3.0,'Branches',size=12,color='#111111')
        ax2.text(lim_x*0.75,-4.4,'Trunk',size=12,color='#111111')
        ax2.text(lim_x*0.09,-18,'To rootstock',size=9,color='#111111')
        ax2.text(lim_x*0.09,7,'To grapes',size=9,color='#111111')
        arr = Arrow(lim_x*0.075, -16, 0, -3, edgecolor='black',facecolor='black',width=lim_x*0.04)
        arr2 = Arrow(lim_x*0.075, 6, 0, 3, edgecolor='black',facecolor='black',width=lim_x*0.04)
        ax2.add_patch(arr)
        ax2.add_patch(arr2)
#        ax2.legend(fontsize=8,loc=(2.0,-12))



    if(doVolumes):
        volumes=np.zeros((12,5))
        specimens2=['AS1','AS2','AS3',   'RES1','RES2','RES3',  'S1','S2','S3',  'APO1','APO2','APO3']
        lookuptable=(0,1,2,6,7,8,3,4,5,9,10,11)
        specimensLUT=['AS1','AS2','AS3',   'S1','S2','S3',  'RES1','RES2','RES3',  'APO1','APO2','APO3']
        titles=['Healthy wood volume (cm³)','Necrose wood volume (cm³)','Amadou volume (cm³)','Unhealthy wood volume (cm³)','Total wood volume (cm³)']
        x_lims=[1000,1200,400,1600,2200]
        plots_to_do=np.array([[2,0],[1,0],[2,1],[3,0],[4,0],[4,1],[4,2]])   

        mat= count_volumes()
        print (mat)
        for spec in range(12):
            volumes[spec,0]=mat[spec,0]
            volumes[spec,1]=mat[spec,1]
            volumes[spec,2]=mat[spec,2]
            volumes[spec,3]=mat[spec,1]+mat[spec,2]
            volumes[spec,4]=mat[spec,4]

        print('')
        print('Valeurs volume bois sain : ')
        print(volumes[:,0])
        print('')
        print('Valeurs volume necrose : ')
        print(volumes[:,1])
        print('')
        print('Valeurs volume amadou : ')
        print(volumes[:,2])

        print('Valeurs volume unhealthy : ')
        print(volumes[:,3])

        print('Valeurs volume total : ')
        print(volumes[:,4])

        for pl in range(np.shape(plots_to_do)[0]):
            mes_x=plots_to_do[pl,0]            
            mes_y=plots_to_do[pl,1]            
            plt.figure(figsize=(900/my_dpi, 600/my_dpi), dpi=my_dpi) 
            ax2 = plt.subplot(1,1,1)
            plt.ylim(0,x_lims[mes_y])
            plt.xlim(0,x_lims[mes_x])
            markers=['^','o','s']
            plt.ylabel(titles[mes_y])
            plt.xlabel(titles[mes_x])

            for spec in range(12):
                plt.scatter(volumes[lookuptable[spec],mes_x], volumes[lookuptable[spec],mes_y],label=specimens2[lookuptable[spec]],facecolor=colors[3*(spec//3)+2],marker=markers[spec%3],edgecolor='#000000') # 'go',              
            ax2.legend(specimensLUT,fontsize=8)




def count_volumes():
    slice_begin=int(round(5/0.3))
    slice_end=int(round(20/0.3))
    print("Count from "+str(slice_begin)+" to "+str(slice_end))
    mat_tot=np.zeros((12,5))
    for spec in range(12):
        print("processing specimen "+str(spec))
        z,mat=read_tissues_volumes('/home/fernandr/Bureau/ML_CEP/RESULTS/EXP_6_ON_STACKS/'+specimens[spec]+'/countTabGeodesicFull.txt',inverse=0)
        nb_vox=np.sum(mat[7:11,slice_begin:slice_end],axis=1)
        volumes=nb_vox*0.722*0.722/1000
        mat_tot[spec,0:4]=volumes
    mat_tot[:,4]=np.sum(mat_tot[:,0:4],axis=1)
    return mat_tot    


def std_spec(mat):
    mat1=mat.T
    mat2=np.zeros((5,20))
    print(mat1)
    for symp in range(4):
        mat2[:,symp*5:symp*5+3]=np.round(mat1[:,symp*3:symp*3+3])

    print(mat2)
    print(np.shape(mat1))
    print(np.shape(mat2))
    for symp in range(4):        
        for line in range(5):
            print("processing symtom"+str(symp)+" at line "+str(line))
            print("data=")
            print(mat1[line,symp*3:symp*3+3])
            print("mean="+str(np.mean(mat1[line,symp*3:symp*3+3])))
            print("std="+str(np.std(mat1[line,symp*3:symp*3+3])))
            print("inscrits aux indices "+str(line)+" "+str(3+symp*5)+"-"+str(4+symp*5))          
            mat2[line,3+symp*5]=np.mean(mat1[line,symp*3:symp*3+3])
            mat2[line,4+symp*5]=np.std(mat1[line,symp*3:symp*3+3])
    return mat2

mat=count_volumes()
mat2=std_spec(mat)

print (mat2)
np.savetxt("/home/fernandr/Bureau/mat_test.csv",mat2.astype(int), fmt='%i', delimiter=",")
specimens=['CEP011_AS1','CEP012_AS2','CEP013_AS3',   'CEP014_RES1','CEP015_RES2','CEP016_RES3',  'CEP017_S1','CEP018_S2','CEP019_S3',  'CEP020_APO1','CEP021_APO2','CEP022_APO3']

close('all')
doBasicRatios=1
hideFirst=1
doVerticalAmadouHealthy=0
doVerticalAmadouHealthyCat=1
doVerticalAmadouNecroseCat=0
doVerticalNecroseHealthyCat=0
doVerticalAmadouCat=0
doVerticalHealthyCat=0
doVerticalNecroseCat=0
doVerticalHealthyOverOthers=0
doSurfaceCat=0
doRatioCat=0
doCatCatRatio=1
do2D6=0
do2D3=0
doVolumes=0
listFigures=[doBasicRatios,doVerticalAmadouHealthy,doVerticalAmadouHealthyCat,doVerticalAmadouNecroseCat,doVerticalNecroseHealthyCat,doVerticalAmadouCat,doVerticalHealthyCat,doVerticalNecroseCat,doVerticalHealthyOverOthers,do2D6,do2D3,hideFirst,doSurfaceCat,doRatioCat,doCatCatRatio,doVolumes]

sympt=0
z1,mat1=read_tissues_volumes('/home/fernandr/Bureau/ML_CEP/RESULTS/EXP_6_ON_STACKS/'+specimens[sympt*3]+'/countTabGeodesicFull.txt',inverse=0)
                
count_volumes()

compute_both_chamfer(specimens,listFigures)

   

#slice_numbers= [ 86 , 76 , 174 ,          65 , 97 , 108 ,        71  , 74 ,  68 ,       59 , 42  , 118  ]
#compute_both_ratio(specimens,slice_numbers)






