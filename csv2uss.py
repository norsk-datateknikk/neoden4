#!/usr/bin/python

import sys
import os
import pandas as pd


table_names = ["Feeder", "HP BladeSystem Rack", "Network Interface"]


def split_file(filename, split_mark='#'):
    """Split files byt the line starting with split_mark.

    :param filename: Path to the file.
    :type filename: str
    :param split_mark: This mark notes the first line of after a split, defaults to '#'
    :type split_mark: str, optional
    """
    name_no_extension = os.path.splitext(filename)[0]
    
    with open(filename,'r') as input_file:
        lines = input_file.readlines()

    line_splits = []
    for idx, line in enumerate(lines[:int(len(lines)/2)]):
        # Note the lines to split the file.
        if line.startswith(split_mark):
            line_splits.append(idx)

    first_file = name_no_extension + "_first.csv"

    with open(first_file, 'w') as file:
        for line in lines[:int( line_splits[1] )]:
            file.write(line)

    return first_file



def parse_uss( pnp_df ):
    """ Write out a User Standard Stack (USS) formatted file for a REEL setup.
    """

    # "stack,2,0,1,409.87,101.73,90.00,0805,0805/2.2nF,0.50,0,0.50,0,No,-40,1,100,4,50,80,No,No,-40,-40,-40,-40,",
    #[REEL]|1|0805/2.2nF|0805|1|409.87|101.73|90.00|0805|0.50|0|0.50|0|NO|-40|1|100|4|50|80|NO|NO


    # ReelHead/nozzle is now an index into the nozzleCombo

    # normal feeder setup
    # #Feeder,Feeder ID,Type,Nozzle, X,       Y,    Angle, Footprint, Value ,Pick height,Pick delay,Placement height,Placement delay,Vacuum detection,Vacuum value,Vision alignment,Speed,
    # stack,       2,     0,  12,  409.87, 101.73, 90.00,  0805,       2.2nF,     0.50,       0,          0.50,             0,             No,            -40,            1,           50,

    # continued 1: (different to special feeders)
    # Feed Rate, Feed torque,  Peel Strength,   skip,  size correct        Thresholds for nozzles 1-4
    # 4,          80,            50,             No,        No,             -40, -40, -40, -40,

    # Continued 2 (differences are here)
    # columns, rows, right top x , right top y, startx, starty,   skip, size correct,  thresholds for nozzles 1-4
    # 9,        8,   162.27,      206.88,         3,       4,        No,      No,       -40,-40,-40,-40,

    # Make empty df

    # ReelHead/nozzle is now an index into the nozzleCombo
    """
    //list of nozzle combinations for the parts dropdown
    string nozzleCombo[] = { "-",
                            "1", "2", "3", "4",
                            "12", "13", "14",
                            "22", "23", "24",
                            "34",
                            "123", "124",
                            "234",
                            "1234"
                        };
    """

    names = [   
        '[REEL]',                 #
        'ReelIdx',              # 
        'Type',                 #
        'ReelHead',             # head = nozzle index to combo box.
        'ReelOffSetX',          # X location of feeder.
        'ReelOffSetY',          # Y location of feeder.
        'ReelPickAngle',        # Angle, -180,-90,0,90,180
        'ReelFootPrint',        # Footprint.
        'Reel',                 # Name (?)
        'ReelHeight',           # Pick Height
        'ReelPickDelay',        # Pick delay
        'ReelPlaceHeight',      # Placement Height
        'ReelPlaceDelay',       # Placement Delay
        'ReelVacuumDetection',  # Vacuum Detection (Yes/No)
        'ReelVacuumValue',      # Vacuum Value
        'ReelVisionAlignment',  # Vision Alignment. No Action, Indivudally, Jointly, Large component
        'ReelMoveSpeed',        # 
        'ReelRate',             # Feeding Rate.
        'ReelFeedStrength',     # Feed Strength, 10 to 100 in steps of 1 (tourque).
        'ReelPeelStrength',     # Peel Strength.
        'ReelSkip',             # Skip (Yes/No).
        'ReelSizeCorrect',      # Size Correct ( CheckMark Yes/No).
        'Nozzle1Thresholds',    # -10 to -100 in steps of 5.
        'Nozzle2Thresholds',    # -10 to -100 in steps of 5.
        'Nozzle3Thresholds',    # -10 to -100 in steps of 5.
        'Nozzle4Thresholds'     # -10 to -100 in steps of 5.
        ]

    names_special = [   
        '[REEL]',               #
        'ReelIdx',              # 
        'Type',                 #
        'ReelHead',             # head = nozzle index to combo box.
        'ReelOffSetX',          # X location of feeder.
        'ReelOffSetY',          # Y location of feeder.
        'ReelPickAngle',        # Angle, -180,-90,0,90,180
        'ReelFootPrint',        # Footprint.
        'Reel',                 # Name (?)
        'ReelHeight',           # Pick Height
        'ReelPickDelay',        # Pick delay
        'ReelPlaceHeight',      # Placement Height
        'ReelPlaceDelay',       # Placement Delay
        'ReelVacuumDetection',  # Vacuum Detection (Yes/No)
        'ReelVacuumValue',      # Vacuum Value, -10 to -100
        'ReelVisionAlignment',  # Vision Alignment. No Action, Indivudally, Jointly, Large component [int].
        'ReelMoveSpeed',        # 
        'trayColumns',          #
        'trayRows',             # 
        'trayRightTopX',        # 
        'trayRightTopY',        # 
        'trayStartX',           #
        'trayStartY'            #
        'ReelSkip',             # Skip (Yes/No).
        'ReelSizeCorrect',      # Size Correct ( CheckMark Yes/No)
        'Nozzle1Thresholds',    # -10 to -100 in steps of 5.
        'Nozzle2Thresholds',    # -10 to -100 in steps of 5.
        'Nozzle3Thresholds',    # -10 to -100 in steps of 5.
        'Nozzle4Thresholds'     # -10 to -100 in steps of 5.
        ]

    uss_df_normal  = pd.DataFrame()
    uss_df_special = pd.DataFrame()
    #uss_df_special.columns = names_special
    
    for idx, row in pnp_df.iterrows():
        # Normal feeder.
        if row['Feeder'] == 'stack':
            data_dict = {   '[REEL]':               ['[REEL]'],                
                            'ReelIdx':              [row['Feeder ID']],            
                            'Type':                 [0],                 
                            'ReelHead':             [row['Nozzle']],       
                            'ReelOffSetX':          [row['X']],
                            'ReelOffSetY':          [row['Y']],        
                            'ReelPickAngle':        [row['Angle']],    
                            'ReelFootPrint':        [row['Footprint']],
                            'Reel':                 [row['Value']],
                            'ReelHeight':           [row['Pick Height']],
                            'ReelPickDelay':        [row['Pick Delay']],
                            'ReelPlaceHeight':      [row['Place Height']],
                            'ReelPlaceDelay':       [row['Place Delay']],
                            'ReelVacuumDetection':  [row['Vacuum Detection']],
                            'ReelVacuumValue':      [row['Threshold']],       #? 
                            'ReelVisionAlignment':  [row['Vision Alignment']],
                            'ReelMoveSpeed':        [row['Speed']],
                            'ReelRate':             [row['Feed Rate/Column']],
                            'ReelFeedStrength':     [row['Feed torque/rows']],
                            'ReelPeelStrength':     [row['Peel Strength/right top x']],
                            'ReelSkip':             [row['skip/right top y']],
                            'ReelSizeCorrect':      [row['size correct/startx']],
                            'Nozzle1Thresholds':    [row['Nozzle 1 Threshold/starty']],
                            'Nozzle2Thresholds':    [row['Nozzle 2 Threshold/skip']],
                            'Nozzle3Thresholds':    [row['Nozzle 3 Threshold/size correct']],
                            'Nozzle4Thresholds':    [row['Nozzle 4 Threshold/Nozzle 1 Threshold']]}

            data_list_df = pd.DataFrame( data_dict )
            uss_df_normal = uss_df_normal.append( data_list_df, ignore_index=True )

        # Currently only processing reels.
        """
        # Special feeder/tray.
        elif row['Feeder'] == 'mark':
            data_list = ['[REEL]', 0 ]
            row_df = pd.DataFrame( data_list )
            uss_df_special.append(row_df)
        """
    return uss_df_normal, uss_df_special

def convert_file( filename ):
    reel_table_filename = split_file(filename)
    

    # The column names for the neoden pnp file. The different feeder types reel/tray have different columns.
    names = [   'Feeder',
                'Feeder ID',
                'Type',
                'Nozzle',
                'X',
                'Y',
                'Angle',
                'Footprint',
                'Value',
                'Pick Height',
                'Pick Delay',
                'Place Height',
                'Place Delay',
                'Vacuum Detection',
                'Threshold',
                'Vision Alignment',
                'Speed',
                'Feed Rate/Column',             # Normal/special.
                'Feed torque/rows',             # Normal/special.
                'Peel Strength/right top x',    # Normal/special.
                'skip/right top y',             # Normal/special.
                'size correct/startx',          # Normal/special.
                'Nozzle 1 Threshold/starty',    # Normal/special.
                'Nozzle 2 Threshold/skip',      # Normal/special.
                'Nozzle 3 Threshold/size correct',          # Normal/special.
                'Nozzle 4 Threshold/Nozzle 1 Threshold',    # Normal/special.
                '/Nozzle 2 Threshold',          # Normal/special.
                '/Nozzle 3 Threshold',          # Normal/special.
                '/Nozzle 4 Threshold',
                '13', #?
                '14', #?
                '15', #?
                '16'] #?

    pnp_df = pd.read_csv( reel_table_filename, sep=',', names=names, skiprows=1 )
    uss_normal_df, uss_special_df = parse_uss(pnp_df)


    name_no_extension = os.path.splitext(filename)[0]
    uss_normal_df.to_csv(name_no_extension+'.USS',sep='|', header=False, index=False)
    print("Saved file " + name_no_extension+'.USS')
    


if 1 < len(sys.argv):
    try:
        convert_file( sys.argv[1] )
    except IOError as e:
        print("This file doesn't exist. Aborting.")
        print(e)
        exit(1)