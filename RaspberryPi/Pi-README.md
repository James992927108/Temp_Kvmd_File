### 安裝篇

-----

1. 下載 pikvm image 檔案 https://pikvm.org/download.html
    - 選擇 HDMI-to-USB
<img src="img/download-image-file.png" alt="drawing"/>

2. 下載和安裝 [balenaEtcher](https://www.balena.io/etcher)
    - 解壓縮 XXX.bz2 (v2-hdmiusb-rpi4.img.bz2)，完成後 xxx.img 為 6 GB 的映像檔案 (v2-hdmiusb-rpi4.img)
3. 啟動 balenaEtcher
    - 選 **Flash from file**，並選解壓完的 image 檔案
    <img src="img/balena-1.png" alt="drawing" height="300"/>
    - 將 SD card 透過讀卡器(套件中目前<span style="color:red">
    **無** </span>附讀卡器)插入電腦
    - **Select target** 選擇 SD card
    - 按 **Flash!**，等待完成後，Window 會自動安全移除 SD 卡
    <img src="img/balena-5.png" alt="drawing" height="300"/>

4. 將 SD card 插入到 Pi 背面的插槽
    - <img src="img/raspberry-SDcard-loacation-2.png" alt="drawing" height="300"/>

5. 將 Pi 接入電源，pikvm 預設自動 DHCP 獲得 IP 位置。
    - IP 位置需要透過 Router 上面找。註: 有許多透過網路連結方式，包括透過 OA 分享網路給 Pi的方式，但此以 router 連接為主 (以方法一為主) 
    - 方法一
    > <img src="img/method1.png" alt="drawing" height="300"/>
    - 方法二
    > <img src="img/method2.png" alt="drawing" height="300"/>

### 透過網路連接 pikvm

1. 方法一
- 進入 Router 頁面 (公司 Router 預設 ip 為 192.168.50.1 user: admin password: admin)
> <img src="img/router-web-home-page-pi-dhcp.png" alt="drawing" height="300"/>
- 從 Router 把 pikvm 的 ip 設為固定，從區域網路的 DHCP 頁面->**手動指定 IP 的 DHCP 清單**，下來選單選擇 pikvm
> <img src="img/router-fixed-dhcp.png" alt="drawing"/>
- 套用完成後，pikvm 的 ip 即為手動( Manual )
> <img src="img/router-web-home-page-manual.png" alt="drawing"/>

- 兩種登入 pikvm，以上圖為例，ip為192.168.50.168 <br/>
> web: 瀏覽器輸入 `192.168.50.168`，預設使用者帳號密碼皆為 admin <br/>
> ssh: `$ssh root@192.168.50.168`，password 為 root

- 設定通訊埠轉發清單 
> 外部網路的虛擬伺服器 -> **通訊埠轉發清單**
> <img src="img/virtual-server-transfer-port.png" alt="drawing"/>
> 假設測試網路 10.30.50.111 <br/>
> web: `https://10.30.50.111:7777` <br/>
> ssh: `$root@10.30.50.111 -p 2222`
- 設定網路來源優先權
  - 公司網路 > 測試網路 <br/>
打開網路和網際網路設定 -> 變更介面卡選項 -> 開啟連接公司網路(corpnet.asus)的內容 -> 設定ip (網際網路通訊協定第4版) -> 進階 -> 自動計量取消勾選，自定義數值
  - 設定自動計量數值，愈低代表優先權越大，若避免 build code remote sign 失敗或者無法存取 NAS 的情況發生，可以將第二網路 ( 連接 router ) 的自動計量數值設定固定大於公司網路自定義即可<br/>
<img src="img/OA-network-priority-setup.png" alt="drawing"/>

2. 方法二
- OA 端 ( Window 10 )
> 打開網路和網際網路設定 -> 變更介面卡選項 -> 開啟連接 pikvm 網路的內容 -> 設定ip (網際網路通訊協定第4版) -> 手動設定 ip 位址、子網路遮罩、預設閘道 <br/>
例如: <br/>
ip 位址: `10.10.10.10`<br/>
子網路遮罩: `255.255.255.0` <br/>
預設閘道: `10.10.10.1`<br/>
> <img src="img/OA-pikvm-ip-setup.png" alt="drawing"/>
- pikvm端 
1. pikvm 先接上螢幕，套件中有附上 micro hdmi to hdmi <br/>
2. 以 root 登入
> user: root<br/>password: root 
3. <span style="color:red">**開啟 write & read 權限**</span>
> `$rw` 即可
4. 編輯靜態 ip 位置(編輯文本套件很多以 vim 為例，慣用即可)
> `vim /etc/dhcpcd.conf` <br/>

並設定以下內容，ip 可以自行設定同一個網域，範圍 10.10.10.2:10.10.10.255，static router 與 window 端的預設閘道相同即可。
> interface eth0 <br/>
static ip_address=10.10.10.5/24 <br/>
static routers=10.10.10.1 <br/>
5. 設定外網(以 wifi 連接)，建立 netctl 設定檔案，先從 copy 預設設定檔案
> cp /etc/netctl/examples/wireless-wpa /etc/netctl/office_wifi

編輯 office_wifi 設定檔
> `$vim office_wifi` <br/>

<img src="img/pikvm-wifi-setup.png" alt="drawing"/>

關閉 pikvm 網路 interface，一般都是 wlan0 ( `ipconfig、iwconfig` 可以查詢)
> `$ip link set wlan0 down`<br/>

連接 office_wifi 設定檔
> `$netctl start office_wifi`

透過 `iwconfig` 查看 wlan0 狀態，ESSID 與 office_wifi 設定相同即設定成功<br/>
<img src="img/pikvm-wifi-success.png" alt="drawing"/>

### 系統更新
1. 以 ssh 方式並以 root 登入
2. 開啟讀寫權限
    > `$rw` 即可
3. 執行更新指令，確定 pikvm 有外網
    > `$pacman -Syu`


### 以下未完成，但 pikvm 基本遠端功能已經設定完成

-----

### 硬體連接方式

-----
- 示意圖
<img src="img/hardware-schematic.png" alt="drawing"/>

### Flashrom 流程

1. Motherboard S6 (切斷電源)
2. Pi VCC enable(連接 Pi VCC pin 與 Motherboard SPI VCC)
3. flashrom -p linux_spi:dev=/dev/spidev0.0,spispeed=10000 -V
<img src="img/flashrom-get-flash-success.png" alt="drawing"/>

4. flashrom -p linux_spi:dev=/dev/spidev0.0,spispeed=10000 -w TUF-GAMING-B460M-PLUS-ASUS-0901.bin
<img src="img/flashrom-write-bin-file-success.png" alt="drawing"/>

5.  pi VCC disable


-----
### 常用指令
* pacman -Syu  
* pacman -S flashrom  
* scp TUF-GAMING-B460M-PLUS-ASUS-0901.ROM root@192.168.50.168:~/TUF-GAMING-B460M-PLUS-ASUST-0901.ROM
* lsmod
* modprobe 
* Dmesg
* flashrom -p linux_spi:dev=/dev/spidev0.0,spispeed=10000 -V
* ping /n 100 192.168.50.168
-----
### 備忘錄

### Automate SSH login without password
1. 找到本地的 public key
2. ssh 到 server 
3. 建立 .ssh 資料夾(mkdir .ssh)
4. cd .ssh
5. 建立 authorized_keys 檔案(touch authorized_keys)
6. vim authorized_keys
7. 將本地的 public key 貼到 authorized_keys 檔案中

* pandoc --pdf-engine=xelatex -V CJKmainfont="Microsoft YaHei" README.md -o test1.pdf

flashrom [
                -h|-R|-L|-p <programmername>[:<parameters>] [-c <chipname>]
                (
                    --flash-name|--flash-size|[-E|(-r|-w|-v) <file>]
                    [(-l <layoutfile>|--ifd| --fmap|--fmap-file <file>) [-i <imagename>]...]
                    [-n] [-N] [-f]
                )
        ]
        [-V[V[V]]] [-o <logfile>]
