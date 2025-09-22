SUMMARY = "Detección de bolas con OpenCV"
LICENSE = "CLOSED"


SRC_URI = "git://github.com/alfaquillo/Embebidos.git;branch=main;protocol=https"
SRCREV = "${AUTOREV}"
S = "${WORKDIR}/git"

RDEPENDS:${PN} = "python3-opencv python3-numpy"

do_install() {
    install -d ${D}${bindir}
    install -m 0755 ${S}/bola_naranja.py ${D}${bindir}/bola_naranja
}
