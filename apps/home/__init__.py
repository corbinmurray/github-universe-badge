"""
Custom Home Screen - Displays name and GitHub QR code
Simple, battery-efficient display using pre-generated QR code image
"""
from badgeware import screen, io, brushes, shapes, run, Image, PixelFont
import gc

# Configuration
NAME = "Corbin Murray"
GITHUB_USERNAME = "corbinmurray"

# Global resources
qr_image = None
font = None
last_battery_check = 0
battery_level = 100

def init():
    """Initialize the home screen - load resources once"""
    global qr_image, font
    
    # Load the pre-generated QR code
    try:
        qr_image = Image.load("/system/apps/home/assets/github_qr.png")
    except:
        qr_image = None  # Graceful fallback if image not found
    
    # Load a nice font
    try:
        font = PixelFont.load("/system/assets/fonts/nope.ppf")
        screen.font = font
    except:
        pass  # Use default font if not found
    
    # Enable antialiasing for smooth text
    screen.antialias = Image.X2
    
    # Clean up memory
    gc.collect()

def update():
    """Main update loop - called every frame"""
    global last_battery_check, battery_level
    
    # Check battery every 5 seconds (5000ms) to save power
    if io.ticks - last_battery_check > 5000:
        try:
            from badgeware import get_battery_level
            battery_level = get_battery_level()
            last_battery_check = io.ticks
        except:
            pass
    
    # Clear screen with a dark background
    screen.brush = brushes.color(10, 20, 30)
    screen.clear()
    
    # Draw name at the top
    screen.brush = brushes.color(255, 255, 255)
    name_width = screen.measure_text(NAME)
    name_x = (160 - name_width) // 2  # Center horizontally
    screen.text(NAME, name_x, 10)
    
    # Draw GitHub username below name
    screen.brush = brushes.color(100, 150, 255)  # Light blue
    username_text = f"@{GITHUB_USERNAME}"
    username_width = screen.measure_text(username_text)
    username_x = (160 - username_width) // 2
    screen.text(username_text, username_x, 25)
    
    # Draw QR code in the center
    if qr_image:
        # Center the QR code (66x66 image)
        qr_x = (160 - 66) // 2
        qr_y = 45  # Position below the text
        screen.blit(qr_image, qr_x, qr_y)
        
        # Label below QR code
        screen.brush = brushes.color(150, 150, 150)
        label = "Scan for GitHub"
        label_width = screen.measure_text(label)
        label_x = (160 - label_width) // 2
        screen.text(label, label_x, 112)
    else:
        # Fallback if QR code didn't load
        screen.brush = brushes.color(255, 100, 100)
        error_msg = "QR code not found"
        error_width = screen.measure_text(error_msg)
        error_x = (160 - error_width) // 2
        screen.text(error_msg, error_x, 60)
    
    # Optional: Show battery level in corner
    screen.brush = brushes.color(80, 80, 80)
    battery_text = f"{battery_level}%"
    screen.text(battery_text, 125, 2)

def on_exit():
    """Cleanup when exiting the app"""
    pass

# Start the app
run(update)
