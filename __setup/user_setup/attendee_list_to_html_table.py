#!/usr/bin/env python
# encoding: utf-8

from __future__ import (absolute_import, division,
                        print_function, unicode_literals)
import os, sys, re
import logging
import argparse
import subprocess

reload(sys)
sys.setdefaultencoding('utf-8')

logging.basicConfig(stream=sys.stderr, level=logging.INFO)
logger = logging.getLogger(__name__)


apache_user_port_default = 8001
gateone_user_port_default = 9001
sftp_user_port_default = 10001

def main():

    parser = argparse.ArgumentParser(description="instantiate user spaces", formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    
    parser.add_argument("--ip_addr", type=str, required=True, nargs='+', help="IP address for server")
    parser.add_argument("--attendee_list", type=str, required=True, help="attendee list file")
    parser.add_argument("--user_id_start", type=int, default=1, help="index to start user IDs (ex. 1)")
    parser.add_argument("--apache_base_port", type=int, default=apache_user_port_default, help="base port for apache")
    parser.add_argument("--gateone_base_port", type=int, default=gateone_user_port_default, help="base port for gateone")
    parser.add_argument("--sftp_base_port", type=int, default=sftp_user_port_default, help="base port for sftp")
    
    args = parser.parse_args()
    
    apache_user_port = args.apache_base_port
    gateone_user_port = args.gateone_base_port
    sftp_user_port = args.sftp_base_port
    
    print("<html><body><h1>Trinity RNA-Seq Workshop<br>Berlin, Germany (June 12-16, 2017)</h1></body></html>")

    print("<style>\n" +
          "tr:nth-child(even) {background: #CCC}\n" +
          "tr:nth-child(odd) {background: #FFF}\n" +
          "</style>\n")
    

    print("<table shade='rows'>\n")
    print ("<tr><th>id</th><th>Attendee</th><th>SSH Terminal</th><th>Apache Viewer</th><th>sftp info</th></tr>")

    ip_addr_list = args.ip_addr
    num_ip_addr = len(ip_addr_list)

    
    attendee_list = []
    user_id = args.user_id_start
    with open(args.attendee_list) as f:
        for attendee_name in f:
            attendee_list.append(attendee_name)

    attendee_list.sort()
    num_attendees = len(attendee_list)
    students_per_ip = num_attendees / num_ip_addr

    prev_ip_bin = 0
    
    for i, attendee in enumerate(attendee_list):
        
        ip_bin = int(i / students_per_ip)
        if ip_bin != prev_ip_bin:
            # reset
            apache_user_port = apache_user_port_default
            gateone_user_port = gateone_user_port_default
            sftp_user_port = sftp_user_port_default
            prev_ip_bin = ip_bin
        
        ip_addr = ip_addr_list[ip_bin]

        attendee_name = attendee.rstrip()
        print("<tr><td>{}</td>".format(user_id) +
              "<td>{}</td>".format(attendee_name) +
              "<td><a href=\"{}\" target='_sshterm'>ssh terminal</a></td>".format(url_maker(ip_addr, gateone_user_port)) +
              "<td><a href=\"{}\" target='_apacheview'>apache</a></td>".format(url_maker(ip_addr, apache_user_port)) +
              "<td>sftp -P {} training@{}</td>".format(sftp_user_port, ip_addr) +
              "</tr>")
        
        apache_user_port += 1
        gateone_user_port += 1
        sftp_user_port += 1

        user_id += 1
    
    print("</table></body></html>")
    
    sys.exit(0)


def url_maker(ip_addr, port_num):

    return("http://" + ip_addr + ":" + str(port_num))



####################
 
if __name__ == "__main__":
    main()
