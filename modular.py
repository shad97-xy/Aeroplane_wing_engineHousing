######################################################################
# PYCATIA LIBRARIES
######################################################################
from pycatia import catia
from pycatia.mec_mod_interfaces.part_document import PartDocument
from pycatia.in_interfaces.camera_3d import Camera3D
from pycatia.in_interfaces.viewer_3d import Viewer3D
import math
import tkinter as tk
from tkinter import messagebox
from PIL import ImageTk, Image
####################################################################
# Tkinter for custom user input for propeller blade
#####################################################################

# Get the input value and validate it as an integer
def submit():
    global h
    global no_of_blades 
    global wing_angle_degrees
    no_of_blades = entry_blades.get()
    wing_angle_degrees = entry_angle.get()
   
    
    def isNumber(x):
        if isinstance(x, int):
            return True
        elif isinstance(x, str) and x.lstrip('-').isdigit():
            return True
        else:
            return False
   
    try:
        if isNumber(no_of_blades) and int(no_of_blades) <= 24 and isNumber(wing_angle_degrees) and -15 <= int(wing_angle_degrees) <= 15 :
            # Convert wing angle to a range of 0-160
            h = 84 + (int(wing_angle_degrees) * 40) / 15
            print(h)
            messagebox.showinfo("Success", f"Number of propeller blades: {no_of_blades} \n Wing angle: {wing_angle_degrees}")
            root.destroy()
        else:
            messagebox.showwarning("Warning", "Please enter valid numbers within the range") 
               
        
    except ValueError:
        # If input is not a valid integer
        messagebox.showerror("Error", "Please enter a valid integer for the number of propeller blades and wing angle.")
        
      

# Create the main window for the user prompt
root = tk.Tk()
root.title("Airplane Customization")
root.geometry("400x300")

# Add an image (you need to replace 'airplane_logo.png' with the path to your airplane logo image)
try:
    image = Image.open("airplane_logo.jpg")
    image = image.resize((100, 100))  # Resize to fit
    photo = ImageTk.PhotoImage(image)
    label_image = tk.Label(root, image=photo)
    label_image.pack(pady=10)
except:
    messagebox.showerror("Error", "Failed to load airplane logo. Please make sure the image exists.")

# Create a label and entry for the number of blades
label_blades = tk.Label(root, text="Enter the number of propeller blades (0-24): ")
label_blades.pack(pady=5)
entry_blades = tk.Entry(root)
entry_blades.pack(pady=5)

# Wing Angle input
label_angle = tk.Label(root, text="Enter wing angle with the horizontal (-15 to 15 degrees):")
label_angle.pack(pady=5)
entry_angle = tk.Entry(root)
entry_angle.pack(pady=5)

# Create a submit button
submit_button = tk.Button(root, text="Submit", command=submit)
submit_button.pack(pady=10)

# Run the Tkinter event loop
root.mainloop()

#####################################################################
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
########################################################################
document: PartDocument = application.active_document        # Get active document
part = document.part                                        # Get Part
partbody = part.bodies[0]                                   # Get default PartBody by index
# partbody = part.bodies.item("PartBody")                     # Get default PartBody by name
sketches = partbody.sketches                                # Get sketches on PartBody 
hybrid_bodies = part.hybrid_bodies                          # Get Hybrid Bodies 
hsf = part.hybrid_shape_factory                             # Get Hybrid Shape Factory 
shpfac = part.shape_factory                                 # Get Shape Factory 
selection = document.selection                              # Get document selection

##########################################################################
# ##Get camera properties
active_window = application.active_window
viewer_3d = Viewer3D(active_window.active_viewer.com_object)
camera_3d = Camera3D(document.cameras.item(1).com_object)
viewpoint_3d = viewer_3d.viewpoint_3d
viewpoint_3d.put_up_direction(o_up=(1.5,1.5,1))
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
#######################################################################
############################PROPELLER##################################

##########################Propeller HUB ###############################
# Create a global reference point

def add_new_point_coord_and_append_hybrid_shape(coords, name):
    point = hsf.add_new_point_coord(*coords)
    point.name = name
    construction_elements.append_hybrid_shape(point)
    return point

def add_new_circle_ctr_rad_with_angles(centre_point, support_plane, radius, s_angle, e_angle, name):
    circle = hsf.add_new_circle_ctr_rad_with_angles(centre_point, support_plane, True, radius, s_angle, e_angle)
    circle.name = name
    circle.set_limitation(0)
    construction_elements.append_hybrid_shape(circle)
    
def create_loft(loft_name, sections):
    # Create a new loft and assign its name
    loft = hsf.add_new_loft()
    loft.name = loft_name
    
    # Add each section to the loft
    for section in sections:
        loft.add_section_to_loft(section, 1, 1)
    
    # Append the loft to the construction elements and update the document
    construction_elements.append_hybrid_shape(loft)
    document.part.update()
    return loft
  
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

p_blade = add_new_point_coord_and_append_hybrid_shape((108,25,200), "p_blade")
p_0 = add_new_point_coord_and_append_hybrid_shape((108,25,0), "p_0")
p_hub = add_new_point_coord_and_append_hybrid_shape((108,25,-135), "p_z")
p_hub1 = add_new_point_coord_and_append_hybrid_shape((108, 25, -145), "p1_z")
p_hub2 = add_new_point_coord_and_append_hybrid_shape((108, 25, -150), "p2_z")
p_hub3 = add_new_point_coord_and_append_hybrid_shape((108, 25 , -127), "p3_z")
p_hub4 = add_new_point_coord_and_append_hybrid_shape((108, 25 , -100), "p4_z")
p_hub5 = add_new_point_coord_and_append_hybrid_shape((108, 25, -80), "p5_z")
p_hub6 = add_new_point_coord_and_append_hybrid_shape((108, 25 , -60), "p6_z")
p_hub7 = add_new_point_coord_and_append_hybrid_shape((108, 25 , -45), "p7_z")
                                                                                                                                                  
pHub_circle = add_new_circle_ctr_rad_with_angles(p_hub, pHub_plane, 8, 0, 360, "p_hub_circle")
pHub1_circle = add_new_circle_ctr_rad_with_angles(p_hub1, pHub1_plane, 3, 0, 360, "p_hub1_circle")
pHub2_circle = add_new_circle_ctr_rad_with_angles(p_hub2, pHub2_plane, 1, 0, 360, "p_hub2_circle")
pHub3_circle = add_new_circle_ctr_rad_with_angles(p_hub3, pHub3_plane, 8, 0, 360, "p_hub3_circle")
pHub4_circle = add_new_circle_ctr_rad_with_angles(p_hub4, pHub4_plane, 20, 0, 360, "p_hub4_circle")
pHub5_circle = add_new_circle_ctr_rad_with_angles(p_hub5, pHub5_plane, 17, 0, 360, "p_hub5_circle")
pHub6_circle = add_new_circle_ctr_rad_with_angles(p_hub6, pHub6_plane, 13, 0, 360, "p_hub6_circle")
pHub7_circle = add_new_circle_ctr_rad_with_angles(p_hub7, pHub7_plane, 9, 0, 360, "p_hub7_circle")


#######################################################
# PROPELLER HUB LOFT
########################################################

hub_sections = [pHub3_circle, pHub_circle, pHub1_circle, pHub2_circle]
hub_sections1 = [pHub4_circle, pHub5_circle, pHub6_circle, pHub7_circle]

hub_loft = create_loft("hub loft", hub_sections)
hub_loft1 = create_loft("hub loft 1", hub_sections1)
document.part.update()

## Z axis referance for engine housing revolution and circular pattern of blades
## Z dir
z_dir = hsf.add_new_line_pt_pt(p_0,p_blade)
z_dir.name = "z_dir"
construction_elements.append_hybrid_shape(z_dir)
document.part.update()
######################### ENGINE HOUSING #################################

########################################################################
#ENGINE HOUSING PROFILE
######################################################################
eng_spline = hsf.add_new_spline()

# Add points to the spline
points1 = [
    (92, 25, 70),
    (83, 25, 85),
    (80, 25, 95),
    (80, 25, 100),
    (80, 25, 105),
    (80, 25, 135),
    (82, 25, 145),
    (82, 25, 105),
    (82, 25, 100),
    (82, 25, 95),
    (85, 25, 85),
    (92, 25, 70)  
]

for point in points1:
    eng_spline.add_point(hsf.add_new_point_coord(*point))

construction_elements.append_hybrid_shape(eng_spline)

########################################################################
# POLYLINE FOR ENGINE HOUSING SUPPORT PROFILE
######################################################################
polyline1 = hsf.add_new_polyline()
polyline_points = [
    (108, 51, 140),
    (113, 51, 100),
    (108, 51, 127),
    (103, 51, 100)
]

for index, point in enumerate(polyline_points):
    polyline1.insert_element(hsf.add_new_point_coord(*point), index)

polyline1.closure = True
construction_elements.append_hybrid_shape(polyline1)
######################################################################

#################################################################
## ENGINE SUPPORT GUIDE CURVE
######################################################################

eSupport_spline = hsf.add_new_spline()

eSupport_spline.add_point(hsf.add_new_point_coord(108, 75 , 100))
eSupport_spline.add_point(hsf.add_new_point_coord(108, 53 , 100))

construction_elements.append_hybrid_shape(eSupport_spline)

#################################################################
#Surface revolution for ENGINE HOUSING
######################################################################
#  Get Z axis direction
# Zdir = hsf.add_new_direction_by_coord(0, 0, 1)
surfRevolution = hsf.add_new_revol(eng_spline, 0, 360, z_dir)
construction_elements.append_hybrid_shape(surfRevolution)

#######################################################################
#####################################################################
# Create a sweep for Engine Support
######################################################################

eSupport = hsf.add_new_sweep_explicit(polyline1, eSupport_spline)
construction_elements.append_hybrid_shape(eSupport)
    
document.part.update()

####################################################################
#################################################################
# PROPELLER BLADE SPLINE: ROOT AND TIP
################################################################
pBlade_spline_r = hsf.add_new_spline()

pBlade_spline_r_points = [
    (108, 30, 134),
    (108.57, 30, 133),
    (108.86, 30, 132),
    (108.836, 30, 131),
    (108.748, 30, 130.46),
    (108.443, 30, 129.68),
    (108, 30, 129),
    (107.442, 30, 129.66),
    (107.21, 30, 130.57),
    (107.125, 30, 131.45),
    (107.238, 30, 132.638),
    (107.543, 30, 133.513),
    (108, 30, 134)  
]

for point in pBlade_spline_r_points:
    pBlade_spline_r.add_point(hsf.add_new_point_coord(*point))

construction_elements.append_hybrid_shape(pBlade_spline_r)

########################################################################################
## MATHEMATIC FORMULALATION FOR TURNING PROPELLER BLADE TIP PROFILE 30 degrees TO Y AXIS
#########################################################################################

# Define cos and sin for 30 degrees
pBlade_spline_t = hsf.add_new_spline()
cos_45 = math.sqrt(2) / 2
sin_45 = 2 / 2

def rotate_y(x, y, z, cx, cz):
    # Translate to the origin
    x_translated = x - cx
    z_translated = z - cz

    # Apply the rotation
    x_rotated = x_translated * cos_45 + z_translated * sin_45
    z_rotated = -x_translated * sin_45 + z_translated * cos_45

    # Translate back to the original position
    x_final = x_rotated + cx
    z_final = z_rotated + cz
    return x_final, y, z_final

# Original points (x, y, z)
points = [
    (108, 50, 135.15),
    (108.270, 50, 134.46),
    (108.350, 50, 133.67),
    (108.302, 50, 132.84),
    (108.250, 50, 132.18),
    (108.180, 50, 131.46),
    (108.160, 50, 130.344),
    (108.869, 50, 129.16),
    (108.564, 50, 128.19),
    (108, 50, 127.279),
    (107.99, 50, 127.79),  
    (107.83, 50, 128.27),
    (107.58, 50, 128.70),
    (107.22, 50, 129.22),
    (106.98, 50, 130.36),
    (107.36, 50, 133.04),
    (107.51, 50, 133.72),
    (108, 50, 135.15)
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
pBlade_section = [pBlade_spline_r,pBlade_spline_t]
pBlade_loft = create_loft("pBlade loft", pBlade_section)
document.part.update()


############################################ WING ###################################################

#####################################################
# WING TIP PROFILE
#####################################################
wtip_spline = hsf.add_new_spline()

wtip_spline_points = [
    (-210, 18 + h, 75),
    (-210, 23 + h, 60),
    (-210, 23.5 + h, 45),
    (-210, 22.5 + h, 31),
    (-210, 20.5 + h, 16),
    (-210, 18 + h, 0),
    (-210, 17.3 + h, 16),
    (-210, 16.8 + h, 31),
    (-210, 16 + h, 45),
    (-210, 15.6 + h, 60),
    (-210, 18 + h, 75)  
]

for point in wtip_spline_points:
    wtip_spline.add_point(hsf.add_new_point_coord(*point))

construction_elements.append_hybrid_shape(wtip_spline)

################################################################
# WINGLET PROFILE
################################################################
winglet_spline = hsf.add_new_spline()
winglet_spline_points = [
    (-250, 31.5 + h + 20, 13.8),
    (-250, 33 + h + 20, 10.8),
    (-250, 33.8 + h + 20, 9.25),
    (-250, 33.98 + h + 20, 6.6),
    (-250, 33.90 + h + 20, 4.56),
    (-250, 33.66 + h + 20, 2.5),
    (-250, 33.4 + h + 20, 0),
    (-250, 32.2 + h + 20, 2.8),
    (-250, 32.17 + h + 20, 4.8),
    (-250, 31.9 + h + 20, 6.5),
    (-250, 31.7 + h + 20, 7.8),
    (-250, 31.6 + h + 20, 10.8),
    (-250, 31.3 + h + 20, 11.8),
    (-250, 31.5 + h + 20, 12.8),
    (-250, 31.5 + h + 20, 13.8)  # Closing the spline by connecting back to the first point
]

for point in winglet_spline_points:
    winglet_spline.add_point(hsf.add_new_point_coord(*point))
construction_elements.append_hybrid_shape(winglet_spline)

################################################################
# WINGLET to WINGTIP CURVE PROFILE
################################################################
winglettip_curve = hsf.add_new_spline()
winglettip_curve_points = [
    (-210, 18 + h, 0),
    (-217.8, 17.70 + h, 0),
    (-224.99, 18.06 + h, 0),
    (-231.46, 20.32 + h, 0),
    (-237.53, 23.49 + h, 0),
    (-241.58, 28.06 + h, 0),
    (-244.84, 31.55 + h, 0),
    (-246.86, 37.312 + h, 0),
    (-248.62, 42.33 + h, 0),
    (-249.68, 47.52 + h, 0),
    (-250, 53.4 + h, 0)  
]

for point in winglettip_curve_points:
    winglettip_curve.add_point(hsf.add_new_point_coord(*point))

construction_elements.append_hybrid_shape(winglettip_curve)

################################################################
## WING ROOT PROFILE
######################################################################

wroot_spline = hsf.add_new_spline()

wroot_spline_points = [
    (90, 67, 177),  # Point A
    (90, 78, 160),  # Point B
    (90, 82, 142),  # Point C
    (90, 84, 120),  # Point D
    (90, 83, 106),  # Point E
    (90, 81, 72),   # Point F
    (90, 77.5, 50), # Point G
    (90, 75, 35),   # Point H
    (90, 68, 0),    # Point I
    (90, 65, 46),   # Point J
    (90, 64, 71),   # Point K
    (90, 63, 106),  # Point L
    (90, 62, 133),  # Point M
    (90, 61, 160),  # Point N
    (90, 67, 177)   # Point O (closing the spline)
]

for point in wroot_spline_points:
    wroot_spline.add_point(hsf.add_new_point_coord(*point))

construction_elements.append_hybrid_shape(wroot_spline)

# WING TO BODY PROFILE
################################################################
bodyw_spline = hsf.add_new_spline()

bodyw_spline_points = [
    (250, 87, 207),
    (250, 98, 190),
    (250, 102, 172),
    (250, 104, 150),
    (250, 103, 136),
    (250, 101, 102),
    (250, 97.5, 80),
    (250, 95, 65),
    (250, 88, 30),
    (250, 85, 76),
    (250, 84, 101),
    (250, 83, 136),
    (250, 82, 163),
    (250, 81, 190),
    (250, 87, 207) 
] 

for point in bodyw_spline_points:
    bodyw_spline.add_point(hsf.add_new_point_coord(*point))

construction_elements.append_hybrid_shape(bodyw_spline)

#####################################################################
#Loft for wing root and wing tip
#########################################################################
wing_section = [wtip_spline,wroot_spline]
wing_surf = create_loft("wing_surf", wing_section)
document.part.update()

###########################################################################
#Loft for winglet and wing tip
############################################################################
wing_let = hsf.add_new_loft()
wing_let.name = "wing_let" 
wing_let.add_section_to_loft(wtip_spline, 1, 1)
wing_let.add_section_to_loft(winglet_spline, 1, 1)
wing_let.add_guide(winglettip_curve)
construction_elements.append_hybrid_shape(wing_let)
############################################################################
# Loft for wingroot and body
######################################################################
wing_body_section = [wroot_spline,bodyw_spline]
wing_b = create_loft("wing_let", wing_body_section )
document.part.update()
#####################################################################


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
p_cockpit1 = add_new_point_coord_and_append_hybrid_shape((299,130, -282), "p8_z")
pCockpit_circle1 = add_new_circle_ctr_rad_with_angles(p_cockpit1, pbodycockpit1_plane, 8, 0, 360, "fuselagecircle1f")

p_cockpit2 = add_new_point_coord_and_append_hybrid_shape((299, 125, -350), "p9_z")
pCockpit_circle2 = add_new_circle_ctr_rad_with_angles(p_cockpit2, pbodycockpit2_plane, 75, 0, 360, "fuselagecircle2f")

p_cockpit3 = add_new_point_coord_and_append_hybrid_shape((299, 95, -420), "p10_z")
pCockpit_circle3 = add_new_circle_ctr_rad_with_angles(p_cockpit3, pbodycockpit3_plane, 45, 0, 360, "fuselagecircle3f")

p_cockpit4 = add_new_point_coord_and_append_hybrid_shape((299, 88, -455), "p11_z")
pCockpit_circle4 = add_new_circle_ctr_rad_with_angles(p_cockpit4, pbodycockpit4_plane, 35, 0, 360, "fuselagecircle4f")

p_tailpit5 = add_new_point_coord_and_append_hybrid_shape((299, 130, 118), "p12_z")
ptailpit_circle5 = add_new_circle_ctr_rad_with_angles(p_tailpit5, pbodytailpit5_plane, 80, 0, 360, "fuselagecircle1r")

p_tailpit6 = add_new_point_coord_and_append_hybrid_shape((299, 135, 210), "p13_z")
ptailpit_circle6 = add_new_circle_ctr_rad_with_angles(p_tailpit6, pbodytailpit6_plane, 75, 0, 360, "fuselagecircle2r")

p_tailpit7 = add_new_point_coord_and_append_hybrid_shape((299, 147, 320), "p14_z")
ptailpit_circle7 = add_new_circle_ctr_rad_with_angles(p_tailpit7, pbodytailpit7_plane, 63, 0, 360, "fuselagecircle3r")

p_tailpit8 = add_new_point_coord_and_append_hybrid_shape((299, 185, 425), "p15_z")
ptailpit_circle8 = add_new_circle_ctr_rad_with_angles(p_tailpit8, pbodytailpit8_plane, 25, 0, 360, "fuselagecircle4r")
document.part.update()


# Create an axis system with default entries (equal to absolute)
axis_sys1 = part.axis_systems.add()
ref_axis =  part.create_reference_from_object(axis_sys1)

# Update the document
document.part.update()
##################### NOSE #####################
# Arguments : (i_center, i_axis, i_radius, i_begin_parallel_angle, i_end_parallel_angle, i_begin_meridian_angle, i_end_meridian_angle)
nose = hsf.add_new_sphere(hsf.add_new_point_coord(299, 88, 455), ref_axis, 35, -90, 90, 0, 360)
nose.limitation = 0 # 0 to specify sphere angles, 1 to fully closed sphere
construction_elements.append_hybrid_shape(nose)
document.part.update()

###################################################################
## LOFT FOR FRONT FUSELAGE
##################################################################
cockpit_section = document.part [pCockpit_circle1, pCockpit_circle2, pCockpit_circle3, pCockpit_circle4,]
cockpit_loft = create_loft("cockpit loft", cockpit_section )
document.part.update()
###################################################################
## LOFT FOR REAR FUSELAGE
##################################################################
tailpit_section = [ptailpit_circle5, ptailpit_circle6, ptailpit_circle7,ptailpit_circle8]
tailpit_loft = create_loft("tail loft", tailpit_section)
document.part.update()
####################################################################
######### TAIL PROFILE ##############################################
# VerTAIL PROFILE
######################################################################
# Create a new spline and name it 'tail_vert_line'
tail_vert_line = hsf.add_new_spline()

tail_vert_line_points = [
    (291.0830774883388, 190, -316.4001661872736),  # Point A
    (293.7009505276944, 190, -305.6206889663975),  # Point B
    (299.5526667333128, 190, -304.6967337760367),  # Point C
    (305.7123680023848, 190, -305.7746814981243),  # Point D
    (312.9500169935444, 190, -321.7899047977116),  # Point E
    (313.4119945887248, 190, -340.4230011366546),  # Point F
    (313.4119945887248, 190, -359.3640825390511),  # Point G
    (311.5640842080032, 190, -378.1511714097209),  # Point H
    (308.638226105194, 190, -393.8584096458546),   # Point I
    (305.8663605341116, 190, -406.9477748426327),  # Point J
    (303.0944949630292, 190, -418.0352371269624),  # Point K
    (299.8606517967664, 190, -427.8907591574777),  # Point L
    (295.7028534401428, 190, -418.1892296586892),  # Point M
    (292.9309878690604, 190, -406.3318047157255),  # Point N
    (288.9271820441636, 190, -392.780461923767),   # Point O
    (287.849234322076, 190, -378.9211340683549),   # Point P
    (286.6172940682616, 190, -359.8260601342315),  # Point Q
    (286.9252791317152, 190, -341.3469563270154),  # Point R
    (288.3112119172564, 190, -327.4876284716033),  # Point S
    (291.0830774883388, 190, -316.4001661872736)   # Point T (closing the spline)
]

for point in tail_vert_line_points:
    tail_vert_line.add_point(hsf.add_new_point_coord(*point))

construction_elements.append_hybrid_shape(tail_vert_line)

tail_vert1_line = hsf.add_new_spline()

points = [
    (299.0830774883388, 330, -416.56006647490943),  # Point A
    (301.9500169935444, 330, -418.71596191908463),  # Point E
    (302.4119945887248, 330, -426.16920045466185),  # Point F
    (303.4119945887248, 330, -433.74563301562046),  # Point G
    (303.5640842080032, 330, -441.26046856388837),  # Point H
    (303.638226105194, 330, -447.5433638583419),    # Point I
    (303.8663605341116, 330, -452.77910993705314),  # Point J
    (302.0944949630292, 330, -457.21409485078493),  # Point K
    (300.0830774883388, 330, -461.1563036629911),   # Point L
    (299.7028534401428, 330, -457.2756918634757),   # Point M
    (298.8309878690604, 330, -452.53272188629023),  # Point N
    (296.9271820441636, 330, -447.1121847695068),   # Point O
    (293.849234322076, 330, -441.56845362734197),   # Point P
    (295.6172940682616, 330, -433.9304240536926),   # Point Q
    (295.9252791317152, 330, -426.5387825308062),   # Point R
    (296.3112119172564, 330, -420.9950513886413),   # Point S
    (299.0830774883388, 330, -416.56006647490943)   # Point T (closing the spline)
]

for x, y, z in points:
    tail_vert1_line.add_point(hsf.add_new_point_coord(x, y, z))

construction_elements.append_hybrid_shape(tail_vert1_line)
document.part.update()

# horTAIL ROOT  PROFILE
######################################################################

hortail_root = hsf.add_new_polyline()
hortail_root.insert_element(hsf.add_new_point_coord (299, 170, -300), 1)
hortail_root.insert_element(hsf.add_new_point_coord( 299, 160, -418), 2)
hortail_root.insert_element(hsf.add_new_point_coord(299, 180, -418), 3)
hortail_root.closure = True
construction_elements.append_hybrid_shape(hortail_root)
document.part.update()
################################################################

# HorTAIL Tip  PROFILE
######################################################################

hortail_tip = hsf.add_new_polyline()
hortail_tip.insert_element(hsf.add_new_point_coord (170, 150, -420), 1)
hortail_tip.insert_element(hsf.add_new_point_coord( 170, 160, -480), 2)
hortail_tip.insert_element(hsf.add_new_point_coord(170, 170, -480), 3)
hortail_tip.closure = True
construction_elements.append_hybrid_shape(hortail_tip)
document.part.update()


###################################################################
## LOFT FOR VERTICAL TAIL
#################################################################
vtail_section = [tail_vert1_line,tail_vert_line]
vtail_loft = create_loft("vertical tail", vtail_section)
document.part.update()
###################################################################
## LOFT FOR HORIZONTAL TAIL
#################################################################
hortail_section = [hortail_tip,hortail_root]
hortail_loft = create_loft("vertical tail",hortail_section)
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
part.in_work_object = partbody
# Create circular pattern around Z axis
angle_per_blade = 360 / int(no_of_blades)
circ_pattern_Z = shpfac.add_new_circ_pattern(blade, 1, int(no_of_blades), 0, angle_per_blade, 1, 1, z_dir, z_dir, True, 0, True)
document.part.update()
######################################################################
## Mirror WING AND ENGINE HOUSING
####################################################################
mirror_1 = shpfac.add_new_mirror(mirror_plane)
document.part.update()
#######################################################################
# HIDING THE SURFACES
####################################################################
selection.clear()
selection.add(construction_elements)
selection.vis_properties.set_show(1) # 0: Show / 1: Hide
selection.clear()
#######################################################################
# Coloring THE SURFACES
####################################################################
color_assignments = {
    hor_tail: (178, 34, 34, 1),  # Red
    vart_tail: (178, 34, 34, 1),  # Red
    body: (178, 34, 34, 1),       # Red
    cockpit: (243, 243, 243, 1),  # Light Gray
    tailpit: (178, 34, 34, 1),    # Red
    blade: (98, 122, 157, 1),     # Blueish Gray
    prop_front_hub: (52, 52, 52, 1),  # Dark Gray
    cnose: (178, 34, 34, 1)       # Red
}

# Apply colors to surfaces
for surface, color in color_assignments.items():
    selection.clear()
    selection.add(surface)
    selection.vis_properties.set_real_color(*color)
######################################################################
## THE END 
######################################################################
