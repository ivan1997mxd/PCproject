from optparse import OptionParser
import os
import re
import json


def main():
    try:
        parser = OptionParser(usage="%prog [options]")
        reg_result = re.compile('\[(.*)\]')
        # add option
        parser.add_option("-m", "--machine", action="store", type="string", dest="machine",
                          help="the machine to be check")
        parser.add_option("-f", "--file", action="store", type="string", dest="file", help="the file with machine list")
        parser.add_option("-n", "--noah_path", action="store", type="string", dest="noah", help="the bns path or group")
        (options, args) = parser.parse_args()

        result = ""
        if options.machine:
            options.machine = options.machine.replace(".baidu.com", "")
            result = os.popen(
                "meta-query entity host " + options.machine + " -f sysSuit,memTotal,diskTotal,cpuFrequency,cpuPhysicalCores,netIdc,status -j").read()
        elif options.file:
            result = os.popen(
                "meta-query entity host -f sysSuit,memTotal,diskTotal,cpuFrequency,cpuPhysicalCores,netIdc,status -F " + options.file + " -j").read()
        elif options.noah:
            result = os.popen(
                "get_instance_by_service " + options.noah + " |meta-query entity host -f sysSuit,memTotal,diskTotal,cpuFrequency,cpuPhysicalCores,netIdc,status -F -j").read()
        else:
            return

        result = json.loads(result)
        print
        "%-*s%-*s%-*s%-*s%-*s%-*s" % (40, "Name", 10, "CPU", 10, "memery", 10, "disk", 10, "IDC", 10, "status")
        for item in result:
            if item['Values']['cpuFrequency'] != "null":
                item['Values']['cpuFrequency'] = str(float(item['Values']['cpuFrequency']) / 1000.0)[0:3]
            else:
                item['Values']['cpuFrequency'] = "0"
            item['Values']['diskTotal'] = str(float(item['Values']['diskTotal']) / 1000000000.0)[0:5]
            item['Values']['memTotal'] = str(float(item['Values']['memTotal']) / 1024 / 1000.0)[0:5]

            print
            "%-*s%-*s%-*s%-*s%-*s%-*s" % (
                40, item['Name'], 10, item['Values']['cpuFrequency'] + " x" + item['Values']['cpuPhysicalCores'], 10,
                item['Values']['memTotal'] + "G", 10, item['Values']['diskTotal'] + "T", 10, item['Values']['netIdc'],
                10,
                item['Values']['status'])
    except Exception as e:
        return


if __name__ == "__main__":
    main()
