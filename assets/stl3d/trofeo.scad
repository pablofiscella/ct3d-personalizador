// Trofeo temático — prueba de concepto CT3D
// Base + copa torneada (rotate_extrude) + personaje en relieve en el cuerpo + placa
// de texto en la base. TEXTO_SIZE se pre-calcula en Python (texto_ajustado.py) para
// que entre en la placa sin salirse.
// Parámetros por CLI con -D, ej:
//   openscad trofeo.scad -o out.stl -D 'TEXTO="MAXI - 8 AÑOS"' -D 'TEXTO_SIZE=4.5' -D 'ALTURA=120'

$fn = 96;

// ── Dimensiones generales ──────────────────────────────────────────────
ALTURA        = 100;   // altura total del trofeo (mm), base incluida
BASE_D        = 46;    // diámetro de la base
BASE_H        = 12;    // alto de la base (donde va la placa)
COPA_D_ABAJO  = 26;    // diámetro de la copa donde nace del pie
COPA_D_ARRIBA = 46;    // diámetro de la copa en la boca
PIE_D         = 10;    // diámetro del pie que conecta base con copa

// ── Personaje en relieve sobre el cuerpo de la copa ────────────────────
INCLUIR_PERSONAJE = true;
FIG_H     = 26;     // alto del personaje (mm)
RELIEVE   = 1.4;    // saliente del relieve (personaje y texto)

// ── Texto en la placa de la base ───────────────────────────────────────
TEXTO      = "CAMPEON 2026";
TEXTO_SIZE = 5;      // pre-calculado en Python para entrar en BASE_D

include <silueta_mod.scad>

module silueta2d() {
    resize([0, FIG_H], auto=true) silueta();
}

// Perfil de la copa: pie angosto -> "panza" vertical (donde va el relieve) -> se
// abre hacia la boca con labio. La panza vertical evita que el relieve quede muy
// deformado por la curvatura.
function copa_perfil() = [
    [0, 0],
    [PIE_D/2, 0],
    [PIE_D/2, ALTURA*0.22],
    [COPA_D_ABAJO/2, ALTURA*0.34],
    [COPA_D_ABAJO/2, ALTURA*0.60],          // panza vertical (acá va el personaje)
    [COPA_D_ARRIBA/2, ALTURA*0.85],
    [COPA_D_ARRIBA/2 + 2.5, ALTURA*0.90],   // labio
    [COPA_D_ARRIBA/2 - 3, ALTURA*0.94],
    [COPA_D_ARRIBA/2 - 3, ALTURA - BASE_H],
    [0, ALTURA - BASE_H],
];

// ── Base (cilindro con bisel) ───────────────────────────────────────────
module base() {
    cylinder(d1=BASE_D, d2=BASE_D - 6, h=BASE_H);
}

// ── Copa torneada ────────────────────────────────────────────────────────
module copa() {
    translate([0, 0, BASE_H])
        rotate_extrude()
            polygon(points=copa_perfil());
}

base();
copa();

// Personaje en relieve, en la panza vertical de la copa (mirando hacia -Y)
if (INCLUIR_PERSONAJE)
    color("goldenrod")
        translate([0, -(COPA_D_ABAJO/2 - 0.5), BASE_H + ALTURA*0.47])
            rotate([90, 0, 0])
                linear_extrude(RELIEVE)
                    silueta2d();

// Texto grabado en la base
color("goldenrod")
    translate([0, -(BASE_D/2 - 1), BASE_H/2])
        rotate([90, 0, 0])
            linear_extrude(RELIEVE)
                text(TEXTO, size=TEXTO_SIZE, font="DejaVu Sans:style=Bold",
                     halign="center", valign="center");
