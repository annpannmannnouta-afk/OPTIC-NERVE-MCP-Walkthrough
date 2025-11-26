import time
from server import AdaptiveRetina

def test_retina():
    print("Initializing Retina...")
    retina = AdaptiveRetina(camera_index=0)
    
    print("Starting Retina (Interval: 1.0s)...")
    retina.set_interval(1.0)
    retina.start()
    
    # Wait for warm-up (increased to 5s)
    print("Waiting for camera warm-up (5s)...")
    time.sleep(5)
    
    # Try reading multiple times
    for i in range(3):
        print(f"Reading Eye (Attempt {i+1})...")
        vision = retina.get_vision()
        status = vision.get('status')
        print(f"Status: {status}")
        
        if status == "SIGHT":
            print(f"Image captured! Length: {len(vision['image_base64'])} chars")
            break
        else:
            print(f"Message: {vision.get('message')}")
            print(f"Error: {vision.get('error')}")
            time.sleep(1)

    print("Stopping Retina...")
    retina.stop()
    print("Test Complete.")

if __name__ == "__main__":
    test_retina()
