#!/usr/bin/env python
import sys, subprocess, os
from optparse import OptionParser
from ctypes.util import find_library

# make sure we have access to required GR python modules
try:
    from gnuradio import gr;
    import volk_modtool;
except:
    print "Can not import GNU Radio or VOLK Modtool, please ensure your environment is set up."
    sys.exit(-1);
    
# get compiler info stored at compile time
def def_vci():      # VOLK Compiler Information
    vci_path = os.path.join(volk_modtool.__path__[0], "compilerinfo.csv");
    try:
        return open(vci_path).read();
    except:
        print "You must update your VOLK version to one that includes an installed compilerinfo.csv"
        sys.exit(-1);
def def_gci():      # GNU Radio Compiler Information
    gci_path = os.path.join(gr.__path__[0], "compilerinfo.csv");
    try:
        return open(gci_path).read();
    except:
        print "You must update your GNU Radio version to one that includes an installed compilerinfo.csv"
        sys.exit(-1);

# stdout -> return (helper)
def shellexec_getout(cmd, throw_ex=True, print_live=True):
    print "shellexec_long: " + str(cmd);
    try:
        p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE);
        ln = "PH";
        out = ""
        while not (ln == ""):
            ln = p.stdout.readline().rstrip('\n');
            if print_live: print ln;
            out = out + ln;
        return out;
    except Exception, e:
        if(throw_ex):
            raise e;
        else:
            return -1;

# parse args
parser = OptionParser()
parser.add_option("-s", "--submit",
                  action="store_true", dest="submit", default=False,
                  help="submit results to stats.gnuradio.org")
parser.add_option("-v", "--volk-compiler-info",
                  action="store", dest="vci", default=def_vci(),
                  help="compiler info file for volk")
parser.add_option("-g", "--gr-compiler-info",
                  action="store", dest="gci", default=def_gci(),
                  help="compiler info file for GNU Radio")
parser.add_option("-a", "--disable-volk",
                  action="store_false", dest="dv", default=True,
                  help="disable VOLK benchmarks")
parser.add_option("-b", "--disable-waveforms",
                  action="store_false", dest="dw", default=True,
                  help="disable Waveform benchmarks")
(options, args) = parser.parse_args();

# first run volk tests
if(options.dv):
    print "executing volk_profile ..."
    perf = shellexec_getout(["volk_profile","-b","1"]);
else:
    perf = "";

# we get cpu info directly after VOLK benchmarks in the hope that the cpu clock is still maxed out
def cpuinfo():
    try:
        ci = open("/proc/cpuinfo", "r");
        return ci.read();
    except:
        print "do something else for OSX/Windows here"
        sys.exit(-1);

if(options.dw):
    print "executing GR waveform benchmarks ..."
    wfperf = "wf perf placeholder"
else:
    wfperf = "";

def kversion():
    try:
        kn = open("/proc/version", "r");
        return kn.read();
    except:
        print "do something else for OSX/Windows here"
        sys.exit(-1);

# compile results
ci = cpuinfo();
kn = kversion();
results = {"k":kn,"ci":ci, "perf":perf, "wfperf":wfperf, "vci":options.vci, "gci":options.gci};
print "testing submit placeholder: %s"%( results );

#submit performance statistics
if(options.submit):
    import urllib;
    uo = urllib.URLopener();
    uo.open("http://stats.gnuradio.org/submit",urllib.urlencode(results));




