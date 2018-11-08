import math
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import pearsonr


def import_data(dataset):

    dir = 'datasets/'+str(dataset)+'/'
    XYspkT = np.loadtxt(dir+'XYspkT.csv',delimiter=',')+40
    spkT = np.loadtxt(dir + 'spkT.csv', delimiter=',')
    phase = np.loadtxt(dir + 'Phase.csv', delimiter=',')
    scaled_phase = phase - 3.14
    #raw_map = np.loadtxt(dir + 'MeanPhaseMap.csv', delimiter=',')
    #MeanPhaseMap = np.flip(raw_map, axis=0)
    #MeanPhaseMap[0] = 'NaN'
    #MeanPhaseMap[:, -1] = 'NaN'
    #arena_size = MeanPhaseMap.shape
    #phase_df = pd.DataFrame(data=MeanPhaseMap, columns=np.arange(arena_size[1]))
    #padded_phase_map = np.pad(MeanPhaseMap,pad_width=2,mode='constant',constant_values=np.nan)
    #padded_phase_df = pd.DataFrame(data=padded_phase_map, columns=np.arange(arena_size[1]+4))

    all = np.column_stack((spkT,XYspkT,scaled_phase,phase))
    df = pd.DataFrame(data=all,columns=['Time','X','Y','Phase','SPhase'])
    df['Color'] = df.apply(lambda row: 'hsl(' + str(row.SPhase/(all[:,4].max()) * 360)
                                       + ' ,75%, 50%)', axis=1)
    df['Name'] = df.apply(lambda row: 'Phase: '+ str(row.Phase),axis=1)
    return df



#Option to all coordinates to compensate for coarse grain of meanphasemap
# round_XY = False
#
# #Spatial or temporal analysis
# spatial = True
#
# XYspkT = np.loadtxt(dir+'XYspkT.csv',delimiter=',')+40
#
# #Aligns positions to [0,0] in the bottom-left corner
# #XYspkT[:,1] -= XYspkT[:,1].min()
# #XYspkT[:,0] -= XYspkT[:,0].min()
# scaled_XY = XYspkT/2
#
# if round_XY == True:
#     scaled_XY = np.round(scaled_XY)
#
# plt.plot(scaled_XY[:,0],scaled_XY[:,1],'.')
# spkT = np.loadtxt(dir+'spkT.csv',delimiter=',')
# raw = np.loadtxt(dir+'MeanPhaseMap.csv',delimiter=',')
#
# #Flipping to align + stripping erraneous values
# MeanPhaseMap = np.flip(raw_map,axis=0)
# MeanPhaseMap[0]='NaN'
# MeanPhaseMap[:,-1]='NaN'
# arena_size = MeanPhaseMap.shape
#
# phase_df = pd.DataFrame(data=MeanPhaseMap, columns=np.arange(arena_size[1]))
# padded_phase_map = np.pad(MeanPhaseMap,pad_width=2,mode='constant',constant_values=np.nan)
# padded_phase_df = pd.DataFrame(data=padded_phase_map, columns=np.arange(arena_size[1]+4))


# def adjacent_matrix(cell):
#     c_x = int(cell[0])
#     c_y = int(cell[1])
#     y_size = arena_size[0] - 1
#     print(y_size - c_y, y_size - c_y + 5)
#     a = padded_phase_df.iloc[y_size - c_y:y_size - c_y + 5, c_x:c_x + 5]
#
#     return a
#
#
# def adjacent_spikes(spikes, phase):
#     # get location of spike with most similar phase
#     y_size = arena_size[0] - 1
#     phases = np.asarray([phase_df.iloc[y_size - int(i[1]), int(i[0])] for i in spikes])
#
#     try:
#         nearest = np.nanargmin(np.abs(phases - phase))
#     except:
#         nearest = 0
#
#     try:
#         return [spikes[nearest, 0] - spikes[0, 0], spikes[nearest, 1] - spikes[0, 1]]
#     except:
#         return [0.0, 0.0]
#
#
# def nearest_phase(array, phase):
#     # Determines change vector from central cell
#     # to cell nearest in value in 7x7 IN FORM **[X,Y]**
#     try:
#         nearest = np.nanargmin(np.abs(array - phase))
#         # loc = [(am%7)-3,3-(am//7)]
#         loc = [(nearest % 5) - 2, 2 - (nearest // 5)]
#         return loc
#     except:
#         return [0, 0]
#
#
# def phase_from_movement(array, x, y):
#     try:
#         return array.iloc[3 - y, 3 + x]
#     except:
#         # return array[3,3]
#         pass
#
# unsorted = np.column_stack((spkT,scaled_XY,scaled_phase))
# sorted = unsorted[unsorted[:,0].argsort()]
#
# #Calculate movement magnitudes
# xdif = np.append(sorted[1:,1],0)-np.append(sorted[:-1,1],0)
# ydif = np.append(sorted[1:,2],0)-np.append(sorted[:-1,2],0)
#
# #Drop rows with movements below threshold
# if round_XY == True:
#     move_thresh = 1
# else:
#     move_thresh = 0.1
#
# raw = np.column_stack((sorted,xdif,ydif))
# movement  = raw[np.any(abs(raw[:,4:]) >= move_thresh, axis=1)]
#
# #Recalculate movement magnitudes
# xdif = np.append(movement[1:,1],0)-np.append(movement[:-1,1],0)
# ydif = np.append(movement[1:,2],0)-np.append(movement[:-1,2],0)
#
# next_phase = np.insert(sorted[1:,3],-1, 0)
# combined = np.column_stack((movement[:,:4],sorted_phase,xdif,ydif))
#
# # Spatial Analysis
# if spatial == True:
#     predicted = [nearest_phase(adjacent_matrix([i[1], i[2]]), i[4]) for i in combined]
#     predicted_movement = np.asarray(predicted)
#
# # Temporal Analysis
# elif spatial == False:
#     predicted = [adjacent_spikes(combined[i + 2:i + 7, 1:3], combined[i, 4]) for i in range(len(combined))]
#     predicted_movement = np.asarray(predicted)
#
# all = np.column_stack((combined, predicted_movement))
# df = pd.DataFrame(data=all,
#                   columns=['Time', 'X', 'Y', 'Phase', 'Next Phase', 'Xdif', 'Ydif', 'Xdif Predicted', 'Ydif Predicted'])
