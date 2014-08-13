import pickle
from deap import tools, creator, base
import numpy as np


creator.create("FitnessMax", base.Fitness, weights=(-1.0,))
creator.create("Individual", list, fitness=creator.FitnessMax)

def dims(xn, yn, stepsize, individual, output_filename):
    col_s1=[]
    f_nums=[]
    s1_float=[]
    s1 = ""
    ind_string=""

    I_THETA = individual[0]
    XSHEAR = individual[1]
    YSHEAR = individual[2]
    SCALE = individual[3]

    y = np.linspace(0, yn, yn)
    x = np.linspace(0, xn, xn)
    (xg,yg)=np.meshgrid(x,y)
    xg = (xg - (xn/2))*stepsize
    yg = (yg - (yn/2))*stepsize

    for i in range(xn):
        for j in range(yn):
            s1+="{:e} {:e},".format(xg[j,i],yg[j,i])

    s1_split=s1.split(",")
    for i in range(7482):
        s1_float.append(map(float,s1_split[i].split(" ")))
    
    for i in range(7482):
        for j in range(2):
            col_s1.append(s1_float[i][j])
    
    #rotation transformation from individual
    rot = np.reshape(col_s1, (-1,2))
    xrot=[]
    yrot=[]
    for i in range(7482):
        xrot.append(np.cos(I_THETA)*rot[i][0] + np.sin(I_THETA)*rot[i][1])
        yrot.append(-np.sin(I_THETA)*rot[i][0] + np.cos(I_THETA)*rot[i][1])
    #scale
    xscale = [i*SCALE for i in xrot]
    yscale = [i*SCALE for i in yrot]

    #shear
    xshear_x=[]
    yshear_x=[]
    for i in range(7482):
        xshear_x.append(xscale[i]+XSHEAR*yscale[i])
        yshear_x.append(yscale[i])

    xshear_y = []
    yshear_y = []
    for i in range(7482):
        xshear_y.append(xshear_x[i])
        yshear_y.append(YSHEAR*xshear_x[i] + yshear_x[i]) 

    f_nums=zip(xshear_y, yshear_y)

    for j in range(7482):
        ind_string+="{:e} {:e},".format(f_nums[j][0],f_nums[j][1])    

    #save list to file 
    f=open('/local/kwiecien/ePIE_codes/blists/'+output_filename+'.csv','w')
    f.write(ind_string.strip(','))
    f.close()

def paramSave(best_qxy_x, best_qxy_y, best_z, best_energy, output_filename):
    fn = output_filename+"_params.csv"
    best_qxy=best_qxy_x,best_qxy_y
    f = open('/local/kwiecien/ePIE_codes/bparams/'+fn, 'w')
    f.write('QXY='+str(best_qxy)+'\n'+'z='+str(best_z)+'\n'+'energy='+str(best_energy))

def up(file_range):
    for i in range(file_range):
        fileset = 'mda{:d}'.format(309+(2*i))
        hof=fileset+'_optim3_hof.p'
        output_filename = fileset+'_8_13'
        input_filename='/local/kwiecien/ptycho/src/data/'+hof

        print hof,fileset,input_filename,output_filename



    	params = pickle.load(open(input_filename, 'r'))
    	individual = params[0]
    	dims(58,129,70e-9,individual,output_filename)
    	paramSave(individual[4], individual[5], individual[6], individual[7], output_filename)





