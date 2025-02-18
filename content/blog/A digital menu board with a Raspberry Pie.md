---
title: A digital menu board with a Raspberry Pie
date: 2024-09-14T23:17:04-08:00
description: Building a digital menu board with a Raspberry Pie Zero 2 W
tags:
  - software
  - RaspberryPi
  - coffee
  - linux
  - HTML/CSS
  - systemd
categories:
  - tools
  - projects
  - linux
draft: false
---

## Overview of the project

I'm a coffee nerd. I also love to use my passions and gifts to serve people. So I was pretty stoked when, a few years ago, I had the opportunity to volunteer at the coffee shop at my church.

Recently we did a small renovation and among the changes proposed was replacing the old menu board. It was a simple piece of printed cardboard and had _very_ outdated prices; more importantly though since the coffee shop is not-for-profit, it didn't accurately reflect the cafe's updated product offerings.

I proposed creating a digital menu board so that we could update it (both the styling and the menu items) anytime we wanted.

It also helped that my day job was in the process of moving out of an office space and offered to donate this monster 75'' TV. That made the decision pretty easy for all the stakeholders and I got the :thumbsup:. 

So, the plan to was create a menu board that we could modify ad hoc. 
I _may_ have used this as an excuse to build something I'd been thinking about for a while, and  decided on a little bit of overkill. 

I waned the content to be simple HTML/CSS managed by a git repository and I also wanted to be able to update the board anytime from anywhere, so I decided to use a Raspberry Pie zero 2 w, and serve the content in a browser in Kiosk mode, and also add a VPN so that I could connect to it remotely for updates.

Here's a photo of the finished menu board on the donated TV:

![Image Description](/img/fika%20menuboard.png)

## Hardware
1. Raspberry Pie Zero 2 W (I opted to buy a CanaKit version because it comes with a case and power supply, memory card--everything you need to get rockin'. ) [Buy it on Amazon](https://www.amazon.com/gp/product/B0CT1NWTHY/ref=ppx_yo_dt_b_search_asin_title?ie=UTF8&psc=1)
2. Any TV with HDMI. I happened to use one like [this](https://www.amazon.com/hisense-fire-tv-75-inch-class-u6hf-series-qled-smart-tv/dp/B0CHJ7GQ2Q/ref=sr_1_3?crid=1S7X7VE27JG07&dib=eyJ2IjoiMSJ9.fiD9rW_Pyr5AZNAFPKzKG69L2wPQp8w5EhDl5RpzuVgW6KDBPzKoiZvkZ9lFegCsRQLiZYMN181uwmFh9ajainKKC_3SPa_bFBRFigeSWXLL7_JbZRjYvQh3Z-GcSaBJugMcsTD4wsAoRCSkkeG_x1nWJ6yG3I5ysnGIpbdJjQqWFLmJOP_y8ThYMZSxherJQBcF-tiLUa31pIm5ekougHwv_4A1tmv5rLytbInxAsyiG3CR1iK1qinzCP4znQ3mtmdVtuIonn0oZ_fc_CGMBkdp_JRyHAMBAL4Ji80Crt6F1RLmEWGIhOf2bcPb553VY9ZjBLdJOcDPeObFpEVf6kamCDqR6NM5rNCONJuhJEo.Adc4DWq_3ZewHvFgOXhVwZ4i6X9VHYdMRtlden-Qr8c&dib_tag=se&keywords=hisense+75+inch+tv&qid=1736537887&s=electronics&sprefix=hisense+75%2Celectronics%2C185&sr=1-3&ufe=app_do%3Aamzn1.fos.5998aa40-ec6f-4947-a68f-cd087fee0848)
3. HDMI cable

## Setup

### Hardware
The Raspberry Pie Zero 2 W is a great little board, but it's not really designed to run as a web server, and what's more the menu is static HTML/CSS so I decided that it didn't actually need to be served up, and that viewing it locally in a lightweight web browser would be sufficient. 

I stared with Chrome in Kiosk mode, but everything just fell on it's face, so I switched to [midori](https://astian.org/midori-browser/)which is more lightweight, and still offers a kiosk mode. So far it's been great! Feel free to comment below if you have suggestions for improvements though. 

### Menu Board code
Here's the [GitHub Repository](https://github.com/micahmount/fika-menu)

### Device configuration
- Update swap file size
    
    Using [this article](Fika%20menu%20346262f1627c45be910badba0f13f5d4.md) as a point of reference I increased the swap size to 2GB.
    
    1. edit `/etc/dphys-swapfile` . Change CONF_SWAPSIZE from 100 to 2048, save and exit the file.
    2. Setup swap with the new parameters: `sudo dphys-swapfile setup`
    3. Turn the swap on: `sudo dphys-swapfile swapon` 
    4. reboot.
- Update OS
    
    Install tmux (so that you are not blocked) and then run updates:
    
    ```bash
    sudo apt update
    sudo apt install tmux
    tmux new -s updates
    
    ```
    
    now you're in tmux.
    
    `sudo apt update && sudo apt upgrade -y`
    
    Now you can ctl + b d to disconnect, and then carry on with the other steps while the system updates in the background
- Wireguard
    - Install wireguard, if it is not already installed: 
    `sudo apt update && sudo apt install wireguard`
    - If you get an error about resolvconf not being found, then install systemd-resolved:
    `sudo apt install systemd-resolved`
    - configure wireguard. I have a profile configured on my personal server. I scp’d it over and then symlined it to the /etc/wireguard dir. e.g.:
        
        ```bash
        scp micah@rpi4:~/code/wireguard/wireguard-cli/configurations/clients/fika/wg0.conf pi@fika:~/
        
        mkdir ~/.ssh/wireguard
        
        mv ~/wg0.conf ~/.ssh/wireguard/
        
        sudo ln -s /home/pi/.ssh/wireguard/wg0.conf /etc/wireguard/
        ```
        
    - Bring up wireguard:
    `sudo wg-quick up wg0` 
- Prevent the screen from sleeping
	- Add the unclutter package
    
	    `sudo apt update && sudo apt install unclutter && sudo reboot now` 
    
	    This will install the unclutter package and reboot the system. See the ChatGPT ref for an option to immediately hide the mouse, but I didn’t think that was a requirement in this setup, so I skipped that step. 
	- Turn off screen blanking
    
	    Click on the raspberry pi logo in the top left > Preferences > Raspberry Pi Configuration > Display > Toggle Screen Blanking
- Systemd service file to automate everything at startup
    
    Created a service file in `/etc/systemd/system/fika-menu.service:
    
    ```bash
    [Unit]
    Description=Launch Web Browser at Startup
    After=network.target
    
    [Service]
    User=pi
    Environment=XAUTHORITY=/home/pi/.Xauthority
    Environment=DISPLAY=:0
    ExecStart=/usr/bin/midori -e Fullscreen '//home/pi/code/fika-menu/menu.html'
    Restart=on-failure
    
    [Install]
    WantedBy=graphical.target
    
    ```
    
    Make the file executable: `sudo chmod +x /etc/systemd/system/fika-menu.service` 
    
    Test that it works by running `sudo systemctl start fika-menu.service`. Assuming that works, you can enable the service to auto start with `sudo systemctl enable fika-menu.service`.
    
    When making changes you may need to reload the systemctl daemon: `sudo systemctl daemon-reload`.