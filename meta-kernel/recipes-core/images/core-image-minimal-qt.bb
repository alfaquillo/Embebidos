require recipes-core/images/core-image-minimal.bb

DESCRIPTION = "Minimal image extendida con Qt y PyQt5 para GUI"
LICENSE = "MIT"

IMAGE_FEATURES += "x11-base x11-sato"

IMAGE_INSTALL:append = " \
    qtbase \
    qtbase-plugins \
    qtdeclarative \
    qtmultimedia \
    python3-pyqt5 \
    v4l-utils \
    kernel-modules \
    linux-firmware \
"
