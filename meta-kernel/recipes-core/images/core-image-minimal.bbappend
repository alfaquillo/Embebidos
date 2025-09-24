IMAGE_FEATURES += "x11-base"

IMAGE_INSTALL:append = " \
    ball-detect \
    python3-opencv \
    python3-numpy v4l-utils gstreamer1.0 gstreamer1.0-plugins-base gstreamer1.0-plugins-good\
    "  
