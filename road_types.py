# road_types.py
# This module defines different types of roads with their respective attributes.

# Nested Dictionary
# Define common road types with structured data
#
#       Note: measurements are in metric, avg American lane width is 12 ft ≈ 3.66 m
#       Unit: meter

ROAD_TYPES = {
    "Two-Lane Road"         : {
        "left_lane_count"   : 1,    "right_lane_count"  : 1,
        "lane_width"        : 3.66, "shoulder_width"    : 1.22,
        "median_width"      : 0.0,  "median_color"      : "none",
        "median_line_color" : "yellow", "line_width"    : 0.15, "speed_limit" : 56.33
    },

    "Four-Lane Road"        : {
        "left_lane_count"   : 2,    "right_lane_count"  : 2,
        "lane_width"        : 3.66, "shoulder_width"    : 1.83,
        "median_width"      : 0.61,  "median_color"     : "grass",
        "median_line_color" : "yellow", "line_width"    : 0.15, "speed_limit" : 72.42
    },

    "Six-Lane Road"         : {
        "left_lane_count"   : 3,    "right_lane_count"  : 3,
        "lane_width"        : 3.66, "shoulder_width"    : 2.44,
        "median_width"      : 1.22,  "median_color"     : "grass",
        "median_line_color" : "yellow", "line_width"    : 0.15, "speed_limit" : 88.51
    },

    "Two-Lane One-Way Road" : {
        "left_lane_count"   : 2,    "right_lane_count"  : 0,
        "lane_width"        : 3.66, "shoulder_width"    : 1.22,
        "median_width"      : 0.0,  "median_color"      : "none",
        "median_line_color" : "white", "line_width"    : 0.15, "speed_limit" : 56.33
    },

    "Four-Lane One-Way Road": {
        "left_lane_count"   : 4,    "right_lane_count"  : 0,
        "lane_width"        : 3.66, "shoulder_width"    : 1.83,
        "median_width"      : 0.0,  "median_color"      : "none",
        "median_line_color" : "white", "line_width"    : 0.15, "speed_limit" : 72.42
    },

    "Six-Lane One-Way Road" : {
        "left_lane_count"   : 6,    "right_lane_count"  : 0,
        "lane_width"        : 3.66, "shoulder_width"    : 2.44,
        "median_width"      : 0.0,  "median_color"      : "none",
        "median_line_color" : "white", "line_width"    : 0.15, "speed_limit" : 88.51
    },

    "One-Way Road"          : {
        "left_lane_count"   : 1,    "right_lane_count"  : 0,
        "lane_width"        : 3.66, "shoulder_width"    : 1.22,
        "median_width"      : 0.0,  "median_color"      : "none",
        "median_line_color" : "white", "line_width"    : 0.15, "speed_limit" : 48.28
    },
}
