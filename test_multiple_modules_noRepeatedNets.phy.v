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
  wire n103;
  wire n104;

  B mymodule1 (
    .in_B_one(in_A_one),
    .in_B_two(in_A_two),
    .in_B_three(n102),
    .in_B_four(in_A_three),
    .out_B_one(n103),
    .out_B_two(out_A),
    .out_B_three(in_A_two),
    .out_B(n104),
    .VDD(VDD),
    .VSS(VSS)
  );

endmodule

module C (
in_A_one,
VDD,
VSS
);

  inout VDD;
  inout VSS;
  input in_A_one;

  wire n101;

endmodule
