#!/usr/bin/env python

# Software License Agreement (BSD License)
#
# Copyright (c) 2011, Willow Garage, Inc.
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
#
#  * Redistributions of source code must retain the above copyright
#    notice, this list of conditions and the following disclaimer.
#  * Redistributions in binary form must reproduce the above
#    copyright notice, this list of conditions and the following
#    disclaimer in the documentation and/or other materials provided
#    with the distribution.
#  * Neither the name of the Willow Garage nor the names of its
#    contributors may be used to endorse or promote products derived
#    from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS
# FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE
# COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT,
# INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING,
# BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
# LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN
# ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.


import roslib
roslib.load_manifest('elektron_base')
import rospy
import diagnostic_msgs.msg
import subprocess

def wifi_monitor():
    diag_pub = rospy.Publisher('/diagnostics', diagnostic_msgs.msg.DiagnosticArray)
    rospy.init_node('wifi_monitor')
    while not rospy.is_shutdown():
        
        #Main header
        diag = diagnostic_msgs.msg.DiagnosticArray()
        diag.header.stamp = rospy.Time.now()

        lines = open("/proc/net/wireless", "r").readlines()

        faces = {}
        for line in lines[2:]:
            if line.find(":") < 0: continue
            face, data = line.split(":")
            strs = data.split()
            link = float(strs[1])
            level = float(strs[2])
            noise = float(strs[3])
        
            #interface info                                                                                                                              
            stat = diagnostic_msgs.msg.DiagnosticStatus()
            stat.name = face.strip()
            stat.level = diagnostic_msgs.msg.DiagnosticStatus.OK
            stat.message = "OK"
        

            stat.values.append(diagnostic_msgs.msg.KeyValue("Quality", str(link)))
            stat.values.append(diagnostic_msgs.msg.KeyValue("Level", str(level)))
            stat.values.append(diagnostic_msgs.msg.KeyValue("Noise", str(noise)))

            #append
            diag.status.append(stat)
        
        #publish
        diag_pub.publish(diag)
        rospy.sleep(1.0)


if __name__ == '__main__':
    try:
        wifi_monitor()
    except rospy.ROSInterruptException: pass
    except IOError: pass
    except KeyError: pass