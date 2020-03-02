import numpy as np

from FATABLE import *

fat = np.array(FATABLE)
actID = np.int16(fat[:, FATABLE_ID])
nActuator = actID.shape[0]
xact = np.float64(fat[:, FATABLE_XPOSITION])
yact = np.float64(fat[:, FATABLE_YPOSITION])

def assembleFfromEFD(df1, output=0):
    '''
    df1 is a pandas frame, which is result of a query to table m1m3_logevent_AppliedForces
    This assumes x/y/z forces from invidual actuators are stored as separate columns
    output:
    col 0: actuator IDs
    col 1: x force
    col 2: y force
    col 3: z force
    '''
    myF = np.zeros((nActuator, 4)) #ID, x, y, z
    myF[:, 0] = actID
    xexist = 1
    yexist = 1
    zexist = 1
    for i in range(nActuator):
        ix = FATABLE[i][FATABLE_XINDEX]
        iy = FATABLE[i][FATABLE_YINDEX]

        myF[i, 3] = np.mean(df1['zForces%d'%(i)]) #Fz

        if ix != -1:
            myF[i, 1] = np.mean(df1['xForces%d'%(ix)]) #Fx, note ix starts with 0

        if iy != -1:
            myF[i, 2] = np.mean(df1['yForces%d'%(iy)]) #Fx, note ix starts with 0

        if output:
            print('%d, %6.1f %6.1f %8.1f'%(myF[i, 0],myF[i, 1],myF[i, 2],myF[i, 3]))

    if not xexist:
        print('---No XForces---')
    if not yexist:
        print('---No YForces---')
    if not zexist:
        print('---No ZForces---')
    return myF

def assembleFfromEFD_C1C2(df1, output=0):
    '''
    df1 is a pandas frame, which is result of a query to table m1m3_logevent_AppliedCylinderForces
    This assumes x/y/z forces from invidual actuators are stored as separate columns
    output:
    col 0: actuator IDs
    col 1: x force
    col 2: y force
    col 3: z force
    '''
    myF = np.zeros((nActuator, 4)) #ID, x, y, z
    myF[:, 0] = actID
    for i in range(nActuator):
        idaa = FATABLE[i][FATABLE_SINDEX]
        orientation = FATABLE[i][FATABLE_ORIENTATION]
        fc1 = np.mean(df1['primaryCylinderForce%d'%(i)])
        myF[i, 3] = fc1
        if orientation == 'NA':
            pass
        else:
            fc2 = np.mean(df1['secondaryCylinderForce%d'%(idaa)])

            myF[i, 3] += fc2*0.707 #Fz
            if orientation == '+X':
                myF[i, 1] = fc2*0.707
            elif orientation == '-X':
                myF[i, 1] = -fc2*0.707
            elif orientation == '+Y':
                myF[i, 2] = fc2*0.707
            elif orientation == '-Y':
                myF[i, 2] = -fc2*0.707
            else:
                print('--- UNKNOWN CYLINDER 2 ORIENTATION ---')
        if output:
            print('%d, %6.1f %6.1f %8.1f'%(myF[i, 0],myF[i, 1],myF[i, 2],myF[i, 3]))
    return myF
