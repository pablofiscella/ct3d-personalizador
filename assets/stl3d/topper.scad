// Topper de torta temático — prueba de concepto CT3D
// Personaje + placa con nombre y edad + palito. Se imprime plano.
// PLACA_W y TEXTO_SIZE se pre-calculan en Python (ver generar.py / texto_ajustado.py)
// para que el texto entre en la placa sin salirse, sea cual sea el nombre.
// Parámetros por CLI con -D, ej:
//   openscad topper.scad -o out.stl -D 'TEXTO="MAXIMILIANO 8"' -D 'PLACA_W=95' -D 'TEXTO_SIZE=6.2'

$fn = 64;

GROSOR = 3;         // espesor de toda la pieza
RELIEVE = 1.2;      // altura del relieve del nombre/edad (mm)
FIG_H = 70;         // alto del personaje
TEXTO = "VALENTINA 5";
TEXTO_SIZE = 8;     // calculado en Python para entrar en PLACA_W
PLACA_W = 78;       // calculado en Python según el largo del texto
PLACA_H = 16;

include <silueta_mod.scad>

module silueta2d() {
    resize([0, FIG_H], auto=true) silueta();
}

module placa2d() {
    hull() {
        for (x = [-1, 1], y = [-1, 1])
            translate([x*(PLACA_W/2 - 4), y*(PLACA_H/2 - 4)])
                circle(r=4);
    }
}

linear_extrude(GROSOR) {
    // personaje arriba
    translate([0, PLACA_H/2 + FIG_H/2 - 4]) silueta2d();

    // placa del nombre (unida al personaje)
    placa2d();

    // palito para clavar (punta en ángulo)
    translate([0, -PLACA_H/2 - 40]) {
        square([8, 82], center=true);
        translate([0, -41]) polygon([[-4, 0], [4, 0], [0, -10]]);
    }
}

// nombre y edad en relieve sobre la placa
color("goldenrod") translate([0, 0, GROSOR])
    linear_extrude(RELIEVE)
        text(TEXTO, size=TEXTO_SIZE, font="DejaVu Sans:style=Bold",
             halign="center", valign="center");
