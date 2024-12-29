import math
import random
import time
import pygame

pygame.init()

# 設置基本的遊戲視窗
WIDTH, HEIGHT = 800, 600
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Aim Trainer")
TARGET_INCREMENT = 400  # 目標生成的時間間隔
TARGET_EVENT = pygame.USEREVENT  # 自定義事件
TARGET_PADDING = 30  # 目標生成的輪廓
BG_COLOR = (255, 255, 255)  # 背景顏色改為白色
LIVES = 3  # 初始生命值
TOP_BAR_HEIGHT = 50  # 訊息欄的高度
LABEL_FONT = pygame.font.SysFont("comicsans", 24)  # 字體
CLICK_SOUND = pygame.mixer.Sound("chatgpt做的/click.mp3")  # 音效

# 在全局範圍內添加音量變數
# VOLUME = 1.0  # 音量範圍從 0.0 到 1.0

class Target:
    MAX_SIZE = 30  # 最大大小
    GROWTH_RATE = 0.2  # 生長速度
    COLOR = "red"  # 主顏色
    SECOND_COLOR = "white"  # 輔助顏色

    def __init__(self, x, y, ttype="normal"):
        self.x = x  # x座標
        self.y = y  # y座標
        self.size = 0  # 初始大小
        self.grow = True  # 是否變大中
        self.type = ttype  # 目標類型（normal, heal, harm）
        self.hit = False  # 有沒有被打到

    def update(self):
        if self.hit:  # 如果被打到，不再更新
            return
        if self.size + self.GROWTH_RATE >= self.MAX_SIZE:
            self.grow = False  # 如果大小達到最大值，停止變大
        if self.grow:
            self.size += self.GROWTH_RATE  # 變大
        else:
            self.size -= self.GROWTH_RATE  # 縮小

    def draw(self, win):
        if self.hit:  # 如被擊中，不再繪製
            return False
        color = "green" if self.type == "heal" else "purple" if self.type == "harm" else self.COLOR
        pygame.draw.circle(win, color, (self.x, self.y), self.size)  # 繪製目標外圈
        pygame.draw.circle(win, self.SECOND_COLOR, (self.x, self.y), self.size * 0.8)  # 繪製目標內圈
        pygame.draw.circle(win, color, (self.x, self.y), self.size * 0.6)
        pygame.draw.circle(win, self.SECOND_COLOR, (self.x, self.y), self.size * 0.4)
        return True

    def collide(self, x, y):
        dis = math.sqrt((x - self.x)**2 + (y - self.y)**2)  # 計算滑鼠和目標的距離
        return dis <= self.size  # 如果距離小於目標的半徑，表示點擊了目標

    def hit_target(self):
        self.hit = True  

def draw(win, targets):
    win.fill(BG_COLOR)  # 填充背景顏色
    for target in targets[:]:
        if not target.draw(win):  # 如果目標已被擊中，刪除該目標
            targets.remove(target)

def format_time(secs):
    milli = math.floor(int(secs * 1000 % 1000) / 100)  # 獲取毫秒部分
    seconds = int(round(secs % 60, 1))  # 獲取秒部分
    minutes = int(secs // 60)  # 獲取分鐘部分
    return f"{minutes:02d}:{seconds:02d}.{milli}"

def draw_top_bar(win, elapsed_time, targets_pressed, misses, mode):
    pygame.draw.rect(win, "grey", (0, 0, WIDTH, TOP_BAR_HEIGHT))  # 繪製頂部訊息欄背景
    time_label = LABEL_FONT.render(f"Time: {format_time(elapsed_time)}", 1, "black")  # 渲染時間
    speed = round(targets_pressed / elapsed_time, 1) if elapsed_time > 0 else 0  # 計算射擊速度
    speed_label = LABEL_FONT.render(f"Speed: {speed} t/s", 1, "black")  # 渲染速度
    hits_label = LABEL_FONT.render(f"Hits: {targets_pressed}", 1, "black")  # 渲染命中次數
    lives_label = LABEL_FONT.render(f"Lives: {max(LIVES - misses, 0)}", 1, "black")  # 渲染剩餘生命

    if mode == "timer":  # 如果是倒數模式，僅顯示剩餘時間
        win.blit(time_label, (5, 5)) 
    else:
        win.blit(time_label, (5, 5))  # 繪製時間
        win.blit(speed_label, (200, 5))  # 繪製速度
        win.blit(hits_label, (450, 5))  # 繪製命中次數
        win.blit(lives_label, (650, 5))  # 繪製剩餘生命

def start_screen(win):
    global VOLUME
    win.fill(BG_COLOR)  # 填充背景顏色
    title_label = LABEL_FONT.render("Aim Trainer", 1, "white")  # 渲染標題
    start_label = LABEL_FONT.render("Choose a Mode to Start", 1, "white")  # 渲染提示信息
    easy_label = LABEL_FONT.render("Easy Mode", 1, "white")  # 渲染簡單模式
    hard_label = LABEL_FONT.render("Hard Mode", 1, "white")  # 渲染困難模式
    timer_label = LABEL_FONT.render("1 Minute Timer Mode", 1, "white")  # 渲染倒數計時模式

    # 音量調整
    # volume_label = LABEL_FONT.render(f"Volume: {int(VOLUME * 100)}%", 1, "white")  # 渲染音量
    # volume_rect = pygame.Rect(WIDTH / 2 - volume_label.get_width() / 2, 450, volume_label.get_width(), volume_label.get_height())

    # 設置按鈕區域
    easy_rect = pygame.Rect(WIDTH / 2 - easy_label.get_width() / 2, 300, easy_label.get_width(), easy_label.get_height())
    hard_rect = pygame.Rect(WIDTH / 2 - hard_label.get_width() / 2, 350, hard_label.get_width(), hard_label.get_height())
    timer_rect = pygame.Rect(WIDTH / 2 - timer_label.get_width() / 2, 400, timer_label.get_width(), timer_label.get_height())

    pygame.draw.rect(win, "green", easy_rect)  # 繪製綠色背景
    pygame.draw.rect(win, "green", hard_rect)  # 繪製綠色背景
    pygame.draw.rect(win, "green", timer_rect)  # 繪製綠色背景
    # pygame.draw.rect(win, "green", volume_rect)  # 繪製音量背景

    win.blit(title_label, (WIDTH / 2 - title_label.get_width() / 2, 150))  # 繪製標題
    win.blit(start_label, (WIDTH / 2 - start_label.get_width() / 2, 220))  # 繪製提示信息
    win.blit(easy_label, easy_rect.topleft)  # 繪製簡單模式按鈕
    win.blit(hard_label, hard_rect.topleft)  # 繪製困難模式按鈕
    win.blit(timer_label, timer_rect.topleft)  # 繪製倒數計時模式按鈕
    # win.blit(volume_label, volume_rect.topleft)  # 繪製音量顯示
    pygame.display.update()  # 更新顯示

    mode = None  # 儲存所選模式
    while mode is None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if easy_rect.collidepoint(mouse_pos):  # 點擊簡單模式按鈕
                    mode = "easy"
                elif hard_rect.collidepoint(mouse_pos):  # 點擊困難模式按鈕
                    mode = "hard"
                elif timer_rect.collidepoint(mouse_pos):  # 點擊倒數計時模式按鈕
                    mode = "timer"
        #         elif volume_rect.collidepoint(mouse_pos):  # 點擊音量調整按鈕
        #             VOLUME = (VOLUME + 0.1) % 1.1  # 增加音量，並保持在 0.0 到 1.0 之間
        #             pygame.mixer.music.set_volume(VOLUME)  # 設置音量

        # volume_label = LABEL_FONT.render(f"Volume: {int(VOLUME * 100)}%", 1, "white")  # 更新音量顯示
        # win.blit(volume_label, volume_rect.topleft)  # 繪製更新後的音量顯示
        # pygame.display.update()  # 更新顯示

    return mode

def draw_end_screen(win, elapsed_time, targets_pressed, clicks, misses, mode):
    win.fill(BG_COLOR)  # 填充背景顏色
    time_label = LABEL_FONT.render(f"Time: {format_time(elapsed_time)}", 1, "black")  # 渲染時間
    speed = round(targets_pressed / elapsed_time, 1) if elapsed_time > 0 else 0  # 計算射擊速度
    speed_label = LABEL_FONT.render(f"Speed: {speed} t/s", 1, "black")  # 渲染速度
    hits_label = LABEL_FONT.render(f"Hits: {targets_pressed}", 1, "black")  # 渲染命中次數
    accuracy = round(targets_pressed / clicks * 100, 1) if clicks > 0 else 0  # 計算準確度
    accuracy_label = LABEL_FONT.render(f"Accuracy: {accuracy}%", 1, "black")  # 渲染準確度

    win.blit(time_label, (get_middle(time_label), 100))  # 繪製時間
    win.blit(speed_label, (get_middle(speed_label), 200))  # 繪製速度
    win.blit(hits_label, (get_middle(hits_label), 300))  # 繪製命中次數
    win.blit(accuracy_label, (get_middle(accuracy_label), 400))  # 繪製準確度

    # 繪製重新開始按鈕
    restart_button = {"rect": pygame.Rect(WIDTH / 2 - 100, 500, 200, 50), "label": LABEL_FONT.render("Restart", 1, "white")}
    pygame.draw.rect(win, "green", restart_button["rect"])  # 繪製綠色背景
    win.blit(restart_button["label"], (restart_button["rect"].x + 50, restart_button["rect"].y + 10))  # 校正文字位置
    pygame.display.update()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if restart_button["rect"].collidepoint(mouse_pos):
                    main()  # 再次調用主函數開始新一局遊戲

def get_middle(surface):
    return WIDTH / 2 - surface.get_width()/2

def main():
    mode = start_screen(WIN)  # 顯示開始畫面並獲取選擇的模式
    global TARGET_INCREMENT, LIVES
    TARGET_INCREMENT = 400 if mode in ["easy", "hard"] else 1000  # 設置目標生成時間間隔
    LIVES = 5 if mode == "easy" else 3  # 設置初始生命值

    run = True
    targets = []  # 存儲當前屏幕上的目標
    clock = pygame.time.Clock()  # 遊戲時鐘

    targets_pressed = 0  # 記錄擊中目標的次數
    clicks = 0  # 記錄點擊次數
    misses = 0  # 記錄漏掉的目標次數
    start_time = time.time()  # 記錄遊戲開始時間

    countdown_time = 60  # 倒數計時模式的總時間
    remaining_time = countdown_time  # 初始化剩餘時間

    last_target_time = time.time()  # 初始化最後一次生成目標的時間

    if mode != "timer":
        pygame.time.set_timer(TARGET_EVENT, TARGET_INCREMENT)  # 設置目標生成定時器

    while run:
        clock.tick(60)  # 控制幀率
        click = False
        mouse_pos = pygame.mouse.get_pos()  # 獲取鼠標當前位置
        elapsed_time = time.time() - start_time  # 計算已用時間

        if mode == "timer":
            remaining_time = countdown_time - elapsed_time  # 倒數計算剩餘時間
            if remaining_time <= 0:  # 倒數計時結束
                run = False
                remaining_time = 0  # 確保不顯示負數時間

            # 手動生成目標
            if time.time() - last_target_time >= TARGET_INCREMENT / 1000:  # 將間隔從毫秒轉換為秒
                x = random.randint(TARGET_PADDING, WIDTH - TARGET_PADDING)
                y = random.randint(TARGET_PADDING + TOP_BAR_HEIGHT, HEIGHT - TARGET_PADDING)
                ttype = "normal"  # 倒數模式只生成普通目標
                target = Target(x, y, ttype)
                targets.append(target)
                last_target_time = time.time()  # 更新最後生成目標的時間

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break

            if event.type == TARGET_EVENT and mode != "timer":  # 生成新目標（非倒數模式）
                x = random.randint(TARGET_PADDING, WIDTH - TARGET_PADDING)
                y = random.randint(TARGET_PADDING + TOP_BAR_HEIGHT, HEIGHT - TARGET_PADDING)
                ttype = random.choices(["normal", "heal", "harm"], [0.8, 0.1, 0.1])[0]
                target = Target(x, y, ttype)
                targets.append(target)

            if event.type == pygame.MOUSEBUTTONDOWN:
                CLICK_SOUND.play()  # 播放點擊音效
                click = True
                clicks += 1

        # 更新目標並檢查是否被點擊
        for target in targets[:]:
            target.update()

            if target.size <= 0 and not target.hit:
                targets.remove(target)
                if target.type == "normal":  # 如果目標類型為normal，則漏掉目標時扣除生命值
                    misses += 1

            if click and target.collide(*mouse_pos):  # 如果點擊了目標
                target.hit_target()  # 標記目標已擊中
                if target.type == "heal":  # 如果是回血目標
                    misses = max(0, misses - 1)
                elif target.type == "harm":  # 如果是傷害目標
                    misses += 1
                targets_pressed += 1  # 增加命中目標數

        if misses >= LIVES and mode != "timer":  # 如果生命值為0，結束遊戲（非倒數模式）
            run = False

        draw(WIN, targets)  # 繪製目標

        # 倒數模式顯示剩餘時間，其他模式顯示經過時間
        time_to_display = remaining_time if mode == "timer" else elapsed_time
        draw_top_bar(WIN, time_to_display, targets_pressed, misses, mode)
  # 繪製頂部信息欄
        pygame.display.update()  # 更新顯示

    draw_end_screen(WIN, countdown_time - remaining_time if mode == "timer" else elapsed_time,
                    targets_pressed, clicks, misses, mode)  # 顯示結束畫面
    pygame.quit()  # 退遊
    
if __name__ == "__main__":
    main()  # 運行主函數
