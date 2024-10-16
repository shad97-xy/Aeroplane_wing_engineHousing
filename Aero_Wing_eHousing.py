######################################################################
# PYCATIA LIBRARIES
from pycatia import catia
from pycatia.mec_mod_interfaces.part_document import PartDocument

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

# Append spline
construction_elements.append_hybrid_shape(eng_spline)
    
# Update the document
document.part.update()
################################################################


# WING TIP PROFILE
######################################################################

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

# Append wtip_spline
construction_elements.append_hybrid_shape(wtip_spline)
# Update the document
document.part.update()
################################################################

#WINGLET PROFILE
################################################################
winglet_spline = hsf.add_new_spline()
# spline.add_point(hsf.add_new_point_coord(L, 0, 0))
# spline.add_point(hsf.add_new_point_coord(L/2, 0, L/8))
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
# Append wtip_spline
construction_elements.append_hybrid_shape(winglet_spline)
# Update the document
document.part.update()
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

# Append wroot_spline
construction_elements.append_hybrid_shape(wroot_spline)
# Update the document
document.part.update()
# ################################################################


## ENGINE SUPPORT GUIDE CURVE
######################################################################

eSupport_spline = hsf.add_new_spline()

eSupport_spline.add_point(hsf.add_new_point_coord(0, 28, 100))
eSupport_spline.add_point(hsf.add_new_point_coord(0, 50, 100))

# Append eSupport_spline
construction_elements.append_hybrid_shape(eSupport_spline)
# Update the document
document.part.update()
#################################################################

# WING TO BODY SPLINE
################################################################
bodyw_spline = hsf.add_new_spline()

bodyw_spline.add_point(hsf.add_new_point_coord(160, 117, 177))
bodyw_spline.add_point(hsf.add_new_point_coord(160, 128, 160))
bodyw_spline.add_point(hsf.add_new_point_coord(160, 132, 142))
bodyw_spline.add_point(hsf.add_new_point_coord(160, 134, 120))
bodyw_spline.add_point(hsf.add_new_point_coord(160, 133, 106))
bodyw_spline.add_point(hsf.add_new_point_coord(160, 131, 72))
bodyw_spline.add_point(hsf.add_new_point_coord(160, 127.5, 50))
bodyw_spline.add_point(hsf.add_new_point_coord(160, 125, 35))
bodyw_spline.add_point(hsf.add_new_point_coord(160, 118, 0))
bodyw_spline.add_point(hsf.add_new_point_coord(160, 115, 46))
bodyw_spline.add_point(hsf.add_new_point_coord(160, 114, 71))
bodyw_spline.add_point(hsf.add_new_point_coord(160, 113, 106))
bodyw_spline.add_point(hsf.add_new_point_coord(160, 112, 133))
bodyw_spline.add_point(hsf.add_new_point_coord(160, 111, 160))
bodyw_spline.add_point(hsf.add_new_point_coord(160, 117, 177))

# Append wroot_spline
construction_elements.append_hybrid_shape(bodyw_spline)
# Update the document
document.part.update()
#################################################################


# POLYLINE FOR ENGINE HOUSING SUPPORT PROFILE
######################################################################
polyline1 = hsf.add_new_polyline()
polyline1.insert_element(hsf.add_new_point_coord (0, 28, 140), 0)
polyline1.insert_element(hsf.add_new_point_coord( 5, 28, 100), 1)
polyline1.insert_element(hsf.add_new_point_coord(0, 28, 127), 2)
polyline1.insert_element(hsf.add_new_point_coord(-5, 28, 100), 3)
polyline1.closure = True

# Append polyline
construction_elements.append_hybrid_shape(polyline1)
    
# Update the document
document.part.update()
######################################################################

# Create surface revolution for ENGINE HOUSING
######################################################################

#  Get Z axis direction
Zdir = hsf.add_new_direction_by_coord(0, 0, 1)

surfRevolution = hsf.add_new_revol(eng_spline, 0, 360, Zdir)

# Append surface
construction_elements.append_hybrid_shape(surfRevolution)

# Update the document
document.part.update()
#######################################################################

#Create lofted surface and fill wing root and wing tip
#########################################################################

wing_surf = hsf.add_new_loft()
wing_surf.name = "wing_surf" 
wing_surf.add_section_to_loft(wtip_spline, 1, 1)
wing_surf.add_section_to_loft(wroot_spline, 1, 1)
# wing_surf.add_section_to_loft(spline4, 1, 1)
construction_elements.append_hybrid_shape(wing_surf)

wing_root_filled = hsf.add_new_fill()
wing_root_filled.name = "wing_root_filled" 
wing_root_filled.add_bound(wroot_spline)
construction_elements.append_hybrid_shape(wing_root_filled)

wing_tip_filled = hsf.add_new_fill()
wing_tip_filled.name = "wing_tip_filled" 
wing_tip_filled.add_bound(wtip_spline)
construction_elements.append_hybrid_shape(wing_tip_filled)

wing_surf_complete = hsf.add_new_join(wing_surf, wing_root_filled)
wing_surf_complete.name = "wing_surf_complete" 
wing_surf_complete.add_element(wing_tip_filled)
construction_elements.append_hybrid_shape(wing_surf_complete)

# Update the document
document.part.update()
###########################################################################


# Create lofted surface and fill winglet and wing tip
############################################################################

wing_let = hsf.add_new_loft()
wing_let.name = "wing_let" 
wing_let.add_section_to_loft(wtip_spline, 1, 1)
wing_let.add_section_to_loft(winglet_spline, 1, 1)
construction_elements.append_hybrid_shape(wing_let)

wing_let_filled = hsf.add_new_fill()
wing_let_filled.name = "wing_let_filled" 
wing_let_filled.add_bound(winglet_spline)
construction_elements.append_hybrid_shape(wing_let_filled)


# Create lofted surface and fill wingroot and body
######################################################################

wing_b = hsf.add_new_loft()
wing_b.name = "wing_let" 
wing_b.add_section_to_loft(wroot_spline, 1, 1)
wing_b.add_section_to_loft(bodyw_spline, 1, 1)
construction_elements.append_hybrid_shape(wing_b)

wing_b_filled = hsf.add_new_fill()
wing_b_filled.name = "wing_b_filled" 
wing_b_filled.add_bound(bodyw_spline)
construction_elements.append_hybrid_shape(wing_b_filled)

# Update the document
document.part.update()
#####################################################################

# Create a sweep for Engine Support
######################################################################

sweep = hsf.add_new_sweep_explicit(polyline1, eSupport_spline)
construction_elements.append_hybrid_shape(sweep)
    
# Update the document
document.part.update()
####################################################################


























