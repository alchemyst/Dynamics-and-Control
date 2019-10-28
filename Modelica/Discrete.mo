model Discrete
  Modelica.Blocks.Sources.Ramp ramp1 annotation(
    Placement(visible = true, transformation(origin = {-118, 44}, extent = {{-10, -10}, {10, 10}}, rotation = 0)));
  Modelica.Blocks.Continuous.FirstOrder firstOrder1 annotation(
    Placement(visible = true, transformation(origin = {6, 44}, extent = {{-10, -10}, {10, 10}}, rotation = 0)));
  Modelica.Blocks.Discrete.Sampler sampler1(samplePeriod = 1)  annotation(
    Placement(visible = true, transformation(origin = {-38, -10}, extent = {{-10, -10}, {10, 10}}, rotation = 0)));
  Modelica.Blocks.Discrete.ZeroOrderHold zeroOrderHold1(samplePeriod = 1)  annotation(
    Placement(visible = true, transformation(origin = {56, -10}, extent = {{-10, -10}, {10, 10}}, rotation = 0)));
  Modelica.Blocks.Discrete.TransferFunction transferFunction1(a = {2, -1}, b = {1, 0}, samplePeriod = 1)  annotation(
    Placement(visible = true, transformation(origin = {12, -10}, extent = {{-10, -10}, {10, 10}}, rotation = 0)));
  Modelica.Blocks.Continuous.FirstOrder firstOrder2 annotation(
    Placement(visible = true, transformation(origin = {50, -72}, extent = {{-10, -10}, {10, 10}}, rotation = 0)));
  Modelica.Blocks.Discrete.Sampler sampler2(samplePeriod = 1) annotation(
    Placement(visible = true, transformation(origin = {-34, -72}, extent = {{-10, -10}, {10, 10}}, rotation = 0)));
  Modelica.Blocks.Discrete.ZeroOrderHold zeroOrderHold2(samplePeriod = 1) annotation(
    Placement(visible = true, transformation(origin = {6, -72}, extent = {{-10, -10}, {10, 10}}, rotation = 0)));
  Modelica.Blocks.Discrete.TransferFunction transferFunction2(a = { 1, -exp(-1)}, b = {1 - exp(-1)}, samplePeriod = 1) annotation(
    Placement(visible = true, transformation(origin = {42, -126}, extent = {{-10, -10}, {10, 10}}, rotation = 0)));
  Modelica.Blocks.Discrete.Sampler sampler3(samplePeriod = 1) annotation(
    Placement(visible = true, transformation(origin = {90, -72}, extent = {{-10, -10}, {10, 10}}, rotation = 0)));
equation
  connect(firstOrder2.y, sampler3.u) annotation(
    Line(points = {{61, -72}, {69, -72}, {69, -72}, {79, -72}, {79, -72}, {77, -72}, {77, -72}, {77, -72}}, color = {128, 0, 128}, thickness = 1));
  connect(sampler2.y, transferFunction2.u) annotation(
    Line(points = {{-23, -72}, {-17, -72}, {-17, -126}, {30, -126}}, color = {252, 1, 7}, pattern = LinePattern.Dash, thickness = 1));
  connect(sampler2.y, zeroOrderHold2.u) annotation(
    Line(points = {{-23, -72}, {-21.875, -72}, {-21.875, -72}, {-20.75, -72}, {-20.75, -72}, {-18.5, -72}, {-18.5, -72}, {-14, -72}, {-14, -72}, {-7, -72}, {-7, -72}, {-6, -72}, {-6, -72}, {-6.5, -72}, {-6.5, -72}, {-6.75, -72}, {-6.75, -72}, {-6.875, -72}, {-6.875, -72}, {-6.9375, -72}, {-6.9375, -72}, {-7, -72}}, color = {252, 1, 7}, pattern = LinePattern.Dash, thickness = 1));
  connect(ramp1.y, firstOrder1.u) annotation(
    Line(points = {{-107, 44}, {-6, 44}}, color = {252, 1, 7}, thickness = 1));
  connect(ramp1.y, sampler1.u) annotation(
    Line(points = {{-107, 44}, {-85.5, 44}, {-85.5, 44}, {-64, 44}, {-64, -10}, {-57, -10}, {-57, -10}, {-53.5, -10}, {-53.5, -10}, {-50, -10}}, color = {252, 1, 7}, thickness = 1));
  connect(ramp1.y, sampler2.u) annotation(
    Line(points = {{-107, 44}, {-79, 44}, {-79, -72}, {-46, -72}}, color = {252, 1, 7}, thickness = 1));
  connect(zeroOrderHold2.y, firstOrder2.u) annotation(
    Line(points = {{17, -72}, {20.75, -72}, {20.75, -72}, {22.5, -72}, {22.5, -72}, {28, -72}, {28, -72}, {39, -72}, {39, -72}, {38, -72}, {38, -72}, {37.5, -72}, {37.5, -72}, {37.25, -72}, {37.25, -72}, {37, -72}}, color = {0, 0, 127}));
  connect(transferFunction1.y, zeroOrderHold1.u) annotation(
    Line(points = {{23, -10}, {34, -10}, {34, -10}, {45, -10}, {45, -10}, {43, -10}, {43, -10}, {43, -10}, {43, -10}, {43, -10}}, color = {0, 0, 127}));
  connect(sampler1.y, transferFunction1.u) annotation(
    Line(points = {{-27, -10}, {-20.5, -10}, {-20.5, -10}, {-14, -10}, {-14, -10}, {1, -10}, {1, -10}, {3.27826e-07, -10}, {3.27826e-07, -10}, {-1, -10}}, color = {0, 0, 127}));
  annotation(
    uses(Modelica(version = "3.2.3")),
    Diagram(graphics = {Rectangle(origin = {11, -8}, extent = {{-67, 74}, {65, -26}}), Text(origin = {-12, 71}, extent = {{-18, 3}, {56, -5}}, textString = "Discrete approximation (Backward Difference)"), Rectangle(origin = {33, -78}, extent = {{-89, 26}, {79, -68}}), Text(origin = {36, -41}, extent = {{-32, -1}, {38, -11}}, textString = "Sampled equivalent (Table 17.1)"), Line(origin = {106.66, -9.84}, points = {{-41, 0}, {43, 0}}, color = {78, 118, 255}, thickness = 1), Line(origin = {92.24, -126.07}, points = {{-41, 0}, {53, 0}}, color = {128, 0, 128}, pattern = LinePattern.Dash, thickness = 1), Line(origin = {140.195, -71.6426}, points = {{-41, 0}, {3, 0}}, color = {128, 0, 128}, pattern = LinePattern.Dash, thickness = 1), Text(origin = {144, -97}, rotation = 90, extent = {{-32, -1}, {28, -7}}, textString = "Exactly the same"), Text(origin = {152, 17}, rotation = 90, extent = {{-28, -1}, {28, -7}}, textString = "Approximately the same"), Line(origin = {57.2311, 44.2907}, points = {{-41, 0}, {91, 0}}, color = {0, 0, 255}, thickness = 1)}),
  experiment(StartTime = 0, StopTime = 10, Tolerance = 1e-6, Interval = 0.02),
  __OpenModelica_simulationFlags(lv = "LOG_STATS", outputFormat = "mat", s = "dassl"));end Discrete;