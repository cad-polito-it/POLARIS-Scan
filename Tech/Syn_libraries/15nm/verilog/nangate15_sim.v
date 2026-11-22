// Behavioral simulation model generated from Liberty for Verilator
module AND2_X1 (A1, A2, Z);
  input A1;
  input A2;
  output Z;
  assign Z = (A1 & A2);
endmodule

module AND2_X2 (A1, A2, Z);
  input A1;
  input A2;
  output Z;
  assign Z = (A1 & A2);
endmodule

module AND3_X1 (A1, A2, A3, Z);
  input A1;
  input A2;
  input A3;
  output Z;
  assign Z = ((A1 & A2) & A3);
endmodule

module AND3_X2 (A1, A2, A3, Z);
  input A1;
  input A2;
  input A3;
  output Z;
  assign Z = ((A1 & A2) & A3);
endmodule

module AND4_X1 (A1, A2, A3, A4, Z);
  input A1;
  input A2;
  input A3;
  input A4;
  output Z;
  assign Z = (((A1 & A2) & A3) & A4);
endmodule

module AND4_X2 (A1, A2, A3, A4, Z);
  input A1;
  input A2;
  input A3;
  input A4;
  output Z;
  assign Z = (((A1 & A2) & A3) & A4);
endmodule

module ANTENNA (I);
  input I;
endmodule

module AOI21_X1 (A1, A2, B, ZN);
  input A1;
  input A2;
  input B;
  output ZN;
  assign ZN = ~((A1 & A2) | B);
endmodule

module AOI21_X2 (A1, A2, B, ZN);
  input A1;
  input A2;
  input B;
  output ZN;
  assign ZN = ~((A1 & A2) | B);
endmodule

module AOI22_X1 (A1, A2, B1, B2, ZN);
  input A1;
  input A2;
  input B1;
  input B2;
  output ZN;
  assign ZN = ~((A1 & A2) | (B1 & B2));
endmodule

module AOI22_X2 (A1, A2, B1, B2, ZN);
  input A1;
  input A2;
  input B1;
  input B2;
  output ZN;
  assign ZN = ~((A1 & A2) | (B1 & B2));
endmodule

module BUF_X1 (I, Z);
  input I;
  output Z;
  assign Z = I;
endmodule

module BUF_X2 (I, Z);
  input I;
  output Z;
  assign Z = I;
endmodule

module BUF_X4 (I, Z);
  input I;
  output Z;
  assign Z = I;
endmodule

module BUF_X8 (I, Z);
  input I;
  output Z;
  assign Z = I;
endmodule

module BUF_X12 (I, Z);
  input I;
  output Z;
  assign Z = I;
endmodule

module BUF_X16 (I, Z);
  input I;
  output Z;
  assign Z = I;
endmodule

module CLKBUF_X1 (I, Z);
  input I;
  output Z;
  assign Z = I;
endmodule

module CLKBUF_X2 (I, Z);
  input I;
  output Z;
  assign Z = I;
endmodule

module CLKBUF_X4 (I, Z);
  input I;
  output Z;
  assign Z = I;
endmodule

module CLKBUF_X8 (I, Z);
  input I;
  output Z;
  assign Z = I;
endmodule

module CLKBUF_X12 (I, Z);
  input I;
  output Z;
  assign Z = I;
endmodule

module CLKBUF_X16 (I, Z);
  input I;
  output Z;
  assign Z = I;
endmodule

module CLKGATETST_X1 (QD, CLK, E, TE, Q);
  input CLK;
  input E;
  input TE;
  output Q;
  always @(posedge None) begin
  end
endmodule

module DFFRNQ_X1 (D, RN, CLK, Q);
  input D;
  input RN;
  input CLK;
  output Q;
  reg Q;
  always @(posedge CLK, negedge RN) begin
    if (!RN) begin
      Q <= 1'b0;
    end
    else begin
      Q <= D;
    end
  end
endmodule

module DFFSNQ_X1 (D, SN, CLK, Q);
  input D;
  input SN;
  input CLK;
  output Q;
  reg Q;
  always @(posedge CLK, negedge SN) begin
    if (!SN) begin
      Q <= 1'b1;
    end else begin
      Q <= D;
    end
  end
endmodule

module FA_X1 (A, B, CI, CO, S);
  input A;
  input B;
  input CI;
  output CO;
  output S;
  assign CO = (((B & CI) | (B & A)) | (CI & A));
  assign S = ~((~((B & CI) | ~(B | CI)) & A) | ~(~((B & CI) | ~(B | CI)) | A));
endmodule

module FILLTIE ();
endmodule

module FILL_X1 ();
endmodule

module FILL_X2 ();
endmodule

module FILL_X4 ();
endmodule

module FILL_X8 ();
endmodule

module FILL_X16 ();
endmodule

module HA_X1 (A, B, CO, S);
  input A;
  input B;
  output CO;
  output S;
  assign CO = (A & B);
  assign S = ~((A & B) | ~(A | B));
endmodule

module INV_X1 (I, ZN);
  input I;
  output ZN;
  assign ZN = ~I;
endmodule

module INV_X2 (I, ZN);
  input I;
  output ZN;
  assign ZN = ~I;
endmodule

module INV_X4 (I, ZN);
  input I;
  output ZN;
  assign ZN = ~I;
endmodule

module INV_X8 (I, ZN);
  input I;
  output ZN;
  assign ZN = ~I;
endmodule

module INV_X12 (I, ZN);
  input I;
  output ZN;
  assign ZN = ~I;
endmodule

module INV_X16 (I, ZN);
  input I;
  output ZN;
  assign ZN = ~I;
endmodule

module LHQ_X1 (D, E, Q);
  input D;
  input E;
  output Q;
  reg Q;
  always @(posedge None) begin
    Q <= D;
  end
endmodule

module MUX2_X1 (I0, I1, S, Z);
  input I0;
  input I1;
  input S;
  output Z;
  assign Z = ((S & I1) | (~S & I0));
endmodule

module NAND2_X1 (A1, A2, ZN);
  input A1;
  input A2;
  output ZN;
  assign ZN = ~(A1 & A2);
endmodule

module NAND2_X2 (A1, A2, ZN);
  input A1;
  input A2;
  output ZN;
  assign ZN = ~(A1 & A2);
endmodule

module NAND3_X1 (A1, A2, A3, ZN);
  input A1;
  input A2;
  input A3;
  output ZN;
  assign ZN = ~((A1 & A2) & A3);
endmodule

module NAND3_X2 (A1, A2, A3, ZN);
  input A1;
  input A2;
  input A3;
  output ZN;
  assign ZN = ~((A1 & A2) & A3);
endmodule

module NAND4_X1 (A1, A2, A3, A4, ZN);
  input A1;
  input A2;
  input A3;
  input A4;
  output ZN;
  assign ZN = ~(((A1 & A2) & A3) & A4);
endmodule

module NAND4_X2 (A1, A2, A3, A4, ZN);
  input A1;
  input A2;
  input A3;
  input A4;
  output ZN;
  assign ZN = ~(((A1 & A2) & A3) & A4);
endmodule

module NOR2_X1 (A1, A2, ZN);
  input A1;
  input A2;
  output ZN;
  assign ZN = ~(A1 | A2);
endmodule

module NOR2_X2 (A1, A2, ZN);
  input A1;
  input A2;
  output ZN;
  assign ZN = ~(A1 | A2);
endmodule

module NOR3_X1 (A1, A2, A3, ZN);
  input A1;
  input A2;
  input A3;
  output ZN;
  assign ZN = ~((A1 | A2) | A3);
endmodule

module NOR3_X2 (A1, A2, A3, ZN);
  input A1;
  input A2;
  input A3;
  output ZN;
  assign ZN = ~((A1 | A2) | A3);
endmodule

module NOR4_X1 (A1, A2, A3, A4, ZN);
  input A1;
  input A2;
  input A3;
  input A4;
  output ZN;
  assign ZN = ~(((A1 | A2) | A3) | A4);
endmodule

module NOR4_X2 (A1, A2, A3, A4, ZN);
  input A1;
  input A2;
  input A3;
  input A4;
  output ZN;
  assign ZN = ~(((A1 | A2) | A3) | A4);
endmodule

module OAI21_X1 (A1, A2, B, ZN);
  input A1;
  input A2;
  input B;
  output ZN;
  assign ZN = ~((A1 | A2) & B);
endmodule

module OAI21_X2 (A1, A2, B, ZN);
  input A1;
  input A2;
  input B;
  output ZN;
  assign ZN = ~((A1 | A2) & B);
endmodule

module OAI22_X1 (A1, A2, B1, B2, ZN);
  input A1;
  input A2;
  input B1;
  input B2;
  output ZN;
  assign ZN = ~((A1 | A2) & (B1 | B2));
endmodule

module OAI22_X2 (A1, A2, B1, B2, ZN);
  input A1;
  input A2;
  input B1;
  input B2;
  output ZN;
  assign ZN = ~((A1 | A2) & (B1 | B2));
endmodule

module OR2_X1 (A1, A2, Z);
  input A1;
  input A2;
  output Z;
  assign Z = (A1 | A2);
endmodule

module OR2_X2 (A1, A2, Z);
  input A1;
  input A2;
  output Z;
  assign Z = (A1 | A2);
endmodule

module OR3_X1 (A1, A2, A3, Z);
  input A1;
  input A2;
  input A3;
  output Z;
  assign Z = ((A1 | A2) | A3);
endmodule

module OR3_X2 (A1, A2, A3, Z);
  input A1;
  input A2;
  input A3;
  output Z;
  assign Z = ((A1 | A2) | A3);
endmodule

module OR4_X1 (A1, A2, A3, A4, Z);
  input A1;
  input A2;
  input A3;
  input A4;
  output Z;
  assign Z = (((A1 | A2) | A3) | A4);
endmodule

module OR4_X2 (A1, A2, A3, A4, Z);
  input A1;
  input A2;
  input A3;
  input A4;
  output Z;
  assign Z = (((A1 | A2) | A3) | A4);
endmodule

module SDFFRNQ_X1 (D, RN, SE, SI, CLK, Q);
  input D;
  input RN;
  input SE;
  input SI;
  input CLK;
  output Q;
  reg Q;
  always @(posedge CLK, negedge RN) begin
    if (!RN) begin
      Q <= 1'b0;
    end
    else begin
      Q <= D;
    end
  end
endmodule

module SDFFSNQ_X1 (D, SE, SI, SN, CLK, Q);
  input D;
  input SE;
  input SI;
  input SN;
  input CLK;
  output Q;
  reg Q;
  always @(posedge CLK, negedge SN) begin
    if (!SN) begin
      Q <= 1'b1;
    end else begin
      Q <= D;
    end
  end
endmodule

module TBUF_X1 (EN, I, Z);
  input EN;
  input I;
  output Z;
  assign Z = I;
endmodule

module TBUF_X2 (EN, I, Z);
  input EN;
  input I;
  output Z;
  assign Z = I;
endmodule

module TBUF_X4 (EN, I, Z);
  input EN;
  input I;
  output Z;
  assign Z = I;
endmodule

module TBUF_X8 (EN, I, Z);
  input EN;
  input I;
  output Z;
  assign Z = I;
endmodule

module TBUF_X12 (EN, I, Z);
  input EN;
  input I;
  output Z;
  assign Z = I;
endmodule

module TBUF_X16 (EN, I, Z);
  input EN;
  input I;
  output Z;
  assign Z = I;
endmodule

module TIEH (Z);
  output Z;
  assign Z = 1;
endmodule

module TIEL (ZN);
  output ZN;
  assign ZN = 0;
endmodule

module XNOR2_X1 (A1, A2, ZN);
  input A1;
  input A2;
  output ZN;
  assign ZN = ~(~((A1 & A2) | ~(A1 | A2)));
endmodule

module XOR2_X1 (A1, A2, Z);
  input A1;
  input A2;
  output Z;
  assign Z = ~((A1 & A2) | ~(A1 | A2));
endmodule
