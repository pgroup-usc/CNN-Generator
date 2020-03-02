//Instance of systolic array
`timescale 1ns/100ps
//Number of rows and column need to be same 
//to make sure the number of column in kernel is equal to number of rows in activation
//a new parameter can be added to make the matrix and vector use different parameter for row. 
module systolic_array#(
    NUM_ROW = 8,
    NUM_COL = 8,
    IN_WORD_SIZE = 32,
    OUT_WORD_SIZE = 32
)(
    clk,
    rst,

    top_inputs,
    left_inputs,

    compute_done,
    cycles_count,
    pe_register_vals
);

input clk;
input rst;

input [0: IN_WORD_SIZE-1] top_inputs;
input [0:NUM_ROW * IN_WORD_SIZE -1] left_inputs;

output reg compute_done;
output reg  [OUT_WORD_SIZE-1:0] cycles_count;
output [0 : (OUT_WORD_SIZE * NUM_ROW) -1] pe_register_vals;

wire [127:0] tie_high;
wire [127:0] tie_low;
assign tie_low = 128'b0;
assign tie_high = ~tie_low;

genvar i,j;

//assign pe_register_vals[0:15] = tie_high[15:0];
wire [0: IN_WORD_SIZE-1] imap[0:NUM_ROW-1], wmap [0:NUM_ROW-1];
reg [IN_WORD_SIZE-1:0] buffer[0:NUM_ROW-2][0:NUM_COL-1];

wire [0 : (OUT_WORD_SIZE * NUM_ROW) -1] omap;

assign pe_register_vals = omap;

//loop for left_inputs buffers
generate
  for(i =0; i< NUM_ROW-1; i= i+1)
  begin  :lbuff_row
      for( j =0; j <= i; j=j+1)
      begin  :lbuffer_col
          always@(posedge clk)
          begin
            if(rst == 1)
            begin
              buffer[i][j] <=0;

            end
            else
            begin

                if(j==0)
                  buffer[i][j] <= left_inputs[(NUM_ROW - 2 - i)*IN_WORD_SIZE +: IN_WORD_SIZE];
                else
                  buffer[i][j] <= buffer[i][j-1];
            end

          end

      end



  end
endgenerate



generate
for(i=0; i<NUM_ROW; i= i+1)
  begin : row_loop


        if(i ==0 )
        begin
          PE #(
          IN_WORD_SIZE,
          OUT_WORD_SIZE
          ) m_unit(
          clk,
          rst,
          left_inputs[(NUM_ROW-1)*IN_WORD_SIZE+: IN_WORD_SIZE],
          top_inputs[0 +: IN_WORD_SIZE],
          omap[ (i)*OUT_WORD_SIZE +: OUT_WORD_SIZE],
          imap[i],
          wmap[i]
          );
        end


        else if(i!=0)
        begin
          PE #(
          IN_WORD_SIZE,
          OUT_WORD_SIZE
          )

          m_unit(
          clk,
          rst,
          buffer[i-1][i-1],    //make this buffer
          wmap[i-1],
          omap[ (i)*OUT_WORD_SIZE +: OUT_WORD_SIZE],
          imap[i],
          wmap[i]
          );
        end




  end
endgenerate
always @(posedge clk)
begin
    if(rst==1'b1)
    begin
        compute_done <= 1'b0;
        cycles_count <= 0;


    end
    else
    begin
        
        if(cycles_count == 2*NUM_ROW -1)
        compute_done <= 1'b1;
	else
	cycles_count <=cycles_count+1;
    end
end
endmodule
