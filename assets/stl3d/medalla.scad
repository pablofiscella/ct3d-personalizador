// Medalla temática — prueba de concepto CT3D
// Disco + aro colgante + personaje en relieve + texto (tamaño pre-calculado en Python
// para entrar en el disco sin salirse — ver generar.py / texto_ajustado.py)
// Parámetros por CLI con -D, ej:
//   openscad medalla.scad -o out.stl -D 'TEXTO="MAXIMILIANO"' -D 'TEXTO_SIZE=4.1' -D 'RELIEVE=2.2'

$fn = 96;

D = 60;            // diámetro medalla (mm)
H = 3;              // espesor base
RELIEVE = 1.6;      // altura del relieve del personaje y el texto (mm) — más alto = más marcado al tacto
BORDE = 2.5;        // ancho del aro perimetral
TEXTO = "CAMPEON";  // texto abajo
TEXTO_SIZE = 7;     // tamaño de fuente — calculalo con texto_ajustado.py para que no se salga
TEXTO_Y = -18;      // posición vertical del texto (centro del disco = 0)
FIG_H = 34;         // alto del personaje en mm

include <silueta_mod.scad>

module silueta2d() {
    resize([0, FIG_H], auto=true) silueta();
}

// base
cylinder(d=D, h=H);

// aro perimetral en relieve
translate([0, 0, H])
    difference() {
        cylinder(d=D, h=1.2);
        translate([0, 0, -0.1]) cylinder(d=D - BORDE*2, h=1.5);
    }

// personaje en relieve (centrado, un poco arriba)
color("goldenrod") translate([0, 4, H])
    linear_extrude(RELIEVE)
        silueta2d();

// texto abajo
color("goldenrod") translate([0, TEXTO_Y, H])
    linear_extrude(RELIEVE)
        text(TEXTO, size=TEXTO_SIZE, font="DejaVu Sans:style=Bold",
             halign="center", valign="center");

// oreja para la cinta
translate([0, D/2 + 3.5, 0])
    difference() {
        cylinder(d=12, h=H);
        translate([0, 0, -0.1]) cylinder(d=6, h=H+0.2);
    }
