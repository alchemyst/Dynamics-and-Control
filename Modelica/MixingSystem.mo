model MixingSystem

// Flow rates, mass / time
Real A, B, C, D, E, F, G, H, I, J, K, L;
// Mass fraction X in each stream
Real xA, xB, xC, xD, xE, xF, xG, xH, xI, xJ, xK, xL;
// For each tank:
Real M1, M2, M3; // Mass
Real x1, x2, x3; // Mass fraction x
Real h1, h2, h3; // Height
Real V1, V2, V3; // Volume
parameter Real A1=3, A2=3, A3=3; // Cross-sectional area

parameter Real rhox=1000, rhoy=800; // Density of x and Y

// Setting fixed=false causes these values to be calculated at initialisation
// Discharge coefficients
parameter Real k1(fixed=false), k2(fixed=false);
// Flowrates of the flows with valves
parameter Real Gstart(fixed=false), Hstart(fixed=false), Jstart(fixed=false), Lstart(fixed=false);

initial equation

h1 = 1;
h2 = 1;
h3 = 1;

H = G;
H = 2*J;
J = 2*L;

der(M1) = 0;
der(M2) = 0;
der(M3) = 0;

der(x1*M1) = 0;
der(x2*M2) = 0;
der(x3*M3) = 0;

equation

// Flowrates in
A = (if time <= 0 then 1 * rhox else 1.5 * rhox);
B = 1 * rhoy;
C = 1 * rhoy;

// Fractions in
xA = 1;
xB = 0;
xC = 0;

// Flowrates with valves
// Right now fixed at starting point, but could be changed here
G = Gstart; // For instance try this: G = A + B + C
H = Hstart;
J = Jstart;
L = Lstart;

// MB over tanks
der(M1) = A + L - D "MB Tank 1";
der(M2) = B + D + K - E "MB Tank 2";
der(M3) = C + E + I - F "MB Tank 3";

// X balance over tanks
der(x1*M1) = xA*A + xL*L - xD*D "CB Tank 1";
der(x2*M2) = xB*B + xD*D + xK*K - xE*E "CB Tank 2";
der(x3*M3) = xC*C + xE*E + xI*I - xF*F "CB Tank 3";

//Junctions
F = H + G;
H = I + J;
J = K + L;

// Fractions are the same for all the junctions
xF = xG;
xF = xH;
xF = xI;
xF = xJ;
xF = xK;
xF = xL;

// Fractions coming out of tanks
xD = x1;
xE = x2;
xF = x3;

// Discharge
D = k1 * h1;
E = k2 * h2;

// Geometry
V1 = A1*h1;
V2 = A2*h2;
V3 = A3*h3;

// Mass to volume
V1 = M1*(x1/rhox + (1 - x1)/rhoy);
V2 = M2*(x2/rhox + (1 - x2)/rhoy);
V3 = M3*(x3/rhox + (1 - x3)/rhoy);

annotation(
    experiment(StartTime = 0, StopTime = 20, Tolerance = 1e-6, Interval = 0.04));

end MixingSystem;
