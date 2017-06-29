from math import *
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator, FormatStrFormatter

def calc_format_offset(diff, shapeOff, div):
    try:
        formatOffset = int(diff/(shapeOff/div))
    except ZeroDivisionError:
        formatOffset = 1
    if formatOffset == 0:
        formatOffset = 1
    return formatOffset

def get_divisor(diff):
    divisor = 30 + (diff / 10)
    return divisor

def on_xlimit_change_single_graph(axes):
    x_limit = axes.axes.get_xlim()
    diff = fabs(x_limit[0] - x_limit[1])
    formatOffset = int(diff/20)
    if formatOffset == 0:
        formatOffset = 1
    majorTickOffset = MultipleLocator(formatOffset)
    majorTickFormatter = FormatStrFormatter('%d')
    axes.axes.xaxis.set_major_locator(majorTickOffset)
    axes.axes.xaxis.set_major_formatter(majorTickFormatter)

def on_ylimit_change_single_graph(axes):
    y_limit = axes.axes.get_ylim()
    diff = fabs(y_limit[0] - y_limit[1])
    formatOffset = int(diff / 10)
    if formatOffset == 0:
        formatOffset = 1
    majorTickOffset = MultipleLocator(formatOffset)
    majorTickFormatter = FormatStrFormatter('%d')
    axes.axes.yaxis.set_major_locator(majorTickOffset)
    axes.axes.yaxis.set_major_formatter(majorTickFormatter)

def graph_single(dataFrameList, legendList, markerSize, graphTitle, xLabel, yLabel):
    graph = plt.figure()
    graph.suptitle(graphTitle)
    graph.canvas.set_window_title(graphTitle)

    x = range(len(dataFrameList[0]))
    listAxis = []
    for i in dataFrameList:
        listAxis.append(plt.scatter(x, i, s=markerSize))
    listAxis[0].axes.callbacks.connect('xlim_changed', on_xlimit_change_single_graph)
    listAxis[0].axes.callbacks.connect('ylim_changed', on_ylimit_change_single_graph)
    listAxis[0].axes.grid(True)

    plt.legend(tuple(listAxis), tuple(legendList), bbox_to_anchor=(1, 1), loc=2, borderaxespad=0, prop={'size':8})
    plt.xlabel(xLabel)
    plt.ylabel(yLabel)

    on_xlimit_change_single_graph(listAxis[0])
    on_ylimit_change_single_graph(listAxis[0])

    plt.show()

def on_xlimit_change_double_graph_plot1(axes):
    global splot2_connection
    x_limits = axes.axes.get_xlim()
    diff = fabs(x_limits[0] - x_limits[1])
    divisor = get_divisor(diff)
    formatOffset = calc_format_offset(diff, dataFrameLength, divisor)
    majorTickOffset = MultipleLocator(formatOffset)
    majorTickFormatter = FormatStrFormatter('%d')
    axes.axes.xaxis.set_major_locator(majorTickOffset)
    axes.axes.xaxis.set_major_formatter(majorTickFormatter)
    splot2_axes[0].axes.callbacks.disconnect(splot2_connection)
    splot2_axes[0].axes.set_xlim(axes.axes.get_xlim())
    splot2_axes[0].axes.xaxis.set_major_locator(majorTickOffset)
    splot2_axes[0].axes.xaxis.set_major_formatter(majorTickFormatter)
    splot2_connection = splot2_axes[0].axes.callbacks.connect('xlim_changed', on_xlimit_change_double_graph_plot2)

def on_xlimit_change_double_graph_plot2(axes):
    global splot1_connection
    x_limits = axes.axes.get_xlim()
    diff = fabs(x_limits[0] - x_limits[1])
    divisor = get_divisor(diff)
    formatOffset = calc_format_offset(diff, dataFrameLength, divisor)
    majorTickOffset = MultipleLocator(formatOffset)
    majorTickFormatter = FormatStrFormatter('%d')
    axes.axes.xaxis.set_major_locator(majorTickOffset)
    axes.axes.xaxis.set_major_formatter(majorTickFormatter)
    splot1_axes[0].axes.callbacks.disconnect(splot1_connection)
    splot1_axes[0].axes.set_xlim(axes.axes.get_xlim())
    splot1_axes[0].axes.xaxis.set_major_locator(majorTickOffset)
    splot1_axes[0].axes.xaxis.set_major_formatter(majorTickFormatter)
    splot1_connection = splot1_axes[0].axes.callbacks.connect('xlim_changed', on_xlimit_change_double_graph_plot1)

def on_ylimit_change_double_graph(axes):
    y_limit = axes.axes.get_ylim()
    diff = fabs(y_limit[0] - y_limit[1])
    formatOffset = int(diff / 30)
    if formatOffset == 0:
        formatOffset = 1
    majorTickOffset = MultipleLocator(formatOffset)
    majorTickFormatter = FormatStrFormatter('%d')
    axes.axes.yaxis.set_major_locator(majorTickOffset)
    axes.axes.yaxis.set_major_formatter(majorTickFormatter)


def graph_double(dataFrameList_1, dataFrameList_2, legendList_1, legendList_2, markerSize, graphTitle, xLabel_1, yLabel_1, xLabel_2, yLabel_2):
    graph = plt.figure()
    graph.suptitle(graphTitle)
    graph.canvas.set_window_title(graphTitle)
    splot1 = graph.add_subplot(2, 1, 1)
    splot2 = graph.add_subplot(2, 1, 2)

    x_splot1 = range(len(dataFrameList_1[0]))
    x_splot2 = range(len(dataFrameList_2[0]))

    global splot1_axes
    global splot2_axes
    global splot1_connection
    global splot2_connection
    global dataFrameLength

    splot1_axes = []
    splot2_axes = []

    dataFrameLength = len(dataFrameList_1[0])

    for i in dataFrameList_1:
        if len(dataFrameList_1) < 2:
            splot1_axes.append(splot1.scatter(x_splot1, i, c='r', s=markerSize))
        else:
            splot1_axes.append(splot1.scatter(x_splot1, i, s=markerSize))
    for i in dataFrameList_2:
        if len(dataFrameList_2) < 2:
            splot2_axes.append(splot2.scatter(x_splot2, i, c='b', s=markerSize))
        else:
            splot2_axes.append(splot2.scatter(x_splot2, i, s=markerSize))

    splot1_connection = splot1_axes[0].axes.callbacks.connect('xlim_changed', on_xlimit_change_double_graph_plot1)
    splot2_connection = splot2_axes[0].axes.callbacks.connect('xlim_changed', on_xlimit_change_double_graph_plot2)

    splot1_axes[0].axes.callbacks.connect('ylim_changed', on_ylimit_change_double_graph)
    splot2_axes[0].axes.callbacks.connect('ylim_changed', on_ylimit_change_double_graph)

    splot1_axes[0].axes.grid(True)
    splot2_axes[0].axes.grid(True)

    splot1.legend(tuple(splot1_axes), tuple(legendList_1), bbox_to_anchor=(1,1), loc=2, borderaxespad=0, prop={'size':8})
    splot2.legend(tuple(splot2_axes), tuple(legendList_2), bbox_to_anchor=(1,1), loc=2, borderaxespad=0, prop={'size':8})

    splot1.set_xlabel(xLabel_1)
    splot1.set_ylabel(yLabel_1)

    splot2.set_xlabel(xLabel_2)
    splot2.set_ylabel(yLabel_2)

    on_xlimit_change_double_graph_plot1(splot1_axes[0])
    on_xlimit_change_double_graph_plot2(splot2_axes[0])
    on_ylimit_change_double_graph(splot1_axes[0])
    on_ylimit_change_double_graph(splot2_axes[0])

    plt.show()
