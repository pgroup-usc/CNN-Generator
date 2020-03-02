`timescale 1ns/100ps



module PE#(
          IN_WORD_SIZE  = 32,
          OUT_WORD_SIZE = 32
          )
          (clk,
          rst,
          input_imap,
          input_fmap,
          omap,
          output_imap,
          output_fmap
          );
input rst,clk;
input [IN_WORD_SIZE -1:0] input_fmap,input_imap;
output reg [OUT_WORD_SIZE -1:0] omap;
output reg [IN_WORD_SIZE -1:0] output_imap,output_fmap;
wire valid;
wire [OUT_WORD_SIZE -1:0] currentmult;
reg [OUT_WORD_SIZE-1:0] psum;


/*mlt mt(clk, 1'b1, input_imap, 
  1'b1, input_fmap, valid, currentmult);*/
/* synthesis syn_black_box black_box_pad_pin="aclk,s_axis_a_tvalid,s_axis_a_tdata[15:0],s_axis_b_tvalid,s_axis_b_tdata[15:0],m_axis_dout_tvalid,m_axis_dout_tdata[15:0]" */

always@(posedge clk)
begin
  if(rst)
  begin
    omap <=0;
    output_imap<=0;
    output_fmap<=0;
  end
  else
  begin
    
    omap[15:0] <= omap[15:0] + input_fmap[15:0]*input_imap[15:0] - input_fmap[31:16]*input_imap[31:16]; 
    omap[31:16] <= omap[31:16] + input_fmap[15:0]*input_imap[31:16] + input_fmap[31:16]*input_imap[15:0];
    //omap[15:8] <= omap[15:8] + currentmult[15:8];
    //omap[7:0] <= omap[7:0] + currentmult[7:0];

    output_imap <= input_imap;
    output_fmap <= input_fmap;
  end

end




endmodule
