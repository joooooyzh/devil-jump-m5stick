# M5Stick Jump

一个适合 M5StickC / M5StickC Plus 的小屏幕跳跃游戏，玩法类似“涂鸦跳跃”：小恶魔会自动弹跳，玩家通过倾斜设备或 A/B 按键左右移动，尽量一直向上。

游戏现在带有由 imagegen 设计的 `DEVIL JUMP` 小恶魔首页、Game Over 页面、通关 SUCCESS 页面和 7 张关卡背景。关卡越高，平台越窄、平台间距越大、跳跃和横向移动节奏越快，背景也会从蓝天逐渐跳到太空。

## 硬件

- M5StickC 或 M5StickC Plus
- USB 数据线

## 编译和烧录

推荐使用 PlatformIO：

```bash
pio run -t upload
```

串口监视：

```bash
pio device monitor
```

电脑同步画面：

```bash
python3 -m http.server 8765
```

然后用 Chrome 或 Edge 打开：

```text
http://localhost:8765/mirror/
```

点击「连接 M5Stick」，选择 M5Stick 的串口即可。网页镜像和 `pio device monitor` 不能同时占用同一个串口。

## 操作

- 开机画面：按 A 或 B 开始
- 左右倾斜：移动角色
- A 键：向左微调
- B 键：向右微调
- 游戏结束后按 A 或 B 回到首页，再按 A 或 B 开始
- 通关后会显示小恶魔变天使的 SUCCESS 页面，并有撒花动画；按 A 或 B 回到首页

## 关卡

- L1：入门，平台宽，间距小
- L2：高云层，平台逐渐变窄
- L3：夕阳高度，开始更考验落点
- L4：暮色天空，间距继续变大
- L5：平流层，节奏更快
- L6：星层，平台更窄
- L7：太空，速度最快，达到约 2450 分后通关

## 文件

- `platformio.ini`：PlatformIO 工程配置
- `src/main.cpp`：游戏主程序
- `src/splash_image.h`：首页图的 RGB565 固件数据
- `src/gameover_image.h`：Game Over 图的 RGB565 固件数据
- `src/victory_image.h`：通关 SUCCESS 图的 RGB565 固件数据
- `src/level_backgrounds.h`：7 张关卡背景的 RGB565 固件数据
- `src/player_sprite.h`：游戏中跳跃小恶魔的 RGB565 透明 sprite 数据
- `mirror/index.html`：电脑端同步显示页面
- `mirror/app.js`：通过 Web Serial 接收 M5Stick 游戏状态并重绘画面
- `mirror/styles.css`：电脑端同步显示页面样式
- `assets/devil-jump-home.png`：由 imagegen 生成的 `DEVIL JUMP` 首页设计源图
- `assets/devil-jump-gameover.png`：由 imagegen 生成的小恶魔哭泣 Game Over 设计源图
- `assets/devil-jump-victory.png`：由 imagegen 生成的小恶魔变天使通关设计源图
- `assets/player-devil.png`：由 imagegen 生成的跳跃小恶魔 sprite 源图
- `assets/player-devil-clean.png`：电脑镜像页面使用的透明抠图小恶魔 sprite
- `assets/level-*.png`：由 imagegen 生成的 7 张关卡背景源图
- `assets/little-devil-splash.png`：早期小恶魔设计源图
- `tools/convert_splash.py`：把图片转换为 M5Stick 可用头文件的脚本
