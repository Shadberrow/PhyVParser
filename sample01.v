Hello, world!
input [7:0] CR_ADDRESS
This is a simple text here.
output [127:0] buff1;
output [3:0] state;
inout VDD;
inout VSS;
Some lines going on.
And one more here.
wire [7:0] cr_address;
wire [4:0] pcnt;

wire FE_OFN1262_cr_address_3_;

DEL01BWP7T FE_OFC1262_cr_address_3_ (
.Z(FE_OFN1262_cr_address_3_),
.I(cr_address[3]),
.VDD(VDD_0),
.VSS(VSS_0));

DEL01BWP7T FE_OFC1262_CR_address_3_ (
.Z(FE_OFN1262_cr_address_3_),
.I(CR_ADDRESS[3]),
.VDD(VDD_0),
.VSS(VSS_0));
