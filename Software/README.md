### cnnGen

* This project develops an automatic generation tool for CNNs running on FPGAs.
* Directory structure:
    * auto\_tool.py: the main script for code generation.
    * code/: the generated Verilog code for the FPGA and the generated Cpp for the CPU.
    * py\_dse/: python implementation of the optimized design space exploration algorithm.
    * py\_sim/: some software simulators helping with debug.
    * py\_plots/: the utility scripts for plotting the performance of generated design
    * config\_cnn/: YAML script specifying the CNN models.
    * config\_hw/: YAML script specifying the FPGA device.
    * py\_util: some python utility script used in design space exploration algorithm.
    * zython: output formatting and logging utilities

* Required modules : pyyaml, numpy
* Run: python auto\_tool.py -h for instructions
* Usage: python auto\_tool.py -n path-to-CNN-yaml -p path-to-hardware-yaml
