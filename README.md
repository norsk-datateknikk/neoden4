# neoden4

This repo is a fork of charlie-x's [repository](https://github.com/charlie-x/neoden4), which is a rewrite of dangerous prototypes tm220 ulp (modded by jamz and Xinort).

This fork has a modified ULP script to generate PnP files for Norsk Datataeknikk AS.

## User guide

### In Fusion360
- Run ulp from the board view, load or edit the stack, assign and output a CSV file.

#### If the board has negative XY Coordinates

You have to move your board in eagle to a place where the fiducials in eagle coordinates are mappable in the machines physical space, so no -X,  or -Y all positive, and enough away from 0,0 where the head can physically move. Otherwise it'll cause an error when you try to use the following instructions

There is added board offset XY to the CSV output page, so that during export you can move the boards offset instead of moving it in eagle, but both work. 

This effectively translates the 0,0 origin of eagle to a new origin that matches the origin of the PCB on the PNP, if your PCB starts at 0,0 in eagle then wherever the lower left corner of the PCB is in PNP XY phyiscal coordinates, this should be set as the offset XY. Remembering that if you are using the camera for visual inspection or fiducials both the nozzle and camera position need to be able to moved too physically by the PNP

The PNP software won't work well with negative coordinates, so make sure your outputted CSV is all positive XY.

### On the machine
- Import the generated csv to the machine.
- Press edit on the neoden4 software for the new file you just imnported.
- Make sure the left bottom, and panel1 are set to the XY of component 1 in the Component List(Script will do this).
- Then add the fidicuals in the fiducials settings as they are in eagle,not as they are in the machine(Script will do this).
- Click the first component in the list, then click align, it will go to the wrong place thats ok (if it throws an out of bounds error, see note above about where to move the board in eagle), now hit cancel.
- Press "Change to current position" and the PNP will go to the eagle coords of the fidcuials and complain that it cannot find the fiducials, and do you want to do it, say yes.
- Then  pick the actual location of the fiducial where it physically is on the machine and click save.
- The pnp  will tries to find the second mark,it should fail again, say yes to find it. search for your second fiducial mark, then click save. (again if you get an out of bounds error, read the note above about where to place the eagle file).
- The pnp software should now update all your components to the correct place
- Then update the left bottom position XY to the newly updated first component XY position and recreate the panel by clicking the panel button. save it, test by single step, or using align.

## Ignored parts
Fiducials are exracted automatically, if the parts name or value contains "FID".

If there are parts on the board which for some reason are not to be placed by the machine, they can be specified by specific attributes.

### Attributes:
- NOPNP attribute set to "NOPNP" for parts you don't want to include in PNP placement. E.g. Throgh hole components requiring manual placement.
- DNM attribute set to "DNM" for components which to not to place at all BOM. E.g. backub and configuration resistors.
- NOBOM attribute set to "NOBOM" for components which to ingnore from the BOM. E.g. titleframe etc.