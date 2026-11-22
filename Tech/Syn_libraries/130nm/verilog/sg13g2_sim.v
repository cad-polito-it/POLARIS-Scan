// Behavioral simulation model generated from Liberty for Verilator
module sg13g2_a21o_1 (X, A1, A2, B1);
  input A1;
  input A2;
  input B1;
  output X;
  assign X = ((A1&A2)|B1);
endmodule

module sg13g2_a21o_2 (X, A1, A2, B1);
  input A1;
  input A2;
  input B1;
  output X;
  assign X = ((A1&A2)|B1);
endmodule

module sg13g2_a21oi_1 (Y, A1, A2, B1);
  input A1;
  input A2;
  input B1;
  output Y;
  assign Y = ~((A1&A2)|B1);
endmodule

module sg13g2_a21oi_2 (Y, A1, A2, B1);
  input A1;
  input A2;
  input B1;
  output Y;
  assign Y = ~((A1&A2)|B1);
endmodule

module sg13g2_a221oi_1 (Y, A1, A2, B1, B2, C1);
  input A1;
  input A2;
  input B1;
  input B2;
  input C1;
  output Y;
  assign Y = ~((A1&A2)|(B1&B2)|C1);
endmodule

module sg13g2_a22oi_1 (Y, A1, A2, B1, B2);
  input A1;
  input A2;
  input B1;
  input B2;
  output Y;
  assign Y = ~((A1&A2)|(B1&B2));
endmodule

module sg13g2_and2_1 (X, A, B);
  input A;
  input B;
  output X;
  assign X = (A&B);
endmodule

module sg13g2_and2_2 (X, A, B);
  input A;
  input B;
  output X;
  assign X = (A&B);
endmodule

module sg13g2_and3_1 (X, A, B, C);
  input A;
  input B;
  input C;
  output X;
  assign X = (A&B&C);
endmodule

module sg13g2_and3_2 (X, A, B, C);
  input A;
  input B;
  input C;
  output X;
  assign X = (A&B&C);
endmodule

module sg13g2_and4_1 (X, A, B, C, D);
  input A;
  input B;
  input C;
  input D;
  output X;
  assign X = (A&B&C&D);
endmodule

module sg13g2_and4_2 (X, A, B, C, D);
  input A;
  input B;
  input C;
  input D;
  output X;
  assign X = (A&B&C&D);
endmodule

module sg13g2_antennanp (A);
  input A;
endmodule

module sg13g2_buf_1 (X, A);
  input A;
  output X;
  assign X = A;
endmodule

module sg13g2_buf_16 (X, A);
  input A;
  output X;
  assign X = A;
endmodule

module sg13g2_buf_2 (X, A);
  input A;
  output X;
  assign X = A;
endmodule

module sg13g2_buf_4 (X, A);
  input A;
  output X;
  assign X = A;
endmodule

module sg13g2_buf_8 (X, A);
  input A;
  output X;
  assign X = A;
endmodule

module sg13g2_decap_4 ();
endmodule

module sg13g2_decap_8 ();
endmodule

module sg13g2_dfrbp_1 (Q, Q_N, CLK, D, RESET_B);
  input CLK;
  input D;
  input RESET_B;
  output Q;
  output Q_N;
  reg Q;
  assign Q_N = ~Q;
  always @(posedge CLK, negedge RESET_B) begin
    if (!RESET_B) begin
      Q <= 1'b0;
    end
    else begin
      Q <= D;
    end
  end
endmodule

module sg13g2_dfrbp_2 (Q, Q_N, CLK, D, RESET_B);
  input CLK;
  input D;
  input RESET_B;
  output Q;
  output Q_N;
  reg Q;
  assign Q_N = ~Q;
  always @(posedge CLK, negedge RESET_B) begin
    if (!RESET_B) begin
      Q <= 1'b0;
    end
    else begin
      Q <= D;
    end
  end
endmodule

module sg13g2_dlhq_1 (Q, D, GATE);
  input D;
  input GATE;
  output Q;
  reg Q;
  always @(posedge None) begin
    Q <= D;
  end
endmodule

module sg13g2_dlhr_1 (Q, Q_N, D, GATE, RESET_B);
  input D;
  input GATE;
  input RESET_B;
  output Q;
  output Q_N;
  reg Q;
  assign Q_N = ~Q;
  always @(posedge None, negedge RESET_B) begin
    if (!RESET_B) begin
      Q <= 1'b0;
    end
    else begin
      Q <= D;
    end
  end
endmodule

module sg13g2_dlhrq_1 (Q, D, GATE, RESET_B);
  input D;
  input GATE;
  input RESET_B;
  output Q;
  reg Q;
  always @(posedge None, negedge RESET_B) begin
    if (!RESET_B) begin
      Q <= 1'b0;
    end
    else begin
      Q <= D;
    end
  end
endmodule

module sg13g2_dllr_1 (Q, Q_N, D, GATE_N, RESET_B);
  input D;
  input GATE_N;
  input RESET_B;
  output Q;
  output Q_N;
  reg Q;
  assign Q_N = ~Q;
  always @(posedge None, negedge RESET_B) begin
    if (!RESET_B) begin
      Q <= 1'b0;
    end
    else begin
      Q <= D;
    end
  end
endmodule

module sg13g2_dllrq_1 (Q, D, GATE_N, RESET_B);
  input D;
  input GATE_N;
  input RESET_B;
  output Q;
  reg Q;
  always @(posedge None, negedge RESET_B) begin
    if (!RESET_B) begin
      Q <= 1'b0;
    end
    else begin
      Q <= D;
    end
  end
endmodule

module sg13g2_dlygate4sd1_1 (X, A);
  input A;
  output X;
  assign X = A;
endmodule

module sg13g2_dlygate4sd2_1 (X, A);
  input A;
  output X;
  assign X = A;
endmodule

module sg13g2_dlygate4sd3_1 (X, A);
  input A;
  output X;
  assign X = A;
endmodule

module sg13g2_ebufn_2 (Z, A, TE_B);
  input A;
  input TE_B;
  output Z;
  assign Z = A;
endmodule

module sg13g2_ebufn_4 (Z, A, TE_B);
  input A;
  input TE_B;
  output Z;
  assign Z = A;
endmodule

module sg13g2_ebufn_8 (Z, A, TE_B);
  input A;
  input TE_B;
  output Z;
  assign Z = A;
endmodule

module sg13g2_einvn_2 (Z, A, TE_B);
  input A;
  input TE_B;
  output Z;
  assign Z = ~(A);
endmodule

module sg13g2_einvn_4 (Z, A, TE_B);
  input A;
  input TE_B;
  output Z;
  assign Z = ~(A);
endmodule

module sg13g2_einvn_8 (Z, A, TE_B);
  input A;
  input TE_B;
  output Z;
  assign Z = ~(A);
endmodule

module sg13g2_fill_1 ();
endmodule

module sg13g2_fill_2 ();
endmodule

module sg13g2_fill_4 ();
endmodule

module sg13g2_fill_8 ();
endmodule

module sg13g2_inv_1 (Y, A);
  input A;
  output Y;
  assign Y = ~(A);
endmodule

module sg13g2_inv_16 (Y, A);
  input A;
  output Y;
  assign Y = ~(A);
endmodule

module sg13g2_inv_2 (Y, A);
  input A;
  output Y;
  assign Y = ~(A);
endmodule

module sg13g2_inv_4 (Y, A);
  input A;
  output Y;
  assign Y = ~(A);
endmodule

module sg13g2_inv_8 (Y, A);
  input A;
  output Y;
  assign Y = ~(A);
endmodule

module sg13g2_lgcp_1 (int_GATE, GCLK, CLK, GATE);
  input CLK;
  input GATE;
  output GCLK;
  always @(posedge None) begin
  end
endmodule

module sg13g2_mux2_1 (X, A0, A1, S);
  input A0;
  input A1;
  input S;
  output X;
  assign X = (~S&A0)|(S&A1);
endmodule

module sg13g2_mux2_2 (X, A0, A1, S);
  input A0;
  input A1;
  input S;
  output X;
  assign X = (~S&A0)|(S&A1);
endmodule

module sg13g2_mux4_1 (X, A0, A1, A2, A3, S0, S1);
  input A0;
  input A1;
  input A2;
  input A3;
  input S0;
  input S1;
  output X;
  assign X = (A0&(~S0&~S1))|(A1&(S0&~S1))|(A2&(~S0&S1))|(A3&(S0&S1));
endmodule

module sg13g2_nand2_1 (Y, A, B);
  input A;
  input B;
  output Y;
  assign Y = ~(A&B);
endmodule

module sg13g2_nand2_2 (Y, A, B);
  input A;
  input B;
  output Y;
  assign Y = ~(A&B);
endmodule

module sg13g2_nand2b_1 (Y, A_N, B);
  input A_N;
  input B;
  output Y;
  assign Y = ~(~A_N&B);
endmodule

module sg13g2_nand2b_2 (Y, A_N, B);
  input A_N;
  input B;
  output Y;
  assign Y = ~(~A_N&B);
endmodule

module sg13g2_nand3_1 (Y, A, B, C);
  input A;
  input B;
  input C;
  output Y;
  assign Y = ~(A&B&C);
endmodule

module sg13g2_nand3b_1 (Y, A_N, B, C);
  input A_N;
  input B;
  input C;
  output Y;
  assign Y = ~(~A_N&B&C);
endmodule

module sg13g2_nand4_1 (Y, A, B, C, D);
  input A;
  input B;
  input C;
  input D;
  output Y;
  assign Y = ~(A&B&C&D);
endmodule

module sg13g2_nor2_1 (Y, A, B);
  input A;
  input B;
  output Y;
  assign Y = ~(A|B);
endmodule

module sg13g2_nor2_2 (Y, A, B);
  input A;
  input B;
  output Y;
  assign Y = ~(A|B);
endmodule

module sg13g2_nor2b_1 (Y, A, B_N);
  input A;
  input B_N;
  output Y;
  assign Y = ~(A|~B_N);
endmodule

module sg13g2_nor2b_2 (Y, A, B_N);
  input A;
  input B_N;
  output Y;
  assign Y = ~(A|~B_N);
endmodule

module sg13g2_nor3_1 (Y, A, B, C);
  input A;
  input B;
  input C;
  output Y;
  assign Y = ~(A|B|C);
endmodule

module sg13g2_nor3_2 (Y, A, B, C);
  input A;
  input B;
  input C;
  output Y;
  assign Y = ~(A|B|C);
endmodule

module sg13g2_nor4_1 (Y, A, B, C, D);
  input A;
  input B;
  input C;
  input D;
  output Y;
  assign Y = ~(A|B|C|D);
endmodule

module sg13g2_nor4_2 (Y, A, B, C, D);
  input A;
  input B;
  input C;
  input D;
  output Y;
  assign Y = ~(A|B|C|D);
endmodule

module sg13g2_o21ai_1 (Y, A1, A2, B1);
  input A1;
  input A2;
  input B1;
  output Y;
  assign Y = ~((A1|A2)&B1);
endmodule

module sg13g2_or2_1 (X, A, B);
  input A;
  input B;
  output X;
  assign X = (A|B);
endmodule

module sg13g2_or2_2 (X, A, B);
  input A;
  input B;
  output X;
  assign X = (A|B);
endmodule

module sg13g2_or3_1 (X, A, B, C);
  input A;
  input B;
  input C;
  output X;
  assign X = (A|B|C);
endmodule

module sg13g2_or3_2 (X, A, B, C);
  input A;
  input B;
  input C;
  output X;
  assign X = (A|B|C);
endmodule

module sg13g2_or4_1 (X, A, B, C, D);
  input A;
  input B;
  input C;
  input D;
  output X;
  assign X = (A|B|C|D);
endmodule

module sg13g2_or4_2 (X, A, B, C, D);
  input A;
  input B;
  input C;
  input D;
  output X;
  assign X = (A|B|C|D);
endmodule

module sg13g2_sdfbbp_1 (Q, Q_N, CLK, D, RESET_B, SCD, SCE, SET_B);
  input CLK;
  input D;
  input RESET_B;
  input SCD;
  input SCE;
  input SET_B;
  output Q;
  output Q_N;
  reg Q;
  assign Q_N = ~Q;
  always @(posedge CLK, negedge RESET_B, negedge SET_B) begin
    if (!RESET_B) begin
      Q <= 1'b0;
    end
    else if (!SET_B) begin
      Q <= 1'b1;
    end
    else begin
      Q <= D;
    end
  end
endmodule

module sg13g2_sighold (SH);
  output SH;
endmodule

module sg13g2_slgcp_1 (int_GATE, GCLK, CLK, GATE, SCE);
  input CLK;
  input GATE;
  input SCE;
  output GCLK;
  always @(posedge None) begin
  end
endmodule

module sg13g2_tiehi (L_HI);
  output L_HI;
  assign L_HI = 1;
endmodule

module sg13g2_tielo (L_LO);
  output L_LO;
  assign L_LO = 0;
endmodule

module sg13g2_xnor2_1 (Y, A, B);
  input A;
  input B;
  output Y;
  assign Y = ~(A^B);
endmodule

module sg13g2_xor2_1 (X, A, B);
  input A;
  input B;
  output X;
  assign X = (A^B);
endmodule
