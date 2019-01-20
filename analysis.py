import numpy as np
import pandas as pd

def import_data():

    df_dict = {}
    for i in range(8):
        dir = 'datasets/'+str(i+1)+'/'
        XYspkT = np.loadtxt(dir+'XYspkT.csv',delimiter=',')+40
        XYspkT[:, 1] -= XYspkT[:, 1].min()
        XYspkT[:, 0] -= XYspkT[:, 0].min()
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
        df_dict[i] = pd.DataFrame(data=all,columns=['Time','X','Y','Phase','SPhase'])
        df_dict[i]['Color'] = df_dict[i+1].apply(lambda row: 'hsl(' + str(row.SPhase/(all[:,4].max()) * 360)
                                           + ' ,50%, 50%)', axis=1)
        df_dict[i]['Name'] = df_dict[i+1].apply(lambda row: 'Phase: '+ str(row.Phase),axis=1)

    return df_dict
