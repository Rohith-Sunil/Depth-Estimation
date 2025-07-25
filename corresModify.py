import cv2
import numpy as np

def ssd_correspondence(img1, img2):
    """Improved disparity calculation"""
    
    # Ensure grayscale
    if len(img1.shape) > 2:
        img1 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
    if len(img2.shape) > 2:
        img2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)
    
    # Create StereoBM matcher with better parameters
    stereo = cv2.StereoBM_create(numDisparities=96, blockSize=15)
    stereo.setMinDisparity(0)
    stereo.setSpeckleWindowSize(100)
    stereo.setSpeckleRange(32)
    stereo.setDisp12MaxDiff(1)
    
    # Compute disparity
    disparity = stereo.compute(img1, img2).astype(np.float32)
    
    # StereoBM returns disparities * 16, so divide by 16
    disparity = disparity / 16.0
    
    # Handle invalid disparities
    disparity[disparity <= 0] = 0.1
    
    # Store unscaled for depth computation
    disparity_unscaled = disparity.copy()
    
    # Normalize for display
    disparity_scaled = cv2.normalize(disparity, None, 0, 255, cv2.NORM_MINMAX)
    disparity_scaled = np.uint8(disparity_scaled)

    # Store unscaled before handling invalids for display use if needed
    # disparity_unscaled = disparity.copy()

    # # Create a mask for valid disparities
    # valid_mask = disparity > 0

    # # Optional: set invalid disparities to NaN or a large value
    # disparity_for_depth = disparity.copy()
    # disparity_for_depth[~valid_mask] = np.nan  # or 0.1 if you prefer

    # # Normalize only valid disparities for display
    # normalized = np.zeros_like(disparity)
    # normalized[valid_mask] = cv2.normalize(disparity[valid_mask], None, 0, 255, cv2.NORM_MINMAX)
    # disparity_scaled = np.uint8(normalized)

    
    return disparity_unscaled, disparity_scaled