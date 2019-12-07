#Prerequisites for isolate module
#Isolate depends on several advanced features of the Linux kernel.
#This script will enable all required features

echo performance > /sys/devices/system/cpu/cpufreq/policy6/scaling_governor;
echo performance > /sys/devices/system/cpu/cpufreq/policy4/scaling_governor;
echo performance > /sys/devices/system/cpu/cpufreq/policy2/scaling_governor;
echo performance > /sys/devices/system/cpu/cpufreq/policy0/scaling_governor;
echo performance > /sys/devices/system/cpu/cpufreq/policy7/scaling_governor;
echo performance > /sys/devices/system/cpu/cpufreq/policy5/scaling_governor;
echo performance > /sys/devices/system/cpu/cpufreq/policy3/scaling_governor;
echo performance > /sys/devices/system/cpu/cpufreq/policy1/scaling_governor;
echo 0 > /proc/sys/kernel/randomize_va_space;
echo never > /sys/kernel/mm/transparent_hugepage/enabled;
echo never > /sys/kernel/mm/transparent_hugepage/enabled;
echo 0 > /sys/kernel/mm/transparent_hugepage/khugepaged/defrag;