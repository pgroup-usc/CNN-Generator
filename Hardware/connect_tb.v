`timescale 1ns / 1ps
//////////////////////////////////////////////////////////////////////////////////
// Company: 
// Engineer: 
// 
// Create Date: 09/01/2019 01:07:04 PM
// Design Name: 
// Module Name: fft2D_tb
// Project Name: 
// Target Devices: 
// Tool Versions: 
// Description: 
// 
// Dependencies: 
// 
// Revision:
// Revision 0.01 - File Created
// Additional Comments:
// 
//////////////////////////////////////////////////////////////////////////////////


module connect_tb();
	localparam DATALEN = 16;
	localparam FFTCHNL = 8;
	localparam CMPLXLEN = 2*DATALEN;
    localparam CIN = 2;
    localparam COUT = 2;
	reg clk, rstn;

	/*-------- FFT signal --------*/
	reg invalid;
	reg [FFTCHNL*2*DATALEN-1 : 0] indata;
	reg [FFTCHNL*2*DATALEN-1 : 0] indata_reg;
	wire outvalid;
	wire [FFTCHNL*2*2*DATALEN-1 : 0] outdata;

	/*-------- generate clock signal --------*/
	initial begin
		#0  rstn = 1'b1;
		#5  rstn = 1'b0;
		#30 rstn = 1'b1;
	end
	initial begin
		#0  clk  = 1'b0;

		forever #10 clk = ~clk;
	end

	/*-------- load binary data first --------*/
	integer fp, fp_fft1D, fp_fft2D, stat;
	// 16bit X-Y X:lower 8 bits, y: higher 8 bits
	reg [DATALEN-1 : 0]  filebuf[0 : 8-1][0 : 8-1];
	reg [2*DATALEN-1 : 0] ref_fft1D_buf[0 : 8-1][0 : 8-1];
	reg [2*DATALEN-1 : 0] ref_fft2D_buf[0 : 8-1][0 : 8-1];
	reg [DATALEN-1 : 0] tmpbuf[0 : 8-1];
	reg [2*DATALEN-1 : 0] tmpbuf1[0 : 8-1];
	reg [2*DATALEN-1 : 0] tmpbuf2[0 : 8-1];
	reg [4-1 : 0] _readline_;
	integer _rdcol_;
	always @(posedge clk or negedge rstn) begin
		if (~rstn) begin
			_readline_ = 4'd0;
			fp         = $fopen("input.bin", "rb");
			fp_fft1D   = $fopen("infft1Dref.bin", "rb");
			fp_fft2D   = $fopen("infft2Dref.bin", "rb");
			if (fp) 
				$display("[INFO]: file input.bin found.");
			else begin
				$display("[ERR]: failed to open file input.bin.");
				$finish;
			end
			if (fp_fft1D) 
				$display("[INFO]: file infft1Dref.bin found.");
			else begin
				$display("[ERR]: failed to open file infft1Dref.bin.");
				$finish;
			end
			if (fp_fft2D) 
				$display("[INFO]: file infft2Dref.bin found.");
			else begin
				$display("[ERR]: failed to open file infft2Dref.bin.");
				$finish;
			end
		end
		else if (_readline_ < 4'd8 )begin
				$display("read %dth row.", _readline_);
				stat = $fread(tmpbuf, fp);
				filebuf[_readline_] = tmpbuf;
				stat = $fread(tmpbuf1, fp_fft1D);
				for (_rdcol_ = 0; _rdcol_ < 8; _rdcol_++) begin
					ref_fft1D_buf[_readline_][_rdcol_][7  : 0]  = tmpbuf1[_rdcol_][31 : 24];
					ref_fft1D_buf[_readline_][_rdcol_][15 : 8]  = tmpbuf1[_rdcol_][23 : 16];
					ref_fft1D_buf[_readline_][_rdcol_][23 : 16] = tmpbuf1[_rdcol_][15 : 8];
					ref_fft1D_buf[_readline_][_rdcol_][31 : 24] = tmpbuf1[_rdcol_][7  : 0];
				end
				stat = $fread(tmpbuf2, fp_fft2D);
				for (_rdcol_ = 0; _rdcol_ < 8; _rdcol_++) begin
					ref_fft2D_buf[_readline_][_rdcol_][7  : 0]  = tmpbuf2[_rdcol_][31 : 24];
					ref_fft2D_buf[_readline_][_rdcol_][15 : 8]  = tmpbuf2[_rdcol_][23 : 16];
					ref_fft2D_buf[_readline_][_rdcol_][23 : 16] = tmpbuf2[_rdcol_][15 : 8];
					ref_fft2D_buf[_readline_][_rdcol_][31 : 24] = tmpbuf2[_rdcol_][7  : 0];
				end

				_readline_ <= _readline_ + 1;
		end
	end

	/*-------- construct inputs --------*/
	integer _cntin_;
	integer j;
	initial begin
		wait(_readline_ == 4'd8);

		invalid = 1'b1;
		for (_cntin_ = 0; _cntin_ < 8; _cntin_++) begin
			@(posedge clk);
			
			indata[1*2*DATALEN-1 : DATALEN] = {DATALEN{1'b0}};
			indata[DATALEN-1 : 0] = 
			{filebuf[_cntin_][0][7:0],filebuf[_cntin_][0][15:8]};

			indata[2*2*DATALEN-1 : 1*2*DATALEN+DATALEN] = {DATALEN{1'b0}};
			indata[1*2*DATALEN+DATALEN-1 : 1*2*DATALEN] = 
			{filebuf[_cntin_][1][7:0],filebuf[_cntin_][1][15:8]};

			indata[3*2*DATALEN-1 : 2*2*DATALEN+DATALEN] = {DATALEN{1'b0}};
			indata[2*2*DATALEN+DATALEN-1 : 2*2*DATALEN] = 
			{filebuf[_cntin_][2][7:0],filebuf[_cntin_][2][15:8]};

			indata[4*2*DATALEN-1 : 3*2*DATALEN+DATALEN] = {DATALEN{1'b0}};
			indata[3*2*DATALEN+DATALEN-1 : 3*2*DATALEN] =
			{filebuf[_cntin_][3][7:0],filebuf[_cntin_][3][15:8]};

			indata[5*2*DATALEN-1 : 4*2*DATALEN+DATALEN] = {DATALEN{1'b0}};
			indata[4*2*DATALEN+DATALEN-1 : 4*2*DATALEN] =
			{filebuf[_cntin_][4][7:0],filebuf[_cntin_][4][15:8]};

			indata[6*2*DATALEN-1 : 5*2*DATALEN+DATALEN] = {DATALEN{1'b0}};
			indata[5*2*DATALEN+DATALEN-1 : 5*2*DATALEN] = 
			{filebuf[_cntin_][5][7:0],filebuf[_cntin_][5][15:8]};

			indata[7*2*DATALEN-1 : 6*2*DATALEN+DATALEN] = {DATALEN{1'b0}};
			indata[6*2*DATALEN+DATALEN-1 : 6*2*DATALEN] = 
			{filebuf[_cntin_][6][7:0],filebuf[_cntin_][6][15:8]};

			indata[8*2*DATALEN-1 : 7*2*DATALEN+DATALEN] = {DATALEN{1'b0}};
			indata[7*2*DATALEN+DATALEN-1 : 7*2*DATALEN] = 
			{filebuf[_cntin_][7][7:0],filebuf[_cntin_][7][15:8]};
			//@(posedge clk);
			//invalid <= 1'b0;
		end
		//@(posedge clk);
		invalid <= 1'b0;
	end

    integer _krnrow_, _krncol_;
    reg [COUT * CIN - 1 : 0 ] krnvalid;
    reg [COUT * CIN * 2*DATALEN-1 : 0] krndata;

        genvar _cin_;
        genvar _cout_;

 
                initial begin
                krnvalid <= 4'b0;
 ;
                wait (_readline_ == 4'd8);
                @(posedge clk);

                //--read one pixel per clock
                for (_krnrow_ = 0; _krnrow_ < 8; _krnrow_++) begin
                    for (_krncol_ = 0; _krncol_ < 8; _krncol_++) begin
                        
                        krnvalid <= 4'b1;
                        krndata <= {CIN*COUT{ref_fft2D_buf[_krnrow_][_krncol_]}};
                        
                        
                        @(posedge clk);
                    end
                   
                end

                krnvalid <= 4'b0;
                end
    
    
 

	/*-------- add test module --------*/
	connect DUT(
		.clk(clk),
		.rstn(rstn),
        .inkvalid(krnvalid[0]), .kindata(krndata),
		.invalid(invalid), .indata({CIN{indata}}),

		.outvalid(outvalid), .outdata(outdata)
	);
integer _row_, _col_;
	
	wire [2*DATALEN-1 : 0] outdata_array [0 : FFTCHNL-1][0 : 2-1];
	generate
		genvar i;
		for (i = 0; i < 8; i++) begin
			assign outdata_array[i][0] = outdata[(i+1)*2*CMPLXLEN-CMPLXLEN-1 : i*2*CMPLXLEN];
			assign outdata_array[i][1] = outdata[(i+1)*2*CMPLXLEN-1 : (i+1)*2*CMPLXLEN-CMPLXLEN];
		end
	endgenerate

	reg [4-1 : 0] _cntout_;
	always @(posedge clk or negedge rstn) begin
		if(~rstn) begin
			_cntout_ <= 1'b0;
		end
		else if(outvalid) begin
			_cntout_ <= _cntout_ + 1;
			$display("Output: %x", outdata[15: 0]);
			
		end
	end
    
    
	/*-------- stop simulation --------*/
	initial begin
		wait(_cntout_ == 4'd1);
		#100 $finish;
	end
endmodule
