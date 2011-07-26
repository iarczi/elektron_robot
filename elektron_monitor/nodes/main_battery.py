#!/usr/bin/env python

# Software License Agreement (BSD License)
#
# Copyright (c) 2011, Robot Control and Pattern Recognition Group, Warsaw University of Technology
#
# All rights reserved.
# 
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#     * Redistributions of source code must retain the above copyright
#       notice, this list of conditions and the following disclaimer.
#     * Redistributions in binary form must reproduce the above copyright
#       notice, this list of conditions and the following disclaimer in the
#       documentation and/or other materials provided with the distribution.
#     * Neither the name of the <organization> nor the
#       names of its contributors may be used to endorse or promote products
#       derived from this software without specific prior written permission.
# 
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
# ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL <COPYRIGHT HOLDER> BE LIABLE FOR ANY
# DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
# (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
# ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
# SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

import roslib
roslib.load_manifest('elektron_monitor')

import rospy

import diagnostic_msgs.msg
import serial
import math


class Battery:

    def __init__(self):
        # open serial port
        self.device = rospy.get_param('~device', '/dev/ttyUSB0')
        self.baud = rospy.get_param('~baud', 9600)
        self.ser = serial.Serial(self.device, self.baud, timeout=2)
        
        self.diag_pub = rospy.Publisher('/diagnostics', diagnostic_msgs.msg.DiagnosticArray)
        
        self.adc_factor = 9.34 / 307

    def spin(self):

        self.ser.flushInput()

        while not rospy.is_shutdown():

            # get data
            s = self.ser.read(2)
            
            #Main header
            diag = diagnostic_msgs.msg.DiagnosticArray()
            diag.header.stamp = rospy.Time.now()
    
            
            #battery info                                                                                                                              
            stat = diagnostic_msgs.msg.DiagnosticStatus()
            stat.name = "Main Battery"
            stat.level = diagnostic_msgs.msg.DiagnosticStatus.OK
            stat.message = "OK"

            # check, if it was correct line
            if (len(s) < 2):
                continue
            
            hi = ord(s[0])
            lo = ord(s[1])
            voltage = (hi*256 + lo) * self.adc_factor
            
            stat.values.append(diagnostic_msgs.msg.KeyValue("Voltage", str(voltage)))

            #append
            diag.status.append(stat)
            
            #publish
            self.diag_pub.publish(diag)



if __name__ == '__main__':
    rospy.init_node('main_battery_monitor')      
    bat = Battery()

    try:
        bat.spin()
    except rospy.ROSInterruptException: pass
    except IOError: pass
    except KeyError: pass
