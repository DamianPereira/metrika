import numpy as np
import matplotlib

matplotlib.use('PDF')

import matplotlib.pyplot as plt


# This module is just a basic visualization of results. You can surely do better than this!
# Results are divided into families and groups. A group has 1 element of each family
# in order to visualize how different families relate. Drawing is not done by group, but
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
plt.rcParams['axes.labelsize'] = 10
plt.rcParams['axes.labelweight'] = 'bold'
plt.rcParams['axes.titlesize'] = 10
plt.rcParams['xtick.labelsize'] = 8
plt.rcParams['ytick.labelsize'] = 8
plt.rcParams['legend.fontsize'] = 10
plt.rcParams['figure.titlesize'] = 12

class Plotter:
    def __init__(self, configurator, label='a label', title='a title' ):
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
            f.data[cont] = [m[0] for m in measures]

    def plot_boxes(self, name):
        len_t = self.total_len()
        len_f = self.len_families()
        len_g = self.len_groups()

        bar_width = 1.0 / (len_f + 2)
        sep_width = bar_width / (len_f - 1)

        fig, ax = plt.subplots()
        #plt.figure()

        # draw boxplots
        legends = []
        for i, family in enumerate(sorted(self.families, key=lambda f: f.id)):
            positions = np.arange(len_g)


            values = list(family.data.values())
            # values = list(map(lambda *a: list(a), *values))
        #    plt.boxplot(list(family.data.values()), positions=positions, labels=labels, showmeans=True, meanline=True)
            box = plt.boxplot(values, 0, 'gD',
                              positions=positions+i*(bar_width+sep_width),
                              widths=bar_width,
                              patch_artist=True)

            for line in box['medians']:
                line.set_color(color_number(len_g+1)) # '#AAAAAA')

            for line in box['boxes']:
                line.set_facecolor(color_number(i))
                line.set_edgecolor('black')
                line.set_linewidth(0.5)

            plt.setp(box['whiskers'], linewidth=0.5)
            plt.setp(box['caps'], linewidth=0.5)
            # plt.setp(box['boxes'], color=colors[i])
            # plt.setp(box['whiskers'], color='black')
            plt.setp(box['fliers'], color=color_number(len_g+1), marker='+')

            legends.append(box['boxes'][0])

        # draw temporary red and blue lines and use them to create a legend
        labels = [str(family.id) for family in self.families]
        plt.legend(legends, labels, loc='best')

        # draw labels at x axis
        family = next(iter(self.families))
        contenders = family.data.keys()
        labels = [c[self.group_var] for c in contenders]
        ax.set_xticklabels(labels)
        positions = np.arange(len_g)
        plt.xticks(positions+(bar_width*len_f/2.0), labels, ha="center")  # rotation=-45
        self.do_final_step(name)

    def plot_bars(self, name):
        len_t = self.total_len()
        len_f = self.len_families()
        len_g = self.len_groups()

        bar_width = 1.0 / (len_f + 1)

        fig, ax = plt.subplots()

        legends = []
        for i, family in enumerate(sorted(self.families, key=lambda f: f.id)):
            positions = np.arange(len_g) + bar_width * i

            values = list(family.data.values())
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


        labels = [str(family.id) for family in self.families]
        plt.legend(legends, labels, loc='best')
        #legend = ax.legend(loc="upper center", bbox_to_anchor=(0.5, 1.12), ncol=len_f)
        #legend.get_title().set_fontsize('6')  # legend 'Title' fontsize
        #plt.setp(plt.gca().get_legend().get_texts(), fontsize='12')

        # draw labels at x axis
        family = next(iter(self.families))
        contenders = family.data.keys()
        labels = [c[self.group_var] for c in contenders]
        indexes = np.arange(len_g)

        plt.xticks(indexes, labels, rotation=-45, ha="center")  # rotation_mode="anchor")
        self.do_final_step(name)

    def len_groups(self):
        return len(next(iter(self.families)).data)

    def len_families(self):
        return len(self.families)

    def total_len(self):
        return self.len_families() * self.len_groups()

    def do_final_step(self, name):
        # ax.set_aspect(0.7)

        plt.xlim(xmin=-0.25, xmax=self.len_groups())
        plt.ylim(ymin=0)
        plt.xlabel(self.label)
        plt.title(self.title, y=1.12)
        plt.subplots_adjust(left=0.25, top=0.85, bottom=0.25)
        # plt.legend()
        # plt.setp(plt.gca().get_legend().get_texts(), fontsize='12')

        #plt.tight_layout()
        plt.savefig(name + '.pdf')

class Family:
    def __init__(self, id):
        self.id = id
        self.name = str(id)
        self.data = {}

# not used anymore
# colors = ['cyan', 'lightblue', 'lightgreen', 'tan', 'pink']

def color_number(i):
    return list(plt.rcParams['axes.prop_cycle'])[i]['color']