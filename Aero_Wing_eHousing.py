######################################################################
# PYCATIA LIBRARIES
from pycatia import catia
from pycatia.mec_mod_interfaces.part_document import PartDocument
import math

#######################################################################
#  CATIA variables
######################################################################

caa = catia()
application = caa.application
documents = application.documents
if documents.count > 0:
    for document in documents:
        document.close()
        
# Create Part
documents.add('Part')
######################################################################
# Get references to document, parts and tools to create geometries
document: PartDocument = application.active_document        # Get active document
part = document.part                                        # Get Part
partbody = part.bodies[0]                                   # Get default PartBody by index
# partbody = part.bodies.item("PartBody")                     # Get default PartBody by name
sketches = partbody.sketches                                # Get sketches on PartBody 
hybrid_bodies = part.hybrid_bodies                          # Get Hybrid Bodies 
hsf = part.hybrid_shape_factory                             # Get Hybrid Shape Factory 
shpfac = part.shape_factory                                 # Get Shape Factory 
selection = document.selection                              # Get document selection

######################################################################
# Get references to main planes
plane_XY = part.origin_elements.plane_xy
plane_YZ = part.origin_elements.plane_yz
plane_ZX = part.origin_elements.plane_zx


######################################################################

# Set PartBody as a working object
part.in_work_object = partbody

######################################################################
# Create a new HybridBody to hold the construction elements
construction_elements = hybrid_bodies.add()
construction_elements.name = "construction_elements"
######################################################################


######################### ENGINE HOUSING #################################

########################################################################
#ENGINE HOUSING PROFILE
######################################################################
eng_spline = hsf.add_new_spline()


eng_spline.add_point(hsf.add_new_point_coord(-16, 0, 70))
eng_spline.add_point(hsf.add_new_point_coord(-25, 0, 85))
eng_spline.add_point(hsf.add_new_point_coord(-28, 0, 95))
eng_spline.add_point(hsf.add_new_point_coord(-28, 0, 100))
eng_spline.add_point(hsf.add_new_point_coord(-28, 0, 105))
eng_spline.add_point(hsf.add_new_point_coord(-28, 0, 135))
eng_spline.add_point(hsf.add_new_point_coord(-26, 0, 145))
eng_spline.add_point(hsf.add_new_point_coord(-26, 0, 105))
eng_spline.add_point(hsf.add_new_point_coord(-26, 0, 100))
eng_spline.add_point(hsf.add_new_point_coord(-26, 0, 95))
eng_spline.add_point(hsf.add_new_point_coord(-23, 0, 85))
eng_spline.add_point(hsf.add_new_point_coord(-16, 0, 70))

construction_elements.append_hybrid_shape(eng_spline)
########################################################################
# POLYLINE FOR ENGINE HOUSING SUPPORT PROFILE
######################################################################
polyline1 = hsf.add_new_polyline()
polyline1.insert_element(hsf.add_new_point_coord (0, 28, 140), 0)
polyline1.insert_element(hsf.add_new_point_coord( 5, 28, 100), 1)
polyline1.insert_element(hsf.add_new_point_coord(0, 28, 127), 2)
polyline1.insert_element(hsf.add_new_point_coord(-5, 28, 100), 3)
polyline1.closure = True

construction_elements.append_hybrid_shape(polyline1)
######################################################################

#################################################################
## ENGINE SUPPORT GUIDE CURVE
######################################################################

eSupport_spline = hsf.add_new_spline()

eSupport_spline.add_point(hsf.add_new_point_coord(0, 28, 100))
eSupport_spline.add_point(hsf.add_new_point_coord(0, 50, 100))

construction_elements.append_hybrid_shape(eSupport_spline)

#################################################################
#Surface revolution for ENGINE HOUSING
######################################################################
#  Get Z axis direction
Zdir = hsf.add_new_direction_by_coord(0, 0, 1)
surfRevolution = hsf.add_new_revol(eng_spline, 0, 360, Zdir)
construction_elements.append_hybrid_shape(surfRevolution)

#######################################################################
#####################################################################
# Create a sweep for Engine Support
######################################################################

eSupport = hsf.add_new_sweep_explicit(polyline1, eSupport_spline)
construction_elements.append_hybrid_shape(eSupport)
    
document.part.update()

####################################################################


###PROPELLER###################################################


### Propeller HUB ##############################################

## DEFINING PLANES FOR PROPELLER PARTS
pHub_plane = hsf.add_new_plane_offset(plane_XY, -135, True)
pHub1_plane = hsf.add_new_plane_offset(plane_XY, -145, True)
pHub2_plane = hsf.add_new_plane_offset(plane_XY, -150, True)
pHub3_plane = hsf.add_new_plane_offset(plane_XY, -127, True)
pHub4_plane = hsf.add_new_plane_offset(plane_XY, -100, True)
pHub5_plane = hsf.add_new_plane_offset(plane_XY, -80, True)
pHub6_plane = hsf.add_new_plane_offset(plane_XY, -60, True)
pHub7_plane = hsf.add_new_plane_offset(plane_XY, -45, True)
pBlade_plane = hsf.add_new_plane_offset(plane_ZX, 8, True)
document.part.update()

## Create a point in Z axis
p_hub = hsf.add_new_point_coord(0, 0, -135)
p_hub.name = "p_z"
construction_elements.append_hybrid_shape(p_hub)

pHub_circle = hsf.add_new_circle_ctr_rad_with_angles(p_hub, pHub_plane, True, 8, 0, 360)
pHub_circle.name = "p_hub_circle"
pHub_circle.set_limitation(0)
construction_elements.append_hybrid_shape(pHub_circle)

p_hub1 = hsf.add_new_point_coord(0, 0, -145)
p_hub1.name = "p1_z"
construction_elements.append_hybrid_shape(p_hub1)

pHub1_circle = hsf.add_new_circle_ctr_rad_with_angles(p_hub1, pHub1_plane, True, 3, 0, 360)
pHub1_circle.name = "p_hub1_circle"
pHub1_circle.set_limitation(0)
construction_elements.append_hybrid_shape(pHub1_circle)


p_hub2 = hsf.add_new_point_coord(0, 0, -150)
p_hub2.name = "p2_z"
construction_elements.append_hybrid_shape(p_hub2)

pHub2_circle = hsf.add_new_circle_ctr_rad_with_angles(p_hub2, pHub2_plane, True, 1, 0, 360)
pHub2_circle.name = "p_hub2_circle"
pHub2_circle.set_limitation(0)
construction_elements.append_hybrid_shape(pHub2_circle)


p_hub3 = hsf.add_new_point_coord(0, 0, -127)
p_hub3.name = "p3_z"
construction_elements.append_hybrid_shape(p_hub3)

pHub3_circle = hsf.add_new_circle_ctr_rad_with_angles(p_hub3, pHub3_plane, True, 8, 0, 360)
pHub3_circle.name = "p_hub3_circle"
pHub3_circle.set_limitation(0)
construction_elements.append_hybrid_shape(pHub3_circle)


p_hub4 = hsf.add_new_point_coord(0, 0, -100)
p_hub4.name = "p4_z"
construction_elements.append_hybrid_shape(p_hub4)

pHub4_circle = hsf.add_new_circle_ctr_rad_with_angles(p_hub4, pHub4_plane, True, 20, 0, 360)
pHub4_circle.name = "p_hub4_circle"
pHub4_circle.set_limitation(0)
construction_elements.append_hybrid_shape(pHub4_circle)

p_hub5 = hsf.add_new_point_coord(0, 0, -80)
p_hub5.name = "p5_z"
construction_elements.append_hybrid_shape(p_hub5)

pHub5_circle = hsf.add_new_circle_ctr_rad_with_angles(p_hub5, pHub5_plane, True, 17, 0, 360)
pHub5_circle.name = "p_hub5_circle"
pHub5_circle.set_limitation(0)
construction_elements.append_hybrid_shape(pHub5_circle)

p_hub6 = hsf.add_new_point_coord(0, 0, -60)
p_hub6.name = "p6_z"
construction_elements.append_hybrid_shape(p_hub6)

pHub6_circle = hsf.add_new_circle_ctr_rad_with_angles(p_hub6, pHub6_plane, True, 13, 0, 360)
pHub6_circle.name = "p_hub6_circle"
pHub6_circle.set_limitation(0)
construction_elements.append_hybrid_shape(pHub6_circle)

p_hub7 = hsf.add_new_point_coord(0, 0, -45)
p_hub7.name = "p7_z"
construction_elements.append_hybrid_shape(p_hub7)

pHub7_circle = hsf.add_new_circle_ctr_rad_with_angles(p_hub7, pHub7_plane, True, 9, 0, 360)
pHub7_circle.name = "p_hub7_circle"
pHub7_circle.set_limitation(0)
construction_elements.append_hybrid_shape(pHub7_circle)

# Update the document
document.part.update()
####################
# PROPELLER HUB LOFT
########################################################
hub_loft = hsf.add_new_loft()
hub_loft.name = "hub loft" 
hub_loft.add_section_to_loft(pHub3_circle, 1, 1)
hub_loft.add_section_to_loft(pHub_circle, 1, 1)
hub_loft.add_section_to_loft(pHub1_circle, 1, 1)
hub_loft.add_section_to_loft(pHub2_circle, 1, 1)

construction_elements.append_hybrid_shape(hub_loft)
document.part.update()

hub_loft1 = hsf.add_new_loft()
hub_loft1.add_section_to_loft(pHub4_circle, 1, 1)
hub_loft1.add_section_to_loft(pHub5_circle, 1, 1)
hub_loft1.add_section_to_loft(pHub6_circle, 1, 1)
hub_loft1.add_section_to_loft(pHub7_circle, 1, 1)
construction_elements.append_hybrid_shape(hub_loft1)
document.part.update()

#################################################################
# PROPELLER BLADE SPLINE: ROOT AND TIP
################################################################
pBlade_spline_r = hsf.add_new_spline()

pBlade_spline_r.add_point(hsf.add_new_point_coord(0, 8, 134))
pBlade_spline_r.add_point(hsf.add_new_point_coord(0.57, 8, 133))
pBlade_spline_r.add_point(hsf.add_new_point_coord(0.86, 8, 132))
pBlade_spline_r.add_point(hsf.add_new_point_coord(0.836, 8, 131))
pBlade_spline_r.add_point(hsf.add_new_point_coord(0.748, 8, 130.46))
pBlade_spline_r.add_point(hsf.add_new_point_coord(0.443, 8, 129.68))
pBlade_spline_r.add_point(hsf.add_new_point_coord(0, 8, 129))
pBlade_spline_r.add_point(hsf.add_new_point_coord(-0.558, 8, 129.66))
pBlade_spline_r.add_point(hsf.add_new_point_coord(-0.79, 8,130.57))
pBlade_spline_r.add_point(hsf.add_new_point_coord(-0.875, 8, 131.45))
pBlade_spline_r.add_point(hsf.add_new_point_coord(-0.762, 8, 132.638))
pBlade_spline_r.add_point(hsf.add_new_point_coord(-0.457, 8, 133.513))
pBlade_spline_r.add_point(hsf.add_new_point_coord(0, 8, 134))


construction_elements.append_hybrid_shape(pBlade_spline_r)

########################################################################################
## MATHEMATIC FORMULALATION FOR TURNING PROPELLER BLADE TIP PROFILE 30 degrees TO Y AXIS
#########################################################################################

# Define cos and sin for 30 degrees
pBlade_spline_t = hsf.add_new_spline()
cos_30 = math.sqrt(3) / 2
sin_30 = 1 / 2

def rotate_y(x, y, z, cx, cz):
    # Translate to the origin
    x_translated = x - cx
    z_translated = z - cz

    # Apply the rotation
    x_rotated = x_translated * cos_30 + z_translated * sin_30
    z_rotated = -x_translated * sin_30 + z_translated * cos_30

    # Translate back to the original position
    x_final = x_rotated + cx
    z_final = z_rotated + cz
    return x_final, y, z_final

# Original points (x, y, z)
points = [
    (0, 23, 135.15),
    (0.386, 23, 134.46),
    (0.594, 23, 133.67),
    (0.788, 23, 132.84),
    (1.037, 23, 132.18),
    (1.245, 23, 131.46),
    (1.176, 23, 130.344),
    (0.885, 23, 129.16),
    (0.580, 23, 128.19),
    (0, 23, 127.279),
    (-0.01, 23, 127.79),
    (-0.17, 23, 128.27),
    (-0.42, 23, 128.70),
    (-0.78, 23, 129.22),
    (-1.02, 23, 130.36),
    (-0.64, 23, 133.04),
    (-0.49, 23, 133.72),
    (0, 23, 135.15)
]

# Calculate center of rotation (average x and z)
center_x = sum([p[0] for p in points]) / len(points)
center_z = sum([p[2] for p in points]) / len(points)

# Add rotated points to the spline
for point in points:
    x_rot, y_rot, z_rot = rotate_y(point[0], point[1], point[2], center_x, center_z)
    pBlade_spline_t.add_point(hsf.add_new_point_coord(x_rot, y_rot, z_rot))

# Append wroot_spline
construction_elements.append_hybrid_shape(pBlade_spline_t)
document.part.update()
######################################################################
##PROPELLER BLADE LOFT
#######################################################################
pBlade_loft = hsf.add_new_loft()
pBlade_loft.name = "Propeller Blade Loft" 
pBlade_loft.add_section_to_loft(pBlade_spline_r, 1, 1)
pBlade_loft.add_section_to_loft(pBlade_spline_t, 1, 1)

construction_elements.append_hybrid_shape(pBlade_loft)
document.part.update()


############################################ WING ###################################################

#####################################################
# WING TIP PROFILE
#####################################################
wtip_spline = hsf.add_new_spline()

wtip_spline.add_point(hsf.add_new_point_coord(-210, 18, 75))
wtip_spline.add_point(hsf.add_new_point_coord(-210, 23, 60))
wtip_spline.add_point(hsf.add_new_point_coord(-210, 23.5, 45))
wtip_spline.add_point(hsf.add_new_point_coord(-210, 22.5, 31))
wtip_spline.add_point(hsf.add_new_point_coord(-210, 20.5, 16))
wtip_spline.add_point(hsf.add_new_point_coord(-210, 18, 0))

wtip_spline.add_point(hsf.add_new_point_coord(-210, 17.3, 16))
wtip_spline.add_point(hsf.add_new_point_coord(-210, 16.8, 31))
wtip_spline.add_point(hsf.add_new_point_coord(-210, 16, 45))
wtip_spline.add_point(hsf.add_new_point_coord(-210, 15.6, 60))
wtip_spline.add_point(hsf.add_new_point_coord(-210, 18, 75))


construction_elements.append_hybrid_shape(wtip_spline)

################################################################
# WINGLET PROFILE
################################################################
winglet_spline = hsf.add_new_spline()
winglet_spline.add_point(hsf.add_new_point_coord(-240, 31.5, 75))
winglet_spline.add_point(hsf.add_new_point_coord(-240, 33, 72))
winglet_spline.add_point(hsf.add_new_point_coord(-240, 33.8, 70.45))
winglet_spline.add_point(hsf.add_new_point_coord(-240, 33.98, 67.8))
winglet_spline.add_point(hsf.add_new_point_coord(-240, 33.90, 65.76))
winglet_spline.add_point(hsf.add_new_point_coord(-240, 33.66, 63.7))
winglet_spline.add_point(hsf.add_new_point_coord(-240, 33.4, 61.2))
winglet_spline.add_point(hsf.add_new_point_coord(-240, 32.2, 64))
winglet_spline.add_point(hsf.add_new_point_coord(-240, 32.17, 66))
winglet_spline.add_point(hsf.add_new_point_coord(-240, 31.9, 67.7))
winglet_spline.add_point(hsf.add_new_point_coord(-240, 31.7, 69))
winglet_spline.add_point(hsf.add_new_point_coord(-240, 31.6, 72))
winglet_spline.add_point(hsf.add_new_point_coord(-240, 31.3, 73))
winglet_spline.add_point(hsf.add_new_point_coord(-240, 31.5, 74))
winglet_spline.add_point(hsf.add_new_point_coord(-240, 31.5, 75))

construction_elements.append_hybrid_shape(winglet_spline)

################################################################
## WING ROOT PROFILE
######################################################################

wroot_spline = hsf.add_new_spline()

wroot_spline.add_point(hsf.add_new_point_coord(90, 67, 177))
wroot_spline.add_point(hsf.add_new_point_coord(90, 78, 160))
wroot_spline.add_point(hsf.add_new_point_coord(90, 82, 142))
wroot_spline.add_point(hsf.add_new_point_coord(90, 84, 120))
wroot_spline.add_point(hsf.add_new_point_coord(90, 83, 106))
wroot_spline.add_point(hsf.add_new_point_coord(90, 81, 72))
wroot_spline.add_point(hsf.add_new_point_coord(90, 77.5, 50))
wroot_spline.add_point(hsf.add_new_point_coord(90, 75, 35))
wroot_spline.add_point(hsf.add_new_point_coord(90, 68, 0))
wroot_spline.add_point(hsf.add_new_point_coord(90, 65, 46))
wroot_spline.add_point(hsf.add_new_point_coord(90, 64, 71))
wroot_spline.add_point(hsf.add_new_point_coord(90, 63, 106))
wroot_spline.add_point(hsf.add_new_point_coord(90, 62, 133))
wroot_spline.add_point(hsf.add_new_point_coord(90, 61, 160))
wroot_spline.add_point(hsf.add_new_point_coord(90, 67, 177))


construction_elements.append_hybrid_shape(wroot_spline)

# WING TO BODY PROFILE
################################################################
bodyw_spline = hsf.add_new_spline()

bodyw_spline.add_point(hsf.add_new_point_coord(230, 117, 207))
bodyw_spline.add_point(hsf.add_new_point_coord(230, 128, 190))
bodyw_spline.add_point(hsf.add_new_point_coord(230, 132, 172))
bodyw_spline.add_point(hsf.add_new_point_coord(230, 134, 150))
bodyw_spline.add_point(hsf.add_new_point_coord(230, 133, 136))
bodyw_spline.add_point(hsf.add_new_point_coord(230, 131, 102))
bodyw_spline.add_point(hsf.add_new_point_coord(230, 127.5, 80))
bodyw_spline.add_point(hsf.add_new_point_coord(230, 125, 65))
bodyw_spline.add_point(hsf.add_new_point_coord(230, 118, 30))
bodyw_spline.add_point(hsf.add_new_point_coord(230, 115, 76))
bodyw_spline.add_point(hsf.add_new_point_coord(230, 114, 101))
bodyw_spline.add_point(hsf.add_new_point_coord(230, 113, 136))
bodyw_spline.add_point(hsf.add_new_point_coord(230, 112, 163))
bodyw_spline.add_point(hsf.add_new_point_coord(230, 111, 190))
bodyw_spline.add_point(hsf.add_new_point_coord(230, 117, 207))


construction_elements.append_hybrid_shape(bodyw_spline)

#####################################################################
#Loft for wing root and wing tip
#########################################################################
wing_surf = hsf.add_new_loft()
wing_surf.name = "wing_surf" 
wing_surf.add_section_to_loft(wtip_spline, 1, 1)
wing_surf.add_section_to_loft(wroot_spline, 1, 1)
construction_elements.append_hybrid_shape(wing_surf)
###########################################################################
#Loft for winglet and wing tip
############################################################################
wing_let = hsf.add_new_loft()
wing_let.name = "wing_let" 
wing_let.add_section_to_loft(wtip_spline, 1, 1)
wing_let.add_section_to_loft(winglet_spline, 1, 1)
construction_elements.append_hybrid_shape(wing_let)
############################################################################
# Loft for wingroot and body
######################################################################
wing_b = hsf.add_new_loft()
wing_b.name = "wing_let" 
wing_b.add_section_to_loft(wroot_spline, 1, 1)
wing_b.add_section_to_loft(bodyw_spline, 1, 1)
construction_elements.append_hybrid_shape(wing_b)
document.part.update()
#####################################################################

#################################################################
# VerTAIL ROOT  PROFILE
######################################################################

hortail_root = hsf.add_new_polyline()
hortail_root.insert_element(hsf.add_new_point_coord (299, 170, -300), 1)
hortail_root.insert_element(hsf.add_new_point_coord( 299, 160, -418), 2)
hortail_root.insert_element(hsf.add_new_point_coord(299, 180, -418), 3)
hortail_root.closure = True

# Append polyline
construction_elements.append_hybrid_shape(hortail_root)
    
# Update the document
document.part.update()
################################################################

# HorTAIL Tip  PROFILE
######################################################################

hortail_tip = hsf.add_new_polyline()
hortail_tip.insert_element(hsf.add_new_point_coord (170, 150, -420), 1)
hortail_tip.insert_element(hsf.add_new_point_coord( 170, 160, -480), 2)
hortail_tip.insert_element(hsf.add_new_point_coord(170, 170, -480), 3)
hortail_tip.closure = True

# Append polyline
construction_elements.append_hybrid_shape(hortail_tip)
    
# Update the document
document.part.update()

################################################################
# PLANE BODY
######################################################################

######## DEFINING PLANES FOR BODY #########################################
mirror_plane = hsf.add_new_plane_offset(plane_YZ, -300, True)
pbodycockpit1_plane = hsf.add_new_plane_offset(plane_XY, -282, True)
pbodycockpit2_plane = hsf.add_new_plane_offset(plane_XY, -350, True)
pbodycockpit3_plane = hsf.add_new_plane_offset(plane_XY, -420, True)
pbodycockpit4_plane = hsf.add_new_plane_offset(plane_XY, -455, True)
pbodytailpit5_plane = hsf.add_new_plane_offset(plane_XY, 118, True)
pbodytailpit6_plane = hsf.add_new_plane_offset(plane_XY, 210, True)
pbodytailpit7_plane = hsf.add_new_plane_offset(plane_XY, 320, True)
pbodytailpit8_plane = hsf.add_new_plane_offset(plane_XY, 434, True)
hori_tail_plane = hsf.add_new_plane_offset(mirror_plane, 20, True)
document.part.update()
######################################################################################################
# CENTRAL FUSELAGE
######################################################################################################
plane_body = hsf.add_new_cylinder(hsf.add_new_point_coord(299, 130, 82), 80, 200, 200, hsf.add_new_direction_by_coord(0, 0, 1))
construction_elements.append_hybrid_shape(plane_body)
########################################################################################################
## FRONT FUSELAGE
########################################################################################################
p_cockpit1 = hsf.add_new_point_coord(299,130, -282)
p_cockpit1.name = "p8_z"
construction_elements.append_hybrid_shape(p_cockpit1)

pCockpit_circle1 = hsf.add_new_circle_ctr_rad_with_angles(p_cockpit1, pbodycockpit1_plane, True, 80, 0, 360)
pCockpit_circle1.name = "fuselagecircle1f"
pCockpit_circle1.set_limitation(0)
construction_elements.append_hybrid_shape(pCockpit_circle1)

p_cockpit2 = hsf.add_new_point_coord(299, 125, -350)
p_cockpit2.name = "p9_z"
construction_elements.append_hybrid_shape(p_cockpit2)

pCockpit_circle2 = hsf.add_new_circle_ctr_rad_with_angles(p_cockpit2, pbodycockpit2_plane, True, 75, 0, 360)
pCockpit_circle2.name = "fuselagecircle2f"
pCockpit_circle2.set_limitation(0)
construction_elements.append_hybrid_shape(pCockpit_circle2)

p_cockpit3 = hsf.add_new_point_coord(299, 95, -420)
p_cockpit3.name = "p10_z"
construction_elements.append_hybrid_shape(p_cockpit3)

pCockpit_circle3 = hsf.add_new_circle_ctr_rad_with_angles(p_cockpit3, pbodycockpit3_plane, True, 45, 0, 360)
pCockpit_circle3.name = "fuselagecircle3f"
pCockpit_circle3.set_limitation(0)
construction_elements.append_hybrid_shape(pCockpit_circle3)

p_cockpit4 = hsf.add_new_point_coord(299, 88, -455)
p_cockpit4.name = "p11_z"
construction_elements.append_hybrid_shape(p_cockpit4)

pCockpit_circle4 = hsf.add_new_circle_ctr_rad_with_angles(p_cockpit4, pbodycockpit4_plane, True, 35, 0, 360)
pCockpit_circle4.name = "fuselagecircle4f"
pCockpit_circle4.set_limitation(0)
construction_elements.append_hybrid_shape(pCockpit_circle4)

p_tailpit5 = hsf.add_new_point_coord(299, 130, 118)
p_tailpit5.name = "p12_z"
construction_elements.append_hybrid_shape(p_tailpit5)

ptailpit_circle5 = hsf.add_new_circle_ctr_rad_with_angles(p_tailpit5, pbodytailpit5_plane, True, 80, 0, 360)
ptailpit_circle5.name = "fuselagecircle1r"
ptailpit_circle5.set_limitation(0)
construction_elements.append_hybrid_shape(ptailpit_circle5)

p_tailpit6 = hsf.add_new_point_coord(299, 135, 210)
p_tailpit6.name = "p13_z"
construction_elements.append_hybrid_shape(p_tailpit6)

ptailpit_circle6 = hsf.add_new_circle_ctr_rad_with_angles(p_tailpit6, pbodytailpit6_plane, True, 75, 0, 360)
ptailpit_circle6.name = "fuselagecircle2r"
ptailpit_circle6.set_limitation(0)
construction_elements.append_hybrid_shape(ptailpit_circle6)

p_tailpit7 = hsf.add_new_point_coord(299, 147, 320)
p_tailpit7.name = "p14_z"
construction_elements.append_hybrid_shape(p_tailpit7)

ptailpit_circle7 = hsf.add_new_circle_ctr_rad_with_angles(p_tailpit7, pbodytailpit7_plane, True, 63, 0, 360)
ptailpit_circle7.name = "fuselagecircle3r"
ptailpit_circle7.set_limitation(0)
construction_elements.append_hybrid_shape(ptailpit_circle7)

p_tailpit8 = hsf.add_new_point_coord(299, 185, 425)
p_tailpit8.name = "p15_z"
construction_elements.append_hybrid_shape(p_tailpit8)

ptailpit_circle8 = hsf.add_new_circle_ctr_rad_with_angles(p_tailpit8, pbodytailpit8_plane, True, 25, 0, 360)
ptailpit_circle8.name = "fuselagecircle4r"
ptailpit_circle8.set_limitation(0)
construction_elements.append_hybrid_shape(ptailpit_circle8)



# Create an axis system with default entries (equal to absolute)
axis_sys1 = part.axis_systems.add()
ref_axis =  part.create_reference_from_object(axis_sys1)

# Update the document
document.part.update()

# Arguments : (i_center, i_axis, i_radius, i_begin_parallel_angle, i_end_parallel_angle, i_begin_meridian_angle, i_end_meridian_angle)
nose = hsf.add_new_sphere(hsf.add_new_point_coord(299, 88, 455), ref_axis, 35, -90, 90, 0, 360)
nose.limitation = 0 # 0 to specify sphere angles, 1 to fully closed sphere
construction_elements.append_hybrid_shape(nose)


document.part.update()
###################################################################
## LOFT FOR FRONT FUSELAGE
##################################################################
cockpit_loft = hsf.add_new_loft()
cockpit_loft.name = "cockpit loft" 
cockpit_loft.add_section_to_loft(pCockpit_circle1, 1, 1)
cockpit_loft.add_section_to_loft(pCockpit_circle2, 1, 1)
cockpit_loft.add_section_to_loft(pCockpit_circle3, 1, 1)
cockpit_loft.add_section_to_loft(pCockpit_circle4, 1, 1)
construction_elements.append_hybrid_shape(cockpit_loft)
###################################################################
## LOFT FOR REAR FUSELAGE
##################################################################
tailpit_loft = hsf.add_new_loft()
tailpit_loft.name = "tail loft" 
tailpit_loft.add_section_to_loft(ptailpit_circle5, 1, 1)
tailpit_loft.add_section_to_loft(ptailpit_circle6, 1, 1)
tailpit_loft.add_section_to_loft(ptailpit_circle7, 1, 1)
tailpit_loft.add_section_to_loft(ptailpit_circle8, 1, 1)
construction_elements.append_hybrid_shape(tailpit_loft)
document.part.update()
####################################################################
######### TAIL PROFILE ##############################################
######################################################################
tail_vert_line = hsf.add_new_polyline()
tail_vert_spline = hsf.add_new_spline()


tail_vert_line.insert_element(hsf.add_new_point_coord (310.5,190, -428), 2)
tail_vert_line.insert_element(hsf.add_new_point_coord( 287.5, 190, -428), 3)
tail_vert_line.insert_element(hsf.add_new_point_coord(287.5, 190, -310), 4)
tail_vert_line.insert_element(hsf.add_new_point_coord(310.5, 190, -310), 1)
tail_vert_line.closure = True
construction_elements.append_hybrid_shape(tail_vert_line)

tail_vert1_line = hsf.add_new_polyline()
tail_vert1_line.insert_element(hsf.add_new_point_coord (302, 360, -468), 2)
tail_vert1_line.insert_element(hsf.add_new_point_coord( 296, 360, -468), 3)
tail_vert1_line.insert_element(hsf.add_new_point_coord(296, 360, -420), 4)
tail_vert1_line.insert_element(hsf.add_new_point_coord(302, 360, -420), 1)
construction_elements.append_hybrid_shape(tail_vert1_line)
tail_vert1_line.closure = True  
document.part.update()


###################################################################
## LOFT FOR VERTICAL TAIL
#################################################################
vtail_loft = hsf.add_new_loft()
vtail_loft.name = "vertical tail" 
vtail_loft.add_section_to_loft(tail_vert1_line, 1, 1)
vtail_loft.add_section_to_loft(tail_vert_line, 1, 1)
construction_elements.append_hybrid_shape(vtail_loft)
###################################################################
## LOFT FOR HORIZONTAL TAIL
#################################################################
hortail_loft = hsf.add_new_loft()
hortail_loft.name = "vertical tail" 
hortail_loft.add_section_to_loft(hortail_tip, 1, 1)
hortail_loft.add_section_to_loft(hortail_root, 1, 1)
construction_elements.append_hybrid_shape(hortail_loft)

document.part.update()

##################################################################
#CONVERT TO BODY
##################################################################
part.in_work_object = partbody
wing_1 = shpfac.add_new_close_surface(wing_surf)
wing_2 = shpfac.add_new_close_surface(wing_let)
wing_3 = shpfac.add_new_close_surface(wing_b)
engineHold = shpfac.add_new_close_surface(eSupport)
engineHouse = shpfac.add_new_close_surface(surfRevolution)
prop_front_hub = shpfac.add_new_close_surface(hub_loft)
prop_rear_hub = shpfac.add_new_close_surface(hub_loft1)
vart_tail = shpfac.add_new_close_surface(vtail_loft)
hor_tail = shpfac.add_new_close_surface(hortail_loft)
cockpit = shpfac.add_new_close_surface(cockpit_loft)
tailpit = shpfac.add_new_close_surface(tailpit_loft)
body = shpfac.add_new_close_surface(plane_body)
blade = shpfac.add_new_close_surface(pBlade_loft)
cnose = shpfac.add_new_close_surface(nose)

document.part.update()

####################################################################
#################CIRCULAR PATTERN FOR PROPELELR BLADE############
####################################################################
# Create a global reference point
p_0 = hsf.add_new_point_coord(0, 0, 0)
p_0.name = "p_0"
construction_elements.append_hybrid_shape(p_0)

# Create a point in Z axis
p_blade = hsf.add_new_point_coord(0, 0, 200)
p_blade.name = "p_blade"
construction_elements.append_hybrid_shape(p_blade)

# Z dir
z_dir = hsf.add_new_line_pt_pt(p_0,p_blade)
z_dir.name = "z_dir"
construction_elements.append_hybrid_shape(z_dir)

# Set PartBody as a working object
part.in_work_object = partbody
# Create circular pattern around Z axis
circ_pattern_Z = shpfac.add_new_circ_pattern(blade, 1, 24, 0, 15, 1, 1, z_dir, z_dir, True, 0, True)
document.part.update()

######################################################################
## Mirror WING AND ENGINE HOUSING
####################################################################
mirror_1 = shpfac.add_new_mirror(mirror_plane)
document.part.update()
#######################################################################
# HIDING THE SURFACES
selection.clear()
selection.add(construction_elements)
selection.vis_properties.set_show(1) # 0: Show / 1: Hide
selection.clear()
#######################################################################
# Coloring THE SURFACES
selection.clear()
selection.add(hor_tail)
selection.vis_properties.set_real_color(160,160,160,1)
selection.clear()
selection.add(body)
selection.vis_properties.set_real_color(160,160,160,1)
selection.clear()
selection.add(cockpit)
selection.vis_properties.set_real_color(160,160,160,1)
selection.clear()
selection.add(tailpit)
selection.vis_properties.set_real_color(160,160,160,1)
selection.clear()
selection.add(vart_tail)
selection.vis_properties.set_real_color(243,243,243,1)
selection.clear()
selection.add(blade)
selection.vis_properties.set_real_color(98,122,157,1)
selection.clear()
selection.add(prop_front_hub)
selection.vis_properties.set_real_color(52,52,52,1)
selection.clear()
selection.add(cnose)
selection.vis_properties.set_real_color(160,160,160,1)
selection.clear()
####################################################################



























