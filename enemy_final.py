import pygame
import math
import os
from settings import PATH, PATH2 # 引入順逆向兩種路徑

pygame.init()
ENEMY_IMAGE = pygame.image.load(os.path.join("images", "enemy.png"))
win = pygame.display.set_mode((1024, 800))
clock = pygame.time.Clock()

mode = 1  # PATH 的切換：表示當時是順向或逆向路徑
num_backhome = 0  # 回到主堡的 enemy 數量

class Enemy:
    def __init__(self):
        self.width = 40
        self.height = 50
        self.image = pygame.transform.scale(ENEMY_IMAGE, (self.width, self.height))
        self.health = 20
        self.max_health = 40
        if mode == 1:  # 順向路徑
            self.path = PATH
        elif mode == 2:  #逆向路徑
            self.path = PATH2
        self.path_index = 0
        self.move_count = 0
        self.stride = 1
        self.x, self.y = self.path[0]


    def draw(self, win):
        # draw enemy
        win.blit(self.image, (self.x - self.width // 2, self.y - self.height // 2))
        # draw enemy health bar
        self.draw_health_bar(win)


    def draw_health_bar(self, win):  # 繪製血條，需搭配 enemy 的座標，之後才可一起移動
        pygame.draw.rect(win, (0, 255, 0), [self.x - 20, self.y - 30, self.max_health, 5])
        pygame.draw.rect(win, (255, 0, 0), [self.x, self.y - 30, self.health, 5])


    def move(self):
        # 每移動一步，座標就要往後移一個
        if self.x == self.path[self.path_index + 1][0] and self.y == self.path[self.path_index + 1][1]:
            # print(self.path_index)
            self.path_index += 1
        # 將相鄰兩點的 x,y 分別存取，以計算兩點之間的距離
        ax = self.path[self.path_index][0]
        ay = self.path[self.path_index][1]
        bx = self.path[self.path_index+1][0]
        by = self.path[self.path_index+1][1]
        distance_A_B = math.sqrt((ax - bx) ** 2 + (ay - by) ** 2) # 兩點間距離
        max_count = int(distance_A_B / self.stride)  # 計算步數

        if self.move_count < max_count:  # 走到第幾步 < 總共要走多少步
            unit_vector_x = (bx - ax) / distance_A_B
            unit_vector_y = (by - ay) / distance_A_B
            delta_x = unit_vector_x * self.stride
            delta_y = unit_vector_y * self.stride
            # update the coordinate and the counter
            if self.move_count == max_count-1:  # 當走到最後一步時
                # 直接把 enemy 指定到 b，把步數歸零
                self.x = bx
                self.y = by
                self.move_count = 0
            else:  # 不是最後一步，繼續向前移動
                self.x += delta_x
                self.y += delta_y
                self.move_count += 1
            # print(self.move_count, max_count, self.x, self.y)

class EnemyGroup:
    def __init__(self):
        self.gen_count = 120
        self.gen_period = 120   # (unit: frame)
        self.reserved_members = [] # 有幾隻預備出來的 enemy
        self.expedition = []  # don't change this line until you do the EX.3 # 出來幾隻 enemy
        # self.expedition = [Enemy()]  # don't change this line until you do the EX.3 (初始值)

    def campaign(self):
        """
        Send an enemy to go on an expedition once 120 frame
        """
        # print(self.gen_count)
        if self.reserved_members and self.gen_count == self.gen_period: # 判斷預備的 enemy 有沒有人 & 幀數 = 120
            self.expedition.append(self.reserved_members.pop()) # 把人補向前，即將出場
            self.gen_count = 0  # 幀數歸零

        self.gen_count += 1  # 每次迴圈幀數 + 1
        if self.gen_count > 120:  # 超過 120 就歸零計算
            self.gen_count = 0

    def generate(self, num):  # 產生預備出來的 enemy
        """
        Generate the enemies in this wave
        """
        for i in range(num):
            self.reserved_members.append(Enemy())
        self.gen_count = 120  # 每 120 enemy 就會出來一次，所以讓 enemy 馬上出來

    def get(self):
        """
        Get the enemy list
        """
        return self.expedition

    def is_empty(self):
        """
        Return whether the enemy is empty (so that we can move on to next wave)
        """
        return False if self.reserved_members else True

    def retreat(self, enemy):  # 移除抵達的 enemy，並切換 PATH mode
        """
        Remove the enemy from the expedition
        :param enemy: class Enemy()
        :return: None
        """
        self.expedition.remove(enemy)  # 把到達主堡的 enemy 消滅
        global num_backhome, mode  # 宣告變數：回到主堡的 enemy 數；
        num_backhome += 1      # 當有一個 enemy 回主堡時觸發
        if num_backhome == 3:  # 當三個 enemy 都回主堡
            if mode == 1:      # 若當時是 PATH，則換到 PATH2，反之亦然
                mode = 2
            elif mode == 2:
                mode = 1
            num_backhome = 0   # 回到主堡的 enemy 數量歸零





pygame.quit()  # 結束遊戲



