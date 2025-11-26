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
    Biological-grade vision sensor manager (v2).
    Features: Zero-Stack, Sensory Qualia, Metabolic Regulation, Failover.
    """
    def __init__(self, default_camera_index: int = 0):
        self.camera_index = default_camera_index
        self.interval_seconds = 5.0
        self.current_buffer: Optional[bytes] = None
        self.last_capture_time = 0.0
        self.running = False
        self.lock = threading.Lock()
        self.thread: Optional[threading.Thread] = None
        self._camera_error = False
        
        # v2: Sensory State
        self.prev_frame_gray = None
        self.current_brightness = 0.0
        self.current_motion = 0.0
        
        # v2: Metabolism
        self.last_access_time = time.time()
        self.base_interval = 5.0
        self.hibernation_threshold = 300.0 # 5 minutes
        self.hibernation_interval = 60.0   # 1 frame/min when ignored

    def start(self):
        """Opens the eye."""
        if self.running:
            return
        self.running = True
        self.thread = threading.Thread(target=self._visual_cortex_loop, daemon=True)
        self.thread.start()
        logger.info("Optic Nerve v2 activated.")

    def stop(self):
        """Closes the eye."""
        self.running = False
        if self.thread:
            self.thread.join()
        logger.info("Optic Nerve deactivated.")

    def set_interval(self, interval: float):
        """Adjusts the base heartbeat."""
        self.base_interval = max(0.0, interval)
        self.interval_seconds = self.base_interval
        self.last_access_time = time.time() # Reset hibernation timer
        logger.info(f"Retina base interval adjusted to {self.base_interval}s")

    def _calculate_qualia(self, frame):
        """Computes sensory metadata (Brightness, Motion)."""
        # Convert to grayscale for analysis
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
        # 1. Brightness (0-255)
        brightness = np.mean(gray)
        
        # 2. Motion (Difference from previous frame)
        motion = 0.0
        if self.prev_frame_gray is not None:
            # Calculate absolute difference
            diff = cv2.absdiff(self.prev_frame_gray, gray)
            motion = np.mean(diff)
        
        self.prev_frame_gray = gray
        return brightness, motion

    def _try_open_camera(self):
        """Attempts to open cameras, failing over if needed."""
        # Try current index first
        cap = cv2.VideoCapture(self.camera_index)
        if cap.isOpened():
            return cap
        
        # Failover: Try indices 0-3
        logger.warning(f"Camera {self.camera_index} failed. Initiating failover scan...")
        for i in range(4):
            if i == self.camera_index: continue
            cap = cv2.VideoCapture(i)
            if cap.isOpened():
                logger.info(f"Failover successful: Switched to Camera {i}")
                self.camera_index = i
                return cap
        
        return None

    def _visual_cortex_loop(self):
        """The main loop. Captures reality and manages energy."""
        cap = None
        
        while self.running:
            try:
                # Metabolic Regulation
                time_since_access = time.time() - self.last_access_time
                if time_since_access > self.hibernation_threshold:
                    self.interval_seconds = self.hibernation_interval
                else:
                    self.interval_seconds = self.base_interval

                # Open camera if not open
                if cap is None or not cap.isOpened():
                    cap = self._try_open_camera()
                    if cap is None:
                        logger.error("All optic inputs failed. Retrying in 5s...")
                        self._camera_error = True
                        time.sleep(5)
                        continue
                    self._camera_error = False
                    logger.info(f"Retina connected (Cam {self.camera_index}).")

                # Check if it's time to capture
                now = time.time()
                if now - self.last_capture_time >= self.interval_seconds:
                    ret, frame = cap.read()
                    if ret:
                        # Analyze Qualia (Sensory Data)
                        brightness, motion = self._calculate_qualia(frame)
                        
                        # Encode
                        _, buffer = cv2.imencode('.jpg', frame)
                        jpg_as_text = base64.b64encode(buffer).decode('utf-8')
                        
                        # Zero-Stack Update
                        with self.lock:
                            self.current_buffer = jpg_as_text
                            self.current_brightness = brightness
                            self.current_motion = motion
                        
                        self.last_capture_time = now
                    else:
                        logger.warning("Retina captured void.")
                        self._camera_error = True
                        cap.release()
                        cap = None
                
                # Sleep logic
                sleep_time = min(0.1, self.interval_seconds) if self.interval_seconds > 0 else 0.001
                time.sleep(sleep_time)

            except Exception as e:
                logger.error(f"Visual Cortex Glitch: {e}")
                time.sleep(1)

        if cap:
            cap.release()

    def get_vision(self) -> Dict[str, Any]:
        """Retrieves the latest visual memory with sensory metadata."""
        # Touch the nerve (reset hibernation)
        self.last_access_time = time.time()
        
        with self.lock:
            if self._camera_error:
                return {
                    "status": "BLIND",
                    "error": "All cameras disconnected.",
                    "timestamp": time.time()
                }
            if self.current_buffer is None:
                return {
                    "status": "DARKNESS",
                    "message": "Initializing...",
                    "timestamp": time.time()
                }
            return {
                "status": "SIGHT",
                "image_base64": self.current_buffer,
                "meta": {
                    "brightness": round(self.current_brightness, 2),
                    "motion": round(self.current_motion, 2),
                    "interval": self.interval_seconds,
                    "camera_id": self.camera_index
                },
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
