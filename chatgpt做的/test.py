import math
import random
import time
import pygame
pygame.init()

# 游戏窗口的宽度和高度
WIDTH, HEIGHT = 800, 600

# 设置游戏窗口
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Aim Trainer")  # 游戏窗口标题

# 设置目标生成的时间间隔
TARGET_INCREMENT = 400
TARGET_EVENT = pygame.USEREVENT  # 自定义事件

TARGET_PADDING = 30  # 目标生成的边距

BG_COLOR = (0, 25, 40)  # 背景颜色
LIVES = 3  # 初始生命值
TOP_BAR_HEIGHT = 50  # 顶部信息栏的高度

LABEL_FONT = pygame.font.SysFont("comicsans", 24)  # 字体

# 加载点击音效
CLICK_SOUND = pygame.mixer.Sound("click.mp3")

# 定义目标类
class Target:
    MAX_SIZE = 30  # 目标的最大大小
    GROWTH_RATE = 0.2  # 目标的生长速度
    COLOR = "red"  # 目标的主颜色
    SECOND_COLOR = "white"  # 目标的辅助颜色

    def __init__(self, x, y, ttype="normal"):
        self.x = x  # 目标的x坐标
        self.y = y  # 目标的y坐标
        self.size = 0  # 目标的初始大小
        self.grow = True  # 目标是否在生长
        self.type = ttype  # 目标类型（normal, heal, harm）
        self.hit = False  # 用于表示目标是否已被击中

    # 更新目标的状态
    def update(self):
        if self.hit:  # 如果目标已被击中，不再更新
            return

        if self.size + self.GROWTH_RATE >= self.MAX_SIZE:
            self.grow = False  # 如果目标大小达到最大值，停止生长

        if self.grow:
            self.size += self.GROWTH_RATE  # 目标生长
        else:
            self.size -= self.GROWTH_RATE  # 目标缩小

    # 绘制目标
    def draw(self, win):
        if self.hit:  # 如果目标已被击中，不再绘制
            return False

        color = "green" if self.type == "heal" else "purple" if self.type == "harm" else self.COLOR
        pygame.draw.circle(win, color, (self.x, self.y), self.size)  # 绘制目标外圈
        pygame.draw.circle(win, self.SECOND_COLOR,
                           (self.x, self.y), self.size * 0.8)  # 绘制目标内圈
        pygame.draw.circle(win, color, (self.x, self.y), self.size * 0.6)
        pygame.draw.circle(win, self.SECOND_COLOR,
                           (self.x, self.y), self.size * 0.4)

        return True

    # 检查目标是否被点击
    def collide(self, x, y):
        dis = math.sqrt((x - self.x)**2 + (y - self.y)**2)  # 计算鼠标与目标的距离
        return dis <= self.size  # 如果距离小于目标的半径，表示点击了目标

    # 标记目标已被击中
    def hit_target(self):
        self.hit = True  # 标记为已击中

# 绘制游戏窗口内容
def draw(win, targets):
    win.fill(BG_COLOR)  # 填充背景颜色

    for target in targets[:]:
        if not target.draw(win):  # 如果目标已被击中，删除该目标
            targets.remove(target)

# 格式化时间（分钟：秒.毫秒）
def format_time(secs):
    milli = math.floor(int(secs * 1000 % 1000) / 100)  # 获取毫秒部分
    seconds = int(round(secs % 60, 1))  # 获取秒部分
    minutes = int(secs // 60)  # 获取分钟部分

    return f"{minutes:02d}:{seconds:02d}.{milli}"

# 绘制顶部信息栏
def draw_top_bar(win, elapsed_time, targets_pressed, misses):
    pygame.draw.rect(win, "grey", (0, 0, WIDTH, TOP_BAR_HEIGHT))  # 绘制顶部信息栏背景
    time_label = LABEL_FONT.render(
        f"Time: {format_time(elapsed_time)}", 1, "black")  # 渲染时间

    speed = round(targets_pressed / elapsed_time, 1) if elapsed_time > 0 else 0  # 计算射击速度
    speed_label = LABEL_FONT.render(f"Speed: {speed} t/s", 1, "black")  # 渲染速度

    hits_label = LABEL_FONT.render(f"Hits: {targets_pressed}", 1, "black")  # 渲染命中次数

    lives_label = LABEL_FONT.render(f"Lives: {LIVES - misses}", 1, "black")  # 渲染剩余生命

    win.blit(time_label, (5, 5))  # 绘制时间
    win.blit(speed_label, (200, 5))  # 绘制速度
    win.blit(hits_label, (450, 5))  # 绘制命中次数
    win.blit(lives_label, (650, 5))  # 绘制剩余生命

# 显示开始画面
def start_screen(win):
    win.fill(BG_COLOR)  # 填充背景颜色
    title_label = LABEL_FONT.render("Aim Trainer", 1, "white")  # 渲染标题
    start_label = LABEL_FONT.render("Choose a Mode to Start", 1, "white")  # 渲染提示信息
    easy_label = LABEL_FONT.render("Easy Mode", 1, "white")  # 渲染简单模式
    hard_label = LABEL_FONT.render("Hard Mode", 1, "white")  # 渲染困难模式

    # 设置按钮区域
    easy_rect = pygame.Rect(WIDTH / 2 - easy_label.get_width() / 2, 300, easy_label.get_width(), easy_label.get_height())
    hard_rect = pygame.Rect(WIDTH / 2 - hard_label.get_width() / 2, 350, hard_label.get_width(), hard_label.get_height())

    pygame.draw.rect(win, "green", easy_rect)  # 绘制绿色背景
    pygame.draw.rect(win, "green", hard_rect)  # 绘制绿色背景

    win.blit(title_label, (WIDTH / 2 - title_label.get_width() / 2, 150))  # 绘制标题
    win.blit(start_label, (WIDTH / 2 - start_label.get_width() / 2, 220))  # 绘制提示信息
    win.blit(easy_label, easy_rect.topleft)  # 绘制简单模式按钮
    win.blit(hard_label, hard_rect.topleft)  # 绘制困难模式按钮
    pygame.display.update()  # 更新显示

    mode = None  # 存储所选模式
    while mode is None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if easy_rect.collidepoint(mouse_pos):  # 点击简单模式按钮
                    mode = "easy"
                elif hard_rect.collidepoint(mouse_pos):  # 点击困难模式按钮
                    mode = "hard"
    return mode

# 显示结束画面
def draw_end_screen(win, elapsed_time, targets_pressed, clicks, restart_button):
    win.fill(BG_COLOR)  # 填充背景颜色
    time_label = LABEL_FONT.render(
        f"Time: {format_time(elapsed_time)}", 1, "white")  # 渲染时间

    speed = round(targets_pressed / elapsed_time, 1) if elapsed_time > 0 else 0  # 计算射击速度
    speed_label = LABEL_FONT.render(f"Speed: {speed} t/s", 1, "white")  # 渲染速度

    hits_label = LABEL_FONT.render(f"Hits: {targets_pressed}", 1, "white")  # 渲染命中次数

    accuracy = round(targets_pressed / clicks * 100, 1) if clicks > 0 else 0  # 计算准确度
    accuracy_label = LABEL_FONT.render(f"Accuracy: {accuracy}%", 1, "white")  # 渲染准确度

    win.blit(time_label, (get_middle(time_label), 100))  # 绘制时间
    win.blit(speed_label, (get_middle(speed_label), 200))  # 绘制速度
    win.blit(hits_label, (get_middle(hits_label), 300))  # 绘制命中次数
    win.blit(accuracy_label, (get_middle(accuracy_label), 400))  # 绘制准确度

    # 绘制重新开始按钮
    pygame.draw.rect(win, "green", restart_button["rect"])  # 绘制绿色背景
    win.blit(restart_button["label"], restart_button["rect"].topleft)
    pygame.display.update()

# 获取文本的居中位置
def get_middle(surface):
    return WIDTH / 2 - surface.get_width()/2

# 主函数
def main():
    mode = start_screen(WIN)  # 显示开始画面并获取选择的模式
    global TARGET_INCREMENT, LIVES
    TARGET_INCREMENT = 400 if mode == "easy" else 200  # 设置目标生成时间间隔
    LIVES = 5 if mode == "easy" else 3  # 设置初始生命值

    run = True
    targets = []  # 存储当前屏幕上的目标
    clock = pygame.time.Clock()  # 游戏时钟

    targets_pressed = 0  # 记录击中目标的次数
    clicks = 0  # 记录点击次数
    misses = 0  # 记录漏掉的目标次数
    start_time = time.time()  # 记录游戏开始时间

    pygame.time.set_timer(TARGET_EVENT, TARGET_INCREMENT)  # 设置目标生成定时器

    while run:
        clock.tick(60)  # 控制帧率
        click = False
        mouse_pos = pygame.mouse.get_pos()  # 获取鼠标当前位置
        elapsed_time = time.time() - start_time  # 计算已用时间

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break

            if event.type == TARGET_EVENT:  # 生成新目标
                x = random.randint(TARGET_PADDING, WIDTH - TARGET_PADDING)
                y = random.randint(TARGET_PADDING + TOP_BAR_HEIGHT, HEIGHT - TARGET_PADDING)
                ttype = random.choices(["normal", "heal", "harm"], [0.8, 0.1, 0.1])[0]
                target = Target(x, y, ttype)
                targets.append(target)

            if event.type == pygame.MOUSEBUTTONDOWN:
                CLICK_SOUND.play()  # 播放点击音效
                click = True
                clicks += 1

        # 更新目标并检查是否被点击
        for target in targets[:]:
            target.update()

            if target.size <= 0 and not target.hit:
                targets.remove(target)
                if target.type == "normal":  # 如果目标类型为normal，则漏掉目标时扣除生命
                    misses += 1

            if click and target.collide(*mouse_pos):  # 如果点击了目标
                target.hit_target()  # 标记目标已击中
                if target.type == "heal":  # 如果是回血目标
                    misses = max(0, misses - 1)
                elif target.type == "harm":  # 如果是伤害目标
                    misses += 1
                targets_pressed += 1  # 增加命中目标数

        if misses >= LIVES:  # 如果生命值为0，结束游戏
            end_screen(WIN, elapsed_time, targets_pressed, clicks)

        draw(WIN, targets)  # 绘制目标
        draw_top_bar(WIN, elapsed_time, targets_pressed, misses)  # 绘制顶部信息栏
        pygame.display.update()  # 更新显示

    pygame.quit()  # 退出游戏

if __name__ == "__main__":
    main()  # 运行主函数
