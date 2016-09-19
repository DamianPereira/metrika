from subprocess import call

def try_setting_stable_cpufreq(self):
    # call('echo "1" | tee /sys/devices/system/cpu/intel_pstate/no_turbo', shell=True)
    # call('echo "100" | tee /sys/devices/system/cpu/intel_pstate/max_perf_pct', shell=True)
    # call('echo "100" | tee /sys/devices/system/cpu/intel_pstate/min_perf_pct', shell=True)
    pass

    # some other tools to check cpu frequency:
    # watch -n 0,3 'cat /proc/cpuinfo | grep "MHz"'

    # also check http://askubuntu.com/questions/698195/how-to-make-cpugovernor-intel-pstate-stable
