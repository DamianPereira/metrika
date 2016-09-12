import numpy as np
import matplotlib

matplotlib.use('PDF')

import matplotlib.pyplot as plt
from matplotlib import ticker


# This module is just a basic visualization of results. You can surely do better than this!
# Results are divided into families and groups. A group has 1 element of each family
# in order to show different families at one bench. Drawing is not done by group, but
# by family (as elements in the same family share color and shape).
# Each family is represented as a 2D matrix. One dimension are the measures, the other
# is a variable whose value changes in each group.
# The whole plot is drawn by iterating the list of families, which contain 2D matrices as data.

#   opacity = 0.4
opacity = 1
error_config = {'ecolor': 'c'}
patterns = ["//", "", "++", "\\\\", "+", "x", "o", "O", ".", "*"]

plt.style.use('ggplot')
#plt.style.use('bmh')
#plt.rcParams['font.family'] = ['Bitstream Vera Sans']
#plt.rcParams['font.sans-serif'] = ['Tahoma']
plt.rcParams['font.serif'] = 'Bitstream Vera Sans'
plt.rcParams['font.family'] = 'serif'

#plt.rcParams['font.serif'] = 'Ubuntu'
#plt.rcParams['font.monospace'] = 'Ubuntu Mono'
#plt.rcParams['font.size'] = 10
plt.rcParams['axes.facecolor'] = '#FFFFFF'
plt.rcParams['legend.edgecolor'] = 'black'
plt.rcParams['axes.labelsize'] = 10
plt.rcParams['axes.labelweight'] = 'bold'
plt.rcParams['axes.titlesize'] = 10
plt.rcParams['xtick.labelsize'] = 8
plt.rcParams['ytick.labelsize'] = 8
plt.rcParams['legend.fontsize'] = 10
plt.rcParams['figure.titlesize'] = 12

class Plotter:
    def __init__(self, configurator, label='', title=''):
        self.configurator = configurator
        self.label = label
        self.title = title

    def run_with(self, results, name, i):
        self.results = results
        self.configurator(self, name, i)

    def group_by(self, variable):
        self.group_var = variable
        results = next(iter(self.results.values()))
        index = next(iter(results.keys())).index_of(variable)
        # groups = set(map(lambda cont, _: cont[variable], results.items()))
        without = {}
        for cont, _ in results.items():
            id = list(cont.id())
            id.pop(index)
            without[cont] = tuple(id)

        ids = set(without.values())
        self.families = [Family(id) for id in ids]
        for cont, measures in results.items():
            f = next(x for x in self.families if x.id == without[cont])
            data = [m[0] for m in measures]
            f.add_data(cont, data)

    def min_max_values(self):
        min = 1000000000000
        max = -100000000000
        for f in self.families:
            for measures in f.data:
                for m in measures:
                    if m > max:
                        max = m
                    if m < min:
                        min = m

        return min, max

    def plot_boxes(self, name):
        len_t = self.total_len()
        len_f = self.len_families()
        len_g = self.len_groups()

        box_width = 1.0 / (len_f + 2)
        sep_width = box_width / (len_f - 1)
        group_width = (box_width + sep_width) * len_f

        fig, ax = plt.subplots()

        # draw boxplots
        legends = []
        for i, family in enumerate(sorted(self.families, key=lambda f: f.id)):
            color = color_number(i)
            color_dark = darken(color)

            offset = i*(box_width+sep_width)
            positions = np.arange(len_g) * group_width + offset

            values = family.data
            box = plt.boxplot(values,
                              positions=positions,
                              widths=box_width,
                              #showcaps=False,
                              #showmeans=True, meanline=True,
                              patch_artist=True)

            for line in box['medians']:
                line.set_color('#880000')  # color_number(len_g+1)) # '#AAAAAA')
                line.set_linewidth(0.8)

            for line in box['boxes']:
                line.set_facecolor(color)
                line.set_edgecolor(color_dark)
                line.set_linewidth(0.5)

            plt.setp(box['whiskers'], linewidth=0.5)
            plt.setp(box['whiskers'], linestyle='-')
            plt.setp(box['caps'], linewidth=0.5)
            # plt.setp(box['boxes'], color=colors[i])
            plt.setp(box['caps'], color=color_dark)
            plt.setp(box['whiskers'], color=color_dark)
            plt.setp(box['fliers'], markeredgecolor=color_dark, marker="+")
            plt.setp(box['fliers'], markerfacecolor=color)

            legends.append(box['boxes'][0])

        # create a legend
        labels = [str(family.name) for family in self.families]
        plt.legend(legends, labels, loc='best')

        self.setup_limits(box_width, group_width)
        self.setup_axis(ax, group_width, sep_width)

        plt.savefig(name + '.pdf')

    def plot_bars(self, name):
        len_t = self.total_len()
        len_f = self.len_families()
        len_g = self.len_groups()

        bar_width = 1.0 / (len_f + 1)

        fig, ax = plt.subplots()

        legends = []
        for i, family in enumerate(sorted(self.families, key=lambda f: f.id)):
            positions = np.arange(len_g) + bar_width * i

            values = family.data
            means = np.average(values)
            stddevs = np.std(values)

            bars = plt.bar(positions, means, bar_width,
                    alpha=opacity,
                    color=color_number(i),
                    #color='#bbbbbb',
                    ecolor='#444444',
                    linewidth=0.5,
                    #hatch=patterns[i],
                    yerr=stddevs)
                    # error_kw=error_config,
                    #label=contenders[i])

            legends.append(bars[0])

        labels = [str(family.name) for family in self.families]
        plt.legend(legends, labels, loc='best')

        self.setup_axis(ax, 1, bar_width)

        plt.savefig(name + '.pdf')

    def setup_limits(self, box_width, group_width):
        plt.xlim(xmin=-box_width, xmax=self.len_groups() * group_width + box_width)
        min_val, max_val = self.min_max_values()
        delta = max_val - min_val
        plt.ylim(ymin=0, ymax=max_val + delta * 0.05 )

    def setup_axis(self, ax, group_width, sep_width):

        # calculate x-axis labels
        family = next(iter(self.families))
        contenders = family.contenders
        labels = [c[self.group_var] for c in contenders]

        # calculate x-axis label positions
        offset = (group_width - sep_width) / 2.0
        tick_pos = np.arange(self.len_groups()) * group_width
        label_pos = tick_pos + offset

        # setup axis ticks and labels at plot
        ax.xaxis.set_ticks_position('bottom')
        ax.yaxis.set_ticks_position('left')
        ax.xaxis.set_minor_locator(ticker.FixedLocator(label_pos))  # Customize minor tick labels
        ax.xaxis.set_minor_formatter(ticker.FixedFormatter(labels))
        ax.grid(False)
        plt.xticks(tick_pos + group_width, '', ha="center")  # rotation=-45

    def len_groups(self):
        return len(next(iter(self.families)).data)

    def len_families(self):
        return len(self.families)

    def total_len(self):
        return self.len_families() * self.len_groups()


class Family:
    def __init__(self, id):
        self.id = id
        self.contenders = []
        self.data = []

    def add_data(self, contender, data):
        self.contenders.append(contender)
        self.data.append(data)

    @property
    def name(self):
        if isinstance(self.id, str):
            return self.id
        else:
            return ','.join(map(str, self.id))

    def __repr__(self):
        return self.name


# not used anymore
# colors = ['cyan', 'lightblue', 'lightgreen', 'tan', 'pink']

def color_number(i):
    return list(plt.rcParams['axes.prop_cycle'])[i]['color']


def darken(color):
    return '#%x' % ((int(color[1:], 16) & 0xfefefe) >> 1);


def lighten(color):
    return '#%x' % ((int(color[1:], 16) & 0x7f7f7f) << 1);