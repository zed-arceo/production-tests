# Copyright (C) 2021 Analog Devices, Inc.
#
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without modification,
# are permitted provided that the following conditions are met:
#     - Redistributions of source code must retain the above copyright
#       notice, this list of conditions and the following disclaimer.
#     - Redistributions in binary form must reproduce the above copyright
#       notice, this list of conditions and the following disclaimer in
#       the documentation and/or other materials provided with the
#       distribution.
#     - Neither the name of Analog Devices, Inc. nor the names of its
#       contributors may be used to endorse or promote products derived
#       from this software without specific prior written permission.
#     - The use of this software may or may not infringe the patent rights
#       of one or more patent holders.  This license does not release you
#       from the requirement that you obtain separate licenses from these
#       patent holders to use this software.
#     - Use of the software either in source or binary form, must be run
#       on or directly connected to an Analog Devices Inc. component.
#
# THIS SOFTWARE IS PROVIDED BY ANALOG DEVICES "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES,
# INCLUDING, BUT NOT LIMITED TO, NON-INFRINGEMENT, MERCHANTABILITY AND FITNESS FOR A
# PARTICULAR PURPOSE ARE DISCLAIMED.
#
# IN NO EVENT SHALL ANALOG DEVICES BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL,
# EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, INTELLECTUAL PROPERTY
# RIGHTS, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR
# BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT,
# STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF
# THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

import sys

def main(COMPORT_number, dev_name):
    try:
        import adi
        dev_ad7746 = adi.ad7746(uri="serial:" + COMPORT_number + ",115200,8n1", device_name=dev_name)
        print("Connected with CN0552 context at %s" % (COMPORT_number))
    except:
        print("\nNo Device Found. Please make sure that your COM PORT number is correct and try again.")
        input("")
        sys.exit()

    def cap_channels(dev_channel, channel_name):
        try:
            raw_val = dev_ad7746.channel[dev_channel].raw
        except Exception as e:
            print("Device Error: " + str(e))
            sys.exit()

        try:
            scale_val = dev_ad7746.channel[dev_channel].scale
        except Exception as e:
            print("Device Error: " + str(e))
            sys.exit()

        meas_cap = float(raw_val) * float(scale_val)
        print("\tMeasured Capacitance: " + str(meas_cap) + " pF")

        # I'd set the range from 2pF to 3pF, the pin headers contribute to the measured capacitance around 0.5pF
        if (2.0 < meas_cap < 3.0):
            print("\t" + channel_name + " is GOOD!\n")
        else:
            print("\t" + channel_name + " FAILS!\n")
            failed_tests.append(channel_name + " out of range")


    input("\nStarting Production Test! Verify test jig is connected properly! Press enter to continue...")
    failed_tests = []

    # Normal Range Test
    print("\nStarting Normal Range Test...")

    # Channel 1 - CIN1(+) and EXCA pins 
    print("Channel 1")
    cap_channels("capacitance0", "Channel 1")

    # Channel 2 - CIN2(+) and EXCB pins 
    print("Channel 2")
    cap_channels("capacitance1", "Channel 2")

    # Extended Range Test
    input("Normal Range test done. Press enter to continue... \n")
    print("Starting Extended Range Test...")

    #write a value of 0x1B to register address 0x9
    try:
        reg_access = dev_ad7746._ctrl.debug_attrs["direct_reg_access"].value = "0x9 0x1B"
    except Exception as e:
        print("Device Error: " + str(e))
        sys.exit()

    input("Measure the voltage at P14 and press enter.")
    print("Please input the measured voltage:")
    x = float(input(""))
    if (1.65 <= x <= 1.75):
        print("\nExtended Range Test GOOD!\n")
    else:
        print("\nExtended Range Test Failed\n")
        failed_tests.append("Extended Range Test Failed")

    print("***Summary Result***")
    if len(failed_tests) == 0:
        print("    Board PASSES")
    else:
        print("Board Failed the following test:")
        for fails in failed_tests:
            print("- " + fails)

    input("\nThe test is done. Press enter to continue and proceed to the next board!")

if __name__ == '__main__':

    print("EVAL-CN0552-PMDZ Production Test")
    my_com = input("\nInput your device COM Port name (ex. COM5) and press enter: ")

    if len(my_com) == 0:
        print("You did not enter a valid COM Port number. Please try again.")
        sys.exit()
    else:
        try:
            COMPORT_number = my_com
            dev_name = "ad7746"
            main(COMPORT_number, dev_name)

        except Exception as e:
            print("Connection error: " + str(e))
