import numpy as np
import matplotlib

matplotlib.use('PDF')

from matplotlib import rcParams

rcParams['font.family'] = 'Open Sans'
# rcParams['font.sans-serif'] = ['Tahoma']

import matplotlib.pyplot as plt
import copy


def plot(labels, contenders, samples_by_metric, testbed, box=False,normalize=True, normalizer=None, label='a label', title='a title'):

    number_of_groups = len(samples_by_metric)
    metrics_size = len(contenders)

    if normalize:
        plotted = []
        for metric in samples_by_metric:
            if normalizer is None:
                norm = min([np.average(samples) for samples in metric])
            else:
                norm = metric[normalizer]

            plotted.append([np.array(samples) / norm for samples in metric])
    else:
        plotted = copy.deepcopy(samples_by_metric)

    bar_width = 1 / (metrics_size + 1)
    #   opacity = 0.4
    opacity = 1
    error_config = {'ecolor': 'c'}
    patterns = ["//", "", "++", "\\\\", "+", "x", "o", "O", ".", "*"]

    # generate arrays of averages by contender
    samples_by_contender = [[] for _ in range(metrics_size)]
    for metric in plotted:
        for i, samples in enumerate(metric):
            mean = np.average(samples)
            samples_by_contender[i].append(mean)

    # calculate std deviation
    error_by_contender = [[] for _ in range(metrics_size)]
    for metric in plotted:
        for i, samples in enumerate(metric):
            if box:
                value = samples
            else:
                value = np.std(samples)
            error_by_contender[i].append(value)

    fig, ax = plt.subplots()
    indexes = np.arange(number_of_groups)

    if box:
        # draw boxplots
        for i, metric in enumerate(plotted):
            positions = range(i * metrics_size + 1, (i+1) * metrics_size + 1)
            plt.boxplot(metric, positions=positions, labels=contenders, showmeans=True, meanline=True)
        ax.set_xticklabels(labels)
        plt.xticks(range(0, len(labels) * metrics_size, metrics_size), labels, rotation=-45, ha="left")
    else:
        # draw bars
        for i, contender in enumerate(samples_by_contender):
            plt.bar(indexes + bar_width * i,  contender, bar_width,
                    alpha=opacity,
                    color='#bbbbbb',
                    # edgecolor='b',
                    linewidth=0.5,
                    hatch=patterns[i],
                    yerr=error_by_contender[i],
                    # error_kw=error_config,
                    label=contenders[i])

        legend = ax.legend(loc="upper center", bbox_to_anchor=(0.5, 1.12), ncol=metrics_size)
        legend.get_title().set_fontsize('6')  # legend 'Title' fontsize
        plt.setp(plt.gca().get_legend().get_texts(), fontsize='12')
        plt.xticks(indexes, labels, rotation=-45, ha="left")  # rotation_mode="anchor")
    #ax.set_aspect(0.7)

    plt.xlim(xmin=0)
    plt.xlabel(label)
    plt.title(title, y=1.12)
    plt.subplots_adjust(left=0.25, top=0.85, bottom=0.25)
    # plt.legend()
    # plt.setp(plt.gca().get_legend().get_texts(), fontsize='12')

    # plt.tight_layout()
    plt.savefig(testbed)
