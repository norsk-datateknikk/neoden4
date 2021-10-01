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
            print(idx)
            line_splits.append(idx)

    first_file = filename + "_first.csv"

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
    names = [   
        'Type',                 #
        'Feeder ID',            # 
        'Type',                 #
        'ReelHead',             # head = nozzle index to combo box.
        'ReelOffSetX',          # X location of feeder.
        'ReelOffSetY',          # Y location of feeder.
        'ReelPickAngle',        # Angle.
        'ReelFootPrint',        # Footprint.
        'Reel',                 # Name (?)
        'ReelHeight',           # Pick Height
        'ReelPickDelay',        # Pick delay
        'ReelPlaceHeight',      # Placement Height
        'ReelPlaceDelay',       # Placement Delay
        'ReelVacuumDetection',  # Vacuum Detection (Yes/No)
        'ReelVacuumValue',      # Vacuum Value
        'ReelVisionAlignment',  # Vision Alignment.
        'ReelMoveSpeed',        # 
        'ReelRate',             # Feeding Rate.
        'ReelFeedStrength',     # Feed Strength.
        'ReelPeelStrength',     # Peel Strength.
        'ReelSkip',             # Skip (Yes/No).
        'ReelSizeCorrect',      # Size Correct ( CheckMark Yes/No)
        'Nozzle1Thresholds',
        'Nozzle2Thresholds', 
        'Nozzle3Thresholds', 
        'Nozzle4Thresholds'
        ]

    names_special = [   
        'Type',                 #
        'Feeder ID',            # 
        'Type',                 #
        'ReelHead',             # head = nozzle index to combo box.
        'ReelOffSetX',          # X location of feeder.
        'ReelOffSetY',          # Y location of feeder.
        'ReelPickAngle',        # Angle.
        'ReelFootPrint',        # Footprint.
        'Reel',                 # Name (?)
        'ReelHeight',           # Pick Height
        'ReelPickDelay',        # Pick delay
        'ReelPlaceHeight',      # Placement Height
        'ReelPlaceDelay',       # Placement Delay
        'ReelVacuumDetection',  # Vacuum Detection (Yes/No)
        'ReelVacuumValue',      # Vacuum Value
        'ReelVisionAlignment',  # Vision Alignment.
        'ReelMoveSpeed',        # 
        'trayColumns',          #
        'trayRows',             # 
        'trayRightTopX',        # 
        'trayRightTopY',        # 
        'trayStartX',           #
        'trayStartY'            #
        'ReelSkip',             # Skip (Yes/No).
        'ReelSizeCorrect',      # Size Correct ( CheckMark Yes/No)
        'Nozzle1Thresholds',
        'Nozzle2Thresholds', 
        'Nozzle3Thresholds', 
        'Nozzle4Thresholds'
        ]

    uss_df = pd.DataFrame(names=names)
    
    for idx, row in pnp_df.iterrows():
        if row['Feeder'] == 'stack':
            data_list = ['[REEL]', 0.0, ]
            row_df = pd.DataFrame( data_list )
            uss_df.append(row_df)
            
    
    return uss_df

def convert_file( filename ):
    first_filename = split_file(filename)

    names = ['Feeder','Feeder ID','Type','Nozzle','X','Y','Angle','Footprint','Value','Pick height','Pick delay','Place Height','Place Delay','Vacuum detection','Threshold','Vision Alignment','Speed','1','2','3','4','5','6','7','8','9','10','11','12','13','14','15','16']

    pnp_df = pd.read_csv( first_filename, sep=',', names=names, skiprows=1 )
    uss_df = parse_uss(pnp_df)

    uss_df.to_csv('first_filename.USS',sep='|', header=False, index=False)
    
    

            


if 1 < len(sys.argv):
    try:
        convert_file( sys.argv[1] )
    except IOError as e:
        print("This file doesn't exist. Aborting.")
        print(e)
        exit(1)