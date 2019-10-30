// test_multiple_modules.phy.v

module A (
  in_A_one,
  in_A_two,
  in_A_three,
  in_A_four,
  out_A_one,
  out_A_two,
  out_A_three,
  out_A,
  VDD,
  VSS
);

  inout VDD;
  inout VSS;
  input in_A_one;
  input in_A_two;
  input in_A_three;
  input in_A_four;
  output out_A_one;
  output out_A_two;
  output out_A_three;
  output out_A;

  // Internal wires
  wire n101;
  wire n102;
  wire FCNN_N101;
  wire FCNN_IN_A_ONE;

  B mymodule1 (
    .in_B_one(in_A_one),
    .in_B_two(in_A_two),
    .in_B_three(n102),
    .in_B_four(in_A_three),
    .out_B_one(FCNN_N101),
    .out_B_two(out_A),
    .out_B_three(in_A_two),
    .out_B(FCNN_IN_A_ONE),
    .VDD(VDD),
    .VSS(VSS)
  );

endmodule


module B (
  in_B_one,
  in_B_two,
  in_B_three,
  in_B_four,
  out_B_one,
  out_B_two,
  out_B_three,
  out_B,
  VDD,
  VSS
);

  inout VDD;
  inout VSS;
  input in_B_one;
  input in_B_two;
  input in_B_three;
  input in_B_four;
  output out_B_one;
  output out_B_two;
  output out_B_three;
  output out_B;

  // Internal wires
  wire n732;
  wire n164;
  wire N300;
  wire FCNN_n300;

  DEL01BWP7T FE_OFC1487_n164 (
 .Z(N300),
 .I(in_B_four),
 .VDD(VDD),
 .VSS(VSS));

endmodule

module C (
VDD,
VSS
);

  inout VDD;
  inout VSS;

endmodule
