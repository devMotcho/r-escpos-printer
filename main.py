import sys
import time
import pystray
import threading
from PIL import Image, ImageDraw
from app.settings import BASE_URL, CHECK_SERVER_HEALTH

from controllers.script import ScriptController

def on_exit(icon, item):
    """Handle application shutdown procedure"""
    controller.stop_script()  # Stop automation script
    icon.stop()  # Remove tray icon
    return

def on_restart(icon, item):
    """Restart the automation script"""
    controller.stop_script()
    controller.start_script()  # Full script restart

def on_status(icon, item):
    """Show current status in notification balloon"""
    status = "ON" if controller.running else "OFF"
    icon.notify(f"{status}\nMensagem: {controller.status_message}")

def create_image(color):
    """Generate tray icon image with colored square
    Args:
        color (str): Color name or hex value for the icon
    Returns:
        Image: 64x64 RGB image with centered colored square
    """
    image = Image.new('RGB', (64, 64), 'white')  # Create white background
    dc = ImageDraw.Draw(image)
    dc.rectangle((16, 16, 48, 48), fill=color)  # Draw centered square
    return image

def update_icon(icon):
    """Continuous icon color update based on script state
    Runs in dedicated thread for real-time updates"""
    while True:
        # Determine color based on script state
        color = 'green' if controller.running else 'red'
        icon.icon = create_image(color)
        time.sleep(1)  # Update interval

def stop_alert(icon):
    controller.stop_alert_sound()

def setup_icon(icon):
    """Initialize tray icon visibility and start update thread"""
    icon.visible = True
    # Start daemon thread for icon updates (auto-kill on main exit)
    threading.Thread(target=update_icon, args=(icon,), daemon=True).start()

if __name__ == "__main__":

    print(BASE_URL, CHECK_SERVER_HEALTH)
    controller = ScriptController()

    # Configure system tray icon
    icon = pystray.Icon(
        name="my_script",
        title="Rodizio Impressora",  # Hover text
        icon=create_image('gray'),  # Initial neutral state
        menu=pystray.Menu(
            pystray.MenuItem("Mostrar Status", on_status),
            pystray.MenuItem("Reiniciar Impressão", on_restart),
            pystray.MenuItem("Parar Alerta", stop_alert),
            pystray.MenuItem("Sair", on_exit)
        )
    )

    # Start automation script and tray interface
    controller.start_script()
    icon.run(setup=setup_icon)  # Start tray icon with setup callback