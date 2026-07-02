// Cortante de galletitas temático — prueba de concepto CT3D
// Pared fina que sigue el contorno del personaje (offset hacia adentro con offset()),
// más un aro/asa arriba para empujar con el dedo. Sin texto — es el mismo cortante
// para cualquier nombre, solo cambia por temática.
// Parámetros por CLI con -D, ej:
//   openscad cortante.scad -o out.stl -D 'ANCHO_OBJETIVO=90' -D 'ALTO_PARED=22'

$fn = 64;

ANCHO_OBJETIVO = 80;   // ancho final del cortante (mm) — la silueta se escala a esto
ALTO_PARED     = 20;   // alto de la pared de corte (mm)
GROSOR_PARED   = 1.4;  // espesor de la pared (mm) — fino para cortar, pero imprimible
INCLUIR_ASA    = true; // barra superior para empujar con el dedo
ASA_ANCHO      = 6;    // ancho de la barra del asa
ASA_ALTO       = 3;    // espesor de la barra del asa

include <silueta_mod.scad>

module silueta2d() {
    resize([ANCHO_OBJETIVO, 0], auto=true) silueta();
}

// Pared: silueta menos la misma silueta encogida GROSOR_PARED hacia adentro
module pared() {
    difference() {
        silueta2d();
        offset(delta=-GROSOR_PARED) silueta2d();
    }
}

linear_extrude(ALTO_PARED) pared();

// Asa: una barra recta que cruza por el medio, a la altura de la pared, unida
// a los dos lados del contorno para poder empujar sin que se deforme la silueta.
if (INCLUIR_ASA) {
    // Extensión bien larga para garantizar que cruce cualquier silueta; el
    // intersection() con la silueta original la recorta a lo que realmente hace falta.
    translate([0, 0, ALTO_PARED - ASA_ALTO])
        intersection() {
            linear_extrude(ASA_ALTO)
                translate([0, 0]) square([ANCHO_OBJETIVO * 1.5, ASA_ANCHO], center=true);
            linear_extrude(ASA_ALTO) offset(delta=1) silueta2d();
        }
}
