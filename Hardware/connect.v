`timescale 1ns / 1ps

module connect #(
    parameter DATALEN = 16,
    parameter FFTCHNL = 8,
    parameter CIN = 2,
    parameter COUT = 2
)(
    input clk,
    input rstn,
    
    input [CIN*COUT-1:0] inkvalid,
    input [2*DATALEN*CIN*COUT-1:0] kindata,
    input [CIN-1:0] invalid,
    input [FFTCHNL*2*DATALEN*CIN-1 : 0] indata,
    
    output [COUT-1:0] outvalid,
    output [FFTCHNL*2*2*DATALEN*COUT-1 : 0] outdata
);
    localparam CMPLXLEN = 2 * DATALEN;
	wire outvalidd[CIN-1:0];
	wire [FFTCHNL*2*2*DATALEN-1 : 0] outdatawire[CIN-1:0];
	reg [FFTCHNL*2*DATALEN-1 : 0] indatawire[COUT-1:0];
    reg [2*DATALEN-1:0] array[CIN-1:0][FFTCHNL*FFTCHNL-1:0];
    reg [2*DATALEN-1:0] mult[COUT-1:0][FFTCHNL*FFTCHNL-1:0];
    reg [2*DATALEN-1:0] kernelarray[COUT-1:0][CIN-1:0][FFTCHNL*FFTCHNL-1:0];
    reg [7:0] row;
    reg [7:0] col;
    /*-------- 1D FFT along row --------*/
    reg [3:0] offset;
    reg signal;
    reg multsignal;
    reg [3:0] counter;
    reg [3:0] ioffset;
    reg [FFTCHNL*FFTCHNL-1:0] koffset;
    wire [CMPLXLEN-1 : 0] _rowout_[0:FFTCHNL-1];
    wire _rownext_;
    wire rst;
    assign  rst = ~rstn;
reg [2*DATALEN * COUT-1:0] left_inputs_wire[FFTCHNL*FFTCHNL-1:0];
reg [2*DATALEN -1:0] top_inputs_wire[FFTCHNL*FFTCHNL-1:0];
wire [0:2*DATALEN * CIN -1] pe_register_vals_wire[FFTCHNL*FFTCHNL-1:0];
wire compute_done_out[FFTCHNL*FFTCHNL-1:0];
wire [DATALEN-1:0] cycles_count_out[FFTCHNL*FFTCHNL-1:0];
reg [5:0] arraycount; 
reg [8:0] multcount;
reg memsignal;
reg [7:0] outcount;
reg ifftsignal;
genvar j,i;

generate
	for(i=0;i<CIN;i++) begin
	fft2D fft(
		.clk(clk),
		.rstn(rstn),

		.invalid(invalid[0]), .indata(indata[(i+1)*DATALEN*2*FFTCHNL-1:i*DATALEN*2*FFTCHNL]),

		.outvalidd(outvalidd[i]), .outdata(outdatawire[i])
	);
	end
endgenerate
	
	always @(posedge clk) begin
	   
	       
	   if(rstn == 0) begin
	       counter <= 0;
	       signal <= 0;
	       offset <= 0;
	       koffset <= 0;
	       multsignal <= 0;
	       row <= 0;
	       col <= 0;
	       arraycount <= 0;
	       memsignal <= 0;
	       multcount <= 0;
	       outcount <= 0;
	       ifftsignal <= 0;
	       ioffset <= 0;
	       end
	       
	   else if(outvalidd[0] == 1) begin
	       signal <= 1;
	       offset <= offset+2; 
	   end   
	   else if (signal == 1) begin
	      counter <= counter + 1;
	      offset <= offset+2; 
	      end
	   if(counter == 3) begin
	       signal <= 0;
	       counter <= 0;
	       offset <= 0;
	       multsignal <= 1;
	       end
	   if(inkvalid[0] == 1) begin
	       koffset <= koffset+1;
	       end
	    if((multsignal == 1) & (row != CIN) & (col != CIN)) begin
	       row <= row + 1;
	       col <= col + 1;
	    end
	    if(multsignal == 1) begin
	       arraycount <= arraycount + 1;
	    end
	    if(arraycount == 2*CIN + 2) begin
	       memsignal <= 1;
	       
	    end
	    if(memsignal == 1)begin
	       ifftsignal <= 1;
	       
	    end
	    if(ifftsignal == 1)begin
	       ioffset <= ioffset + 1;
	    end
        if(ioffset == 7 | ioffset == 8)begin
            //ioffset <= 0;
            ioffset <= 7;
            ifftsignal <= 0;
        end

	    
	    
     end
  
     
    generate
    for(i=0; i<COUT; i++) begin
        for(j=0; j< CIN; j++) begin
            always @(posedge clk) begin
            if(inkvalid[0] == 1) begin
                kernelarray[i][j][koffset] <= kindata[31:0];
     end           
     end
     end
     end
     endgenerate
	
	generate
	for(j=0; j<CIN ; j++) begin
	for(i=0; i<FFTCHNL ; i++) begin
	       always @(posedge clk) begin
	       if(outvalidd[j] != 0 | signal != 0) begin
	           array[j][offset*FFTCHNL+i] <= outdatawire[j][(2*i+1)*2*DATALEN-1:2*i*2*DATALEN];
	           array[j][(offset+1)*FFTCHNL+i] <= outdatawire[j][(2*i+1)*2*DATALEN+2*DATALEN-1:(2*i+1)*2*DATALEN];
	           
	end
	end       
	end
	end
	endgenerate



assign tie_low = 512'b0;
assign tie_high = ~tie_low;

genvar r, c;
generate
for (i=0; i<FFTCHNL*FFTCHNL; i++) begin
for (r=0; r<COUT; r=r+1)
begin
    always @(posedge clk)
    begin
        if(rst == 1'b1)
        begin
            left_inputs_wire[i][2*(r+1) * DATALEN -1 -: (2*DATALEN)] <= 32'd0;
        end
        else
        begin
            if ((col < CIN) & (multsignal == 1))
            begin
                left_inputs_wire[i][2*(r+1) * DATALEN -1 -: (2*DATALEN)] <= kernelarray[r][col][i];
            end
            else
            begin 
                left_inputs_wire[i][2*(r+1) * DATALEN -1 -: (2*DATALEN)] <= 32'd0;
            end
        end
    end
end



    always @(posedge clk)
    begin
        if(rst == 1'b1)
        begin
            top_inputs_wire[i][2*DATALEN-1 -: 2*DATALEN] <= 32'd0;
        end
        else
        begin
            if ((row < CIN) & (multsignal == 1))
            begin
                top_inputs_wire[i][ 2*DATALEN-1 -: 2*DATALEN] <= array[row][i];
            end
            else
            begin 
                top_inputs_wire[i][2*DATALEN-1 -: 2*DATALEN] <= 32'd0;
            end
        end
end
systolic_array #(
        .IN_WORD_SIZE(2*DATALEN),
        .OUT_WORD_SIZE(2*DATALEN),
        .NUM_ROW(CIN),
        .NUM_COL(CIN)
    ) dut(
        .clk(clk),
        .rst(rst),
        .left_inputs(left_inputs_wire[i]),
        .top_inputs(top_inputs_wire[i]),
        .compute_done(compute_done_out[i]),
        .cycles_count(cycles_count_out[i]),
        .pe_register_vals(pe_register_vals_wire[i])
    );
end



endgenerate


generate
for(i = 0; i<FFTCHNL*FFTCHNL ;i++) begin
for(j=0; j < COUT ; j++) begin
always @(posedge clk)
begin
 if(memsignal == 1) begin
 mult[j][i] <= pe_register_vals_wire[i][j*2*DATALEN:(j+1)*2*DATALEN-1];
end
end
end
end
endgenerate




generate

 
	for(i=0;i<COUT;i++) begin

	ifft2D fft(
		.clk(clk),
		.rstn(rstn),

		.invalid(ifftsignal), .indata({mult[i][ioffset*FFTCHNL+7],mult[i][ioffset*FFTCHNL+6],mult[i][ioffset*FFTCHNL+5],mult[i][ioffset*FFTCHNL+4],mult[i][ioffset*FFTCHNL+3],mult[i][ioffset*FFTCHNL+2],mult[i][ioffset*FFTCHNL+1],mult[i][ioffset*FFTCHNL+0]}),

		.outvalid(outvalid[i]), .outdata(outdata[(i+1)*FFTCHNL*DATALEN*2*2-1 -: FFTCHNL*4*DATALEN])
	);
	end
	
endgenerate
	




endmodule
