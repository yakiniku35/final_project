import math  # 导入数学模块
import random  # 导入随机模块
import time  # 导入时间模块
import pygame  # 导入pygame模块
pygame.init()  # 初始化pygame库

# 游戏窗口宽度和高度
WIDTH, HEIGHT = 800, 600

# 创建游戏窗口
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Aim Trainer")  # 设置窗口标题

# 目标增加的时间间隔
TARGET_INCREMENT = 400
TARGET_EVENT = pygame.USEREVENT  # 自定义事件用于生成目标

# 目标的内边距
TARGET_PADDING = 30

# 背景颜色
BG_COLOR = (0, 25, 40)
# 颜色定义
orange = (255, 140, 0)
red = (255, 0, 0)
LIVES = 3  # 初始生命值
TOP_BAR_HEIGHT = 50  # 顶部栏的高度

# 字体设置
LABEL_FONT = pygame.font.SysFont("comicsans", 24)

# 重启事件定义
RESTART_EVENT = pygame.USEREVENT + 1

# 存储每种模式下的最高击中数
high_hits_easy = 0
high_hits_hard = 0

# 目标类
class Target:
    MAX_SIZE = 30  # 目标最大尺寸
    GROWTH_RATE = 0.2  # 目标生长速度
    COLOR = "red"  # 目标颜色
    SECOND_COLOR = "white"  # 第二种颜色，用于目标的多层效果

    def __init__(self, x, y):
        self.x = x  # 目标的x坐标
        self.y = y  # 目标的y坐标
        self.size = 0  # 初始目标大小为0
        self.grow = True  # 目标是否在生长

    def update(self):
        if self.size + self.GROWTH_RATE >= self.MAX_SIZE:
            self.grow = False  # 如果目标达到最大尺寸，停止生长

        if self.grow:
            self.size += self.GROWTH_RATE  # 目标继续增长
        else:
            self.size -= self.GROWTH_RATE  # 目标开始缩小

    def draw(self, win):
        # 绘制目标的多个层次的圆形
        pygame.draw.circle(win, self.COLOR, (self.x, self.y), self.size)
        pygame.draw.circle(win, self.SECOND_COLOR, (self.x, self.y), self.size * 0.8)
        pygame.draw.circle(win, self.COLOR, (self.x, self.y), self.size * 0.6)
        pygame.draw.circle(win, self.SECOND_COLOR, (self.x, self.y), self.size * 0.4)

    def collide(self, x, y):
        dis = math.sqrt((x - self.x)**2 + (y - self.y)**2)  # 计算鼠标点击位置与目标中心的距离
        return dis <= self.size  # 如果鼠标点击距离小于目标半径，表示击中

# 绘制窗口中的所有元素
def draw(win, targets):
    win.fill(BG_COLOR)  # 填充背景颜色
    for target in targets:
        target.draw(win)  # 绘制每个目标

# 格式化时间，显示为分钟:秒.毫秒
def format_time(secs):
    milli = math.floor(int(secs * 1000 % 1000) / 100)  # 获取毫秒
    seconds = int(round(secs % 60, 1))  # 获取秒数
    minutes = int(secs // 60)  # 获取分钟数
    return f"{minutes:02d}:{seconds:02d}.{milli}"  # 返回格式化的时间字符串

# 绘制顶部栏
def draw_top_bar(win, elapsed_time, targets_pressed, misses, mode):
    pygame.draw.rect(win, "grey", (0, 0, WIDTH, TOP_BAR_HEIGHT))  # 绘制顶部灰色矩形
    time_label = LABEL_FONT.render(f"Time: {format_time(elapsed_time)}", 1, "black")  # 时间标签

    speed = round(targets_pressed / elapsed_time, 1)  # 计算命中速度（命中次数/时间）
    speed_label = LABEL_FONT.render(f"Speed: {speed} t/s", 1, "black")  # 速度标签

    hits_label = LABEL_FONT.render(f"Hits: {targets_pressed}", 1, "black")  # 命中次数标签
    lives_label = LABEL_FONT.render(f"Lives: {LIVES - misses}", 1, "black")  # 剩余生命标签

    # 根据选择的模式显示最高得分
    if mode == "easy":
        high_label = LABEL_FONT.render(f"Easy Record: {high_hits_easy}", 1, "black")
    elif mode == "hard":
        high_label = LABEL_FONT.render(f"Hard Record: {high_hits_hard}", 1, "black")

    # 在屏幕上显示标签
    win.blit(time_label, (5, 5))
    win.blit(speed_label, (200, 5))
    win.blit(hits_label, (400, 5))
    win.blit(lives_label, (500, 5))
    win.blit(high_label, (WIDTH - high_label.get_width() - 10, 5))  # 显示最高得分在右侧

# 开始界面
def start_screen(win):
    global high_hits_easy, high_hits_hard  # 访问全局变量，保存最高击中数

    win.fill(BG_COLOR)  # 填充背景颜色
    title_label = LABEL_FONT.render("Aim Trainer", 1, "white")  # 游戏标题
    start_label = LABEL_FONT.render("Choose a Mode to Start", 1, "white")  # 选择模式提示
    easy_label = LABEL_FONT.render("Easy Mode", 1, "white")  # 简单模式
    hard_label = LABEL_FONT.render("Hard Mode", 1, "white")  # 难模式

    # 创建简单模式和难模式的按钮
    easy_rect = pygame.Rect(WIDTH / 2 - easy_label.get_width() / 2, 300, easy_label.get_width(), easy_label.get_height())
    hard_rect = pygame.Rect(WIDTH / 2 - hard_label.get_width() / 2, 350, hard_label.get_width(), hard_label.get_height())

    pygame.draw.rect(win, "green", easy_rect)  # 绘制绿色按钮
    pygame.draw.rect(win, "green", hard_rect)  # 绘制绿色按钮

    # 显示最高击中数
    high_hits_easy_label = LABEL_FONT.render(f"Easy Record: {high_hits_easy}", 1, "white")
    high_hits_hard_label = LABEL_FONT.render(f"Hard Record: {high_hits_hard}", 1, "white")

    # 显示游戏标题、选择模式、按钮和最高记录
    win.blit(title_label, (WIDTH / 2 - title_label.get_width() / 2, 150))
    win.blit(start_label, (WIDTH / 2 - start_label.get_width() / 2, 220))
    win.blit(easy_label, easy_rect.topleft)
    win.blit(hard_label, hard_rect.topleft)
    win.blit(high_hits_easy_label, (WIDTH / 2 - high_hits_easy_label.get_width() / 2, 400))
    win.blit(high_hits_hard_label, (WIDTH / 2 - high_hits_hard_label.get_width() / 2, 450))
    
    pygame.display.update()  # 更新显示

    mode = None  # 初始模式为空
    while mode is None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # 如果退出事件
                pygame.quit()
                quit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()  # 获取鼠标点击位置
                if easy_rect.collidepoint(mouse_pos):  # 如果点击了简单模式
                    mode = "easy"
                elif hard_rect.collidepoint(mouse_pos):  # 如果点击了难模式
                    mode = "hard"
    return mode  # 返回选择的模式

# 结束界面
def end_screen(win, elapsed_time, targets_pressed, clicks):
    win.fill(BG_COLOR)  # 填充背景颜色
    time_label = LABEL_FONT.render(f"Time: {format_time(elapsed_time)}", 1, "white")  # 时间标签

    speed = round(targets_pressed / elapsed_time, 1)  # 计算命中速度
    speed_label = LABEL_FONT.render(f"Speed: {speed} t/s", 1, "white")  # 速度标签

    hits_label = LABEL_FONT.render(f"Hits: {targets_pressed}", 1, "white")  # 命中次数标签

    accuracy = round(targets_pressed / clicks * 100, 1)  # 计算命中准确率
    accuracy_label = LABEL_FONT.render(f"Accuracy: {accuracy}%", 1, "white")  # 准确率标签

    quit_label = LABEL_FONT.render("Quit", 1, "white")  # 退出按钮标签
    homepage_label = LABEL_FONT.render("Homepage", 1, "white")  # 返回主页按钮标签

    # 创建按钮矩形
    quit_rect = pygame.Rect(WIDTH / 2 - quit_label.get_width() / 2, 420, quit_label.get_width(), quit_label.get_height())
    homepage_rect = pygame.Rect(WIDTH / 2 - homepage_label.get_width() / 2, 350, homepage_label.get_width(), homepage_label.get_height())

    pygame.draw.rect(win, "red", quit_rect)  # 绘制退出按钮
    pygame.draw.rect(win, "orange", homepage_rect)  # 绘制返回主页按钮

    # 显示各项标签
    win.blit(quit_label, quit_rect.topleft)
    win.blit(homepage_label, homepage_rect.topleft)
    win.blit(time_label, (get_middle(time_label), 70))
    win.blit(speed_label, (get_middle(speed_label), 140))
    win.blit(hits_label, (get_middle(hits_label), 210))
    win.blit(accuracy_label, (get_middle(accuracy_label), 280))

    pygame.display.update()  # 更新显示

    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if homepage_rect.collidepoint(mouse_pos):  # 如果点击了返回主页按钮
                    return "homepage"  # 返回主页
                elif quit_rect.collidepoint(mouse_pos):  # 如果点击了退出按钮
                    pygame.quit()
                    quit()
    return None  # 如果没有点击任何按钮，保持在结束界面

# 获取显示元素的水平居中位置
def get_middle(surface):
    return WIDTH / 2 - surface.get_width() / 2

# 主函数
def main():
    global LIVES, TARGET_INCREMENT, high_hits_easy, high_hits_hard  # 使用全局变量

    run = True  # 游戏是否运行的标志
    targets = []  # 存储目标的列表
    clock = pygame.time.Clock()  # 创建时钟对象

    targets_pressed = 0  # 被击中的目标数
    clicks = 0  # 点击次数
    misses = 0  # 错误次数
    start_time = time.time()  # 记录开始时间

    pygame.time.set_timer(TARGET_EVENT, TARGET_INCREMENT)  # 设置目标生成事件

    # 显示开始屏幕，选择游戏模式
    mode = start_screen(WIN)

    # 根据选择的模式调整游戏难度
    if mode == "easy":
        TARGET_INCREMENT = 300  # 简单模式目标生成速度慢
        LIVES = 10  # 更多的生命
    elif mode == "hard":
        TARGET_INCREMENT = 150  # 难模式目标生成速度快
        LIVES = 3  # 更少的生命

    while run:
        clock.tick(60)  # 设置帧率为60
        click = False
        mouse_pos = pygame.mouse.get_pos()  # 获取鼠标位置
        elapsed_time = time.time() - start_time  # 计算游戏经过的时间

        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # 如果退出游戏
                run = False
                break

            if event.type == TARGET_EVENT:  # 如果目标生成事件发生
                x = random.randint(TARGET_PADDING, WIDTH - TARGET_PADDING)  # 随机生成目标位置
                y = random.randint(TARGET_PADDING + TOP_BAR_HEIGHT, HEIGHT - TARGET_PADDING)
                target = Target(x, y)  # 创建一个目标
                targets.append(target)

            if event.type == pygame.MOUSEBUTTONDOWN:  # 如果鼠标点击事件
                click = True
                clicks += 1  # 增加点击次数

        for target in targets:
            target.update()  # 更新每个目标的大小

            if target.size <= 0:
                targets.remove(target)  # 移除已消失的目标
                misses += 1  # 错误次数加1

            if click and target.collide(*mouse_pos):  # 如果目标被点击
                targets.remove(target)  # 移除目标
                targets_pressed += 1  # 增加命中数

        # 更新当前模式下的最高得分
        if mode == "easy" and targets_pressed > high_hits_easy:
            high_hits_easy = targets_pressed
        elif mode == "hard" and targets_pressed > high_hits_hard:
            high_hits_hard = targets_pressed

        if misses >= LIVES:  # 如果错误次数大于或等于生命值
            result = end_screen(WIN, elapsed_time, targets_pressed, clicks)  # 显示结束界面
            if result == "homepage":  # 如果点击了主页按钮，重新开始
                mode = start_screen(WIN)
                if mode == "easy":
                    TARGET_INCREMENT = 500
                    LIVES = 5
                elif mode == "hard":
                    TARGET_INCREMENT = 300
                    LIVES = 1
                targets = []  # 清除现有目标
                targets_pressed = 0  # 重置命中数
                clicks = 0  # 重置点击次数
                misses = 0  # 重置错误次数
                start_time = time.time()  # 重置开始时间

        draw(WIN, targets)  # 绘制目标
        draw_top_bar(WIN, elapsed_time, targets_pressed, misses, mode)  # 绘制顶部信息栏
        pygame.display.update()  # 更新显示

# 如果本模块作为主程序运行，则执行主函数
if __name__ == "__main__":
    main()
