#=============================================================================================================================================================

# -*- coding: euc-kr -*-

#   P r o g r a m   f i l e

#

#   Spotman
#

#   Author : Donggeon Kim, Jonghan Kim

#

#   Function : move the spotlight to follow the object more realistically as if the spotlight is handled by a human 

#

#   Variable prefix  : none

#

#   input file : none

#   output file : none

#

#   Arguments : none

#

# ver Date       Author                      Description

# === ========== =========================   =================================================

# 1  2021/07/07  Donggeon Kim, Jonghan Kim   Initial build for Marmaduke (version 1)
#=============================================================================================

#limitation: only works for straight path (if object turns and moves to the opposite direction, this method can't capture that)

#=============================================================================================================================================================


import maya.cmds as cmds
"""
1. add locator
2. add attributes: velocity, delay, initialSeparation
- velocity: how fast the spotman is moving; the closer this value is to zero, the slower the spotman moves (should be greater than 0!)
- delay: give delay in terms of frame; how much frame after the spotman starts moving (should be greater than 0!)
- initialSeparation: how much the spotman is away from the object at the first frame
3. write code on the expression editor for x coordinates
4. write code on the expression editor for y and z coordinates
4. aim-constraint the spotlight
"""

#<input>
#w_target_obj: (string) the name of object file (or its belongings) to follow
#w_spot_light: (string) the name of the spotlight to connect the spotman locator to
#w_default_velocity: (float), default value of velocity attribute
#w_default_delay: (float), default value of delay attribute
#w_default_initialSeparation: (float), default value of the initialSeparation attribute
w_target_obj = 'billyCowboyWaistcoat_01_C'
w_spot_light = 'k_spot_rsps'
w_default_velocity = 0.2
w_default_delay = 0
w_default_initialSeparation = 100

w_locator    = 'spotman_locator'

w_target_obj = cmds.ls("::*" + w_target_obj)
w_spot_light = cmds.ls("::*" + w_spot_light)

if w_target_obj and w_spot_light: 
    w_target_obj = w_target_obj[0]
    w_spot_light = w_spot_light[0]
    
    try :
        cmds.delete(w_locator)
    except :
        pass

    #creating locator
    cmds.spaceLocator( name=w_locator)

    #creating & setting attributes
    cmds.addAttr( longName = 'velocity', defaultValue = w_default_velocity )
    cmds.setAttr( 'spotman_locator.velocity', keyable=True, type="double3" )
    
    cmds.addAttr( longName = 'delay', defaultValue = w_default_delay )
    cmds.setAttr( 'spotman_locator.delay', keyable=True, type="double3" )
    
    cmds.addAttr( longName = 'initialSeparation', defaultValue = w_default_initialSeparation )
    cmds.setAttr( 'spotman_locator.initialSeparation', keyable=True, type="double3" )
    
    w_start_frame = cmds.playbackOptions(q=True, minTime=True)
    w_end_frame   = cmds.playbackOptions(q=True, maxTime=True)

    #getting x-coordinate of the initial frame
    cmds.currentTime(w_start_frame)
    w_boundingbox = cmds.xform(w_target_obj,q=True,bb=True)
    w_start_x     = ((w_boundingbox[3] - w_boundingbox[0]) / 2) + w_boundingbox[0]

    #getting x-coordinate of the final frame
    cmds.currentTime(w_end_frame)
    w_boundingbox = cmds.xform(w_target_obj,q=True,bb=True)
    w_end_x       = ((w_boundingbox[3] - w_boundingbox[0]) / 2) + w_boundingbox[0]
    
    #returning to the initial frame
    cmds.currentTime(w_start_frame)

    #x-coordinate
    #if going from smaller x-coordinate to greater x-coordinate
    if w_start_x < w_end_x:
        w_string = 'string $w_face;\nfloat $w_boundingbox[];\nstring $w_cmd;\n\n//$w_face = python(\"cmds.ls(sl=True)[0]\");\n$w_face        = \"{}\";\n$w_cmd         =\"cmds.xform(\\\"\" + $w_face + \"\\\",q=True,bb=True)\";\n$w_boundingbox = python($w_cmd);\n$w_pivot_x     = python((($w_boundingbox[3] - $w_boundingbox[0]) / 2) + $w_boundingbox[0]);\n$w_start_frame = python(\"cmds.playbackOptions(q=True, minTime=True)\");\n\n$w_distance = spotman_locator.initialSeparation*(exp( -1 * spotman_locator.velocity * ( frame - (float)$w_start_frame - (float)spotman_locator.delay ) ));\nspotman_locator.translateX = $w_pivot_x - $w_distance;'.format(w_target_obj)
        cmds.expression( o='spotman_locator', s=w_string )
        
    #if going from greater x-coordinate to smaller x-coordinate
    else:
        w_string = 'string $w_face;\nfloat $w_boundingbox[];\nstring $w_cmd;\n\n//$w_face = python(\"cmds.ls(sl=True)[0]\");\n$w_face        = \"{}\";\n$w_cmd         =\"cmds.xform(\\\"\" + $w_face + \"\\\",q=True,bb=True)\";\n$w_boundingbox = python($w_cmd);\n$w_pivot_x     = python((($w_boundingbox[3] - $w_boundingbox[0]) / 2) + $w_boundingbox[0]);\n$w_start_frame = python(\"cmds.playbackOptions(q=True, minTime=True)\");\n\n$w_distance = spotman_locator.initialSeparation*(exp( -1 * spotman_locator.velocity * ( frame - (float)$w_start_frame - (float)spotman_locator.delay ) ));\nspotman_locator.translateX = $w_pivot_x + $w_distance;'.format(w_target_obj)
        cmds.expression( o='spotman_locator', s=w_string )

    #y-coordinate
    w_string = 'string $w_face;\nfloat $w_boundingbox[];\nstring $w_cmd;\n\n//$w_face = python(\"cmds.ls(sl=True)[0]\");\n$w_face = \"{}\";\n$w_cmd =\"cmds.xform(\\\"\" + $w_face + \"\\\",q=True,bb=True)\";\n$w_boundingbox = python($w_cmd);\n\n$w_pivot_y = python((($w_boundingbox[4] - $w_boundingbox[1]) / 2) + $w_boundingbox[1]);\n\nspotman_locator.translateY = $w_pivot_y;'.format(w_target_obj)
    cmds.expression( o='spotman_locator', s=w_string )
    #z-coordinate
    w_string = 'string $w_face;\nfloat $w_boundingbox[];\nstring $w_cmd;\n\n//$w_face = python(\"cmds.ls(sl=True)[0]\");\n$w_face = \"{}\";\n$w_cmd =\"cmds.xform(\\\"\" + $w_face + \"\\\",q=True,bb=True)\";\n$w_boundingbox = python($w_cmd);\n\n$w_pivot_z = python((($w_boundingbox[5] - $w_boundingbox[2]) / 2) + $w_boundingbox[2]);\n\nspotman_locator.translateZ = $w_pivot_z'.format(w_target_obj)
    cmds.expression( o='spotman_locator', s=w_string )
    
    cmds.aimConstraint(w_locator,w_spot_light, aim=(0.0,0.0,-1.0),mo=True)
    
else : 
    print "No proper objects to connect"