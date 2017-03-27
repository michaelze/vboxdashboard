#!/usr/bin/python

import re
import time
import sys
import influxdb

regex = '^(\d{2}:\d{2}:\d{2}\.\d{3})\s+(.*?)\s+(.*?)\s+([\.0-9]+)'
pattern = re.compile(regex)

client = influxdb.InfluxDBClient('192.168.99.101', 8086, 'root', 'root', 'vbox')

def writePoint(timestamp, machine, metric, value):
    point = [
        {
            "measurement": metric,
            "tags": {
                "machine": machine
            },
            "time": time.strftime("%Y-%m-%dT") + timestamp,
            "fields": {
                "value": float(value)
            }
        }
    ]
    client.write_points(point)

def readStdIn():
    try:
        buff = ''
        while True:
            buff += sys.stdin.read(1)
            if buff.endswith('\n'):
                match = pattern.match(buff)
                if match:
                    writePoint(match.group(1), match.group(2), match.group(3), match.group(4))
                buff = ''
    except KeyboardInterrupt:
        sys.stdout.flush()
        pass

def main(argv):
    readStdIn()


if __name__ == '__main__':
        main(sys.argv[1:])

