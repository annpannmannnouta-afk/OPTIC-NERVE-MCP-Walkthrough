import cv2
import time
import threading
import base64
import logging
import numpy as np
from typing import Optional, Dict, Any
from mcp.server.fastmcp import FastMCP

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger("OpticNerve")

class AdaptiveRetina:
    """
    Biological-grade vision sensor manager.
    Implements Zero-Stack Architecture with Latest Frame Drop strategy.
    """
    def __init__(self, camera_index: int = 0):
        self.camera_index = camera_index
        self.interval_seconds = 5.0  # Default: 5 seconds (Low metabolism)
        self.current_buffer: Optional[bytes] = None
        self.last_capture_time = 0.0
        self.running = False
        self.lock = threading.Lock()
        self.thread: Optional[threading.Thread] = None
        self._camera_error = False

    def start(self):
        """Opens the eye."""
        if self.running:
            return
        self.running = True
        self.thread = threading.Thread(target=self._visual_cortex_loop, daemon=True)
        self.thread.start()
        logger.info("Optic Nerve activated.")

    def stop(self):
        """Closes the eye."""
        self.running = False
        if self.thread:
            self.thread.join()
        logger.info("Optic Nerve deactivated.")

    def set_interval(self, interval: float):
        """Adjusts the heartbeat of the retina."""
        self.interval_seconds = max(0.0, interval)
        logger.info(f"Retina interval adjusted to {self.interval_seconds}s")

    def _visual_cortex_loop(self):
        """
        The main loop. Captures reality.
        Patiently waits if the interval is long.
        """
        cap = None
        
        while self.running:
            try:
                # Open camera if not open
                if cap is None or not cap.isOpened():
                    cap = cv2.VideoCapture(self.camera_index)
                    if not cap.isOpened():
                        logger.error("Retina failed to open. Retrying in 5s...")
                        self._camera_error = True
                        time.sleep(5)
                        continue
                    self._camera_error = False
                    logger.info("Retina connected.")

                # Check if it's time to capture
                now = time.time()
                if now - self.last_capture_time >= self.interval_seconds:
                    ret, frame = cap.read()
                    if ret:
                        # Encode to JPEG immediately to save memory
                        _, buffer = cv2.imencode('.jpg', frame)
                        jpg_as_text = base64.b64encode(buffer).decode('utf-8')
                        
                        # Zero-Stack: Overwrite the single buffer slot
                        with self.lock:
                            self.current_buffer = jpg_as_text
                        
                        self.last_capture_time = now
                    else:
                        logger.warning("Retina captured void (empty frame).")
                        self._camera_error = True
                        cap.release()
                        cap = None
                
                # Sleep briefly to prevent CPU burn, but stay responsive
                # If interval is 0 (max speed), sleep minimal amount
                sleep_time = min(0.1, self.interval_seconds) if self.interval_seconds > 0 else 0.001
                time.sleep(sleep_time)

            except Exception as e:
                logger.error(f"Visual Cortex Glitch: {e}")
                time.sleep(1)

        if cap:
            cap.release()

    def get_vision(self) -> Dict[str, Any]:
        """
        Retrieves the latest visual memory.
        """
        with self.lock:
            if self._camera_error:
                return {
                    "status": "BLIND",
                    "error": "Camera disconnected or inaccessible.",
                    "timestamp": time.time()
                }
            if self.current_buffer is None:
                return {
                    "status": "DARKNESS",
                    "message": "No photons captured yet. Initializing...",
                    "timestamp": time.time()
                }
            return {
                "status": "SIGHT",
                "image_base64": self.current_buffer,
                "interval_setting": self.interval_seconds,
                "timestamp": self.last_capture_time
            }

# Initialize the Retina
retina = AdaptiveRetina()
retina.start()

# Initialize MCP Server
mcp = FastMCP("OpticNerve")

@mcp.tool()
def read_eye() -> str:
    """
    Captures the current visual field from the Optic Nerve.
    Returns a JSON string containing the base64 encoded image and metadata.
    """
    vision = retina.get_vision()
    return str(vision)

@mcp.tool()
def configure_eye(interval_seconds: float) -> str:
    """
    Adjusts the capture interval of the Optic Nerve.
    Args:
        interval_seconds: Time in seconds between frames. 
                          0.0 = Max Speed (60+ FPS), 
                          300.0 = 5 minutes, etc.
    """
    retina.set_interval(interval_seconds)
    return f"Optic Nerve adjusted to {interval_seconds}s heartbeat."

if __name__ == "__main__":
    # Run the server
    mcp.run()
