import draw.misc as misc
import PIL.Image as I
import PIL.ImageDraw as ID
import numpy as np

import pdb


def simple_plot():
    U_x = 10
    U_y = 0.5
    def func_data(_):
        return int(_.split()[2])
    f_list = [  'draw/example/plot_log/no_parallel.log',
                'draw/example/plot_log/no_spark.log',
                'draw/example/plot_log/spark_normal.log',
                'draw/example/plot_log/spark_normal_fail.log',
                'draw/example/plot_log/spark_normal_4set.log']
    p = misc.plot_dot_series.plot_curve(f_list, func_data, U_x, U_y, 'draw/example/mem_plot.png')
    p.plot()
    p.save()



if __name__ == '__main__':
    simple_plot()
