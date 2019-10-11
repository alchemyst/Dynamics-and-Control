model FedBatchBioreactorModel
/* This model represents the fed batch bioreactor in section 2.4.9 of
   Seborg et al.
   
   To keep things simple we pretend that the time unit is seconds rather than hours.
*/
  parameter Real mu_max = 0.2 "Maximum growth rate";
  parameter Real K_s = 1.0 "Monod constant";
  parameter Real Y_xs = 0.5 "Cell yield coefficient";
  parameter Real Y_px = 0.2 "Product yield coefficient";
  Real X(start=0.05) "Concentration of the cells";
  Real S(start=10) "Concentration of the substrate";
  Real P(start=0) "Concentration of the product";
  Real V(start=1) "Reactor volume";
  parameter Real F=0.05 "Feed rate";
  Real S_f=10 "Concentration of substrate in feed";
  Real mu "Specific growth rate";
  Real rg "Rate of cell growth";
  Real rp "Rate of product formation";
equation
  rg = mu * X;
  mu = mu_max * S / (K_s + S);
  rp = Y_px * rg;
  der(X * V) = V * rg;
  der(P * V) = V * rp;
  der(S * V) = F * S_f - 1 / Y_xs * V * rg;
  der(V) = F;
  annotation(experiment(StartTime = 0, StopTime = 30));
end FedBatchBioreactorModel;
