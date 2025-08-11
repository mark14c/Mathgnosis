import reflex as rx

# Theme colors
PRIMARY_COLOR = "#F0F8FF"  # AliceBlue, a light blue
SECONDARY_COLOR = "#FFFFFF"  # White
TEXT_COLOR = "#000000"  # Black

# Base styles
base_style = {
    "font_family": "sans-serif",
    "color": TEXT_COLOR,
    "background_color": PRIMARY_COLOR,
}

# App icon style
app_icon_style = {
    "border_radius": "25px",
    "border": "3px solid",
    "border_image": "linear-gradient(45deg, #00BFFF, #1E90FF, #0000FF) 1",
    "box_shadow": "0 4px 8px 0 rgba(0,0,0,0.2)",
    "width": "50px",
    "height": "50px",
    "margin_bottom": "1.5em",
}

# Card styles
card_style = {
    "background_color": SECONDARY_COLOR,
    "border_radius": "10px",
    "box_shadow": "0 4px 8px 0 rgba(0,0,0,0.2)",
    "padding": "1em",
    "margin": "1em",
}
# Button styles
button_style = {
    "background_color": "#4CAF50",  # Green
    "color": "#FFFFFF",  # White
    "border": "none",
    "border_radius": "5px",
    "padding": "0.5em 1em",
    "cursor": "pointer",
}

# Input styles
input_style = {
    "border": "1px solid #ccc",
    "border_radius": "4px",
    "padding": "0.5em",
    "font_size": "1em",
}

# Textarea styles
textarea_style = {
    "border": "1px solid #ccc",
    "border_radius": "4px",
    "padding": "0.5em",
    "font_size": "1em",
}

# Link styles
link_style = {
    "color": "#4CAF50",  # Green
    "text_decoration": "none",
}

# Hover styles
hover_style = {
    "background_color": "#45a049",  # Darker green
    "color": "#FFFFFF",  # White
}

# Active styles
active_style = {
    "background_color": "#3e8e41",  # Even darker green
    "color": "#FFFFFF",  # White
}

# Inactive styles
inactive_style = {
    "background_color": "#f0f0f0",  # Light gray
    "color": "#aaaaaa",  # Dark gray
}

# Focus styles
focus_style = {
    "border": "2px solid #4CAF50",  # Green
    "outline": "none",
}

# Placeholder styles
placeholder_style = {
    "color": "#aaaaaa",  # Dark gray
}

# Global styles
global_style = {
    "font_family": "sans-serif",
    "color": TEXT_COLOR,
    "background_color": PRIMARY_COLOR,
}

# Responsive styles
responsive_style = {
    "max_width": "1200px",
    "margin": "0 auto",
    "padding": "0 1em",
}

# Utility styles
utility_style = {
    "clearfix": {
        "content": '""',
        "display": "table",
        "clear": "both",
    },
}

# Animation styles
animation_style = {
    "transition": "all 0.3s ease",
}

