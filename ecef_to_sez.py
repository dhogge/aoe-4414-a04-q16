# ecef_to_sez.py
#
# Usage: python3 ecef_to_sez.py o_x_km o_y_km o_z_km x_km y_km z_km
# Parameters:
# o_x_km, o_y_km, o_z_km: ECEF coordinates of the SEZ origin
# x_km, y_km, z_km: ECEF coordinates of the position to be converted
# Output:
# SEZ s_km, e_km, z_km coordinates
#
# Written by Dylan Hogge
# Other contributors: None
#
# Optional license statement, e.g., See the LICENSE file for the license.

import sys # argv
import math # math module

# "constants"
R_E_KM = 6378.1363
E_E = 0.081819221456

# helper functions

## calculated denominator
def calc_denom(ecc, lat_rad):
  return math.sqrt(1.0-(ecc**2)*(math.sin(lat_rad)**2))

# Initialize script arguments
if len(sys.argv) == 7:
    r_x_km = float(sys.argv[1])
    r_y_km = float(sys.argv[2])
    r_z_km = float(sys.argv[3])
    x_km = float(sys.argv[4])
    y_km = float(sys.argv[5])
    z_km = float(sys.argv[6])
else:
  print(\
  'Usage: '\
  'python3 ecef_to_sez.py o_x_km o_y_km o_z_km x_km y_km z_km'\
  )
  exit()

# write script below this line
#iteratively find latitude/longitude
lon_rad = math.atan2(r_y_km,r_x_km)
lon_deg = lon_rad*180.0/math.pi
# initialize lat_rad, r_lon_km, r_z_km
lat_rad = math.asin(r_z_km/math.sqrt(r_x_km**2+r_y_km**2+r_z_km**2))
r_lon_km = math.sqrt(r_x_km**2+r_y_km**2)
prev_lat_rad = float('nan')
# iteratively find latitude
c_E = float('nan')
count = 0
while (math.isnan(prev_lat_rad) or abs(lat_rad-prev_lat_rad)>10e-7) and count<5:
    denom = calc_denom(E_E,lat_rad)
    c_E = R_E_KM/denom
    prev_lat_rad = lat_rad
    lat_rad = math.atan((r_z_km+c_E*(E_E**2)*math.sin(lat_rad))/r_lon_km)
count = count+1

dx = x_km - r_x_km
dy = y_km - r_y_km
dz = z_km - r_z_km

# Rotate ECEF coordinates to SEZ frame
s_km = math.sin(lat_rad) * math.cos(lon_rad) * dx + math.sin(lat_rad) * math.sin(lon_rad) * dy - math.cos(lat_rad) * dz
e_km = -math.sin(lon_rad) * dx + math.cos(lon_rad) * dy
z_km = math.cos(lat_rad) * math.cos(lon_rad) * dx + math.cos(lat_rad) * math.sin(lon_rad) * dy + math.sin(lat_rad) * dz

print(round(s_km, 4))
print(round(e_km, 4))
print(round(z_km, 4))

