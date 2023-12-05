#activates the waveshare drivers
#uncomment below line if not in rc.local
#sh /home/pi/SIM7600X-4G-HAT-Demo/Raspberry/c/sim7600_4G_hat_init

#a bunch of code to remove any competing, blocking services
sudo systemctl unmask ModemManager.service
sudo systemctl disable ModemManager.service
sudo systemctl enable dhcpcd
sudo systemctl start dhcpcd


#the mumbo jumbo for free sim card and waveshare
sudo qmicli -d /dev/cdc-wdm0 --dms-set-operating-mode="online"
sudo ip link set wwan0 down
echo 'Y' | sudo tee /sys/class/net/wwan0/qmi/raw_ip
sudo ip link set wwan0 up

sudo qmicli --device=/dev/cdc-wdm0 --device-open-proxy --wds-start-network="ip-type=4, apn=free" --client-no-release-cid

sudo udhcpc -i wwan0

ip a s wwan0