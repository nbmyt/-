import pygame
import sys
import traceback
import board
import ball
import brick
import health
import reward
from pygame.locals import *

pygame.init()
pygame.mixer.init()

# 设置帧率
FPS = 60

# 初始化数据
bg_size = width, height = 860, 573
screen = pygame.display.set_mode(bg_size)
pygame.display.set_caption("打砖块")
icon = pygame.image.load("images/icon.ico")
pygame.display.set_icon(icon)
background = pygame.image.load("images/第一关.jpg").convert()
position = background.get_rect()
brick_position = [200, 10]
health_position = [573, 860]
reward_speed = [0, 2]
filename = 'map.txt'
clock = pygame.time.Clock()

# 加载背景音乐
pygame.mixer.init()
pygame.mixer.init()
ball_brick_sound= pygame.mixer.Sound("sounds/撞击砖块1.wav")
ball_board_sound = pygame.mixer.Sound("sounds/撞击挡板.wav")
ball_wall_sound = pygame.mixer.Sound("sounds/撞击墙壁.wav")

# 生成动画精灵
group_brick = pygame.sprite.Group()
group_ball = pygame.sprite.Group()
group_board = pygame.sprite.Group()
group_reward = pygame.sprite.Group()
group_healths = pygame.sprite.Group()

# 读取地图
mapFile = open(filename, 'r')
content = mapFile.readlines() + ['\r\n']
mapFile.close()


# 初始化砖块
def creat_brick():
    for lineNum in range(len(content)):
        line = content[lineNum].rstrip('\r\n')
        if 'level' in line:
            continue
        for each in line:
            bricks = brick.Brick(bg_size)
            bricks.change_position(brick_position[0], brick_position[1])
            if each == '1':
                bricks.curimage = bricks.image1
            if each == '2':
                bricks.curimage = bricks.image2
            if each == '3':
                bricks.curimage = bricks.image3
            group_brick.add(bricks)
            brick_position[0] += 16
        brick_position[0] = 200
        brick_position[1] += 16
    brick_position[1] = 20

#初始化生命值
def creat_health():
    for num in range(3):
        healths = health.Health()
        healths.change(health_position)
        group_healths.add(healths)
        health_position[1] -= 60
# 小球反弹木板方向判断
def board_collide(ball_position, board_position, ball_speed):
    # ↘方向反弹
    if ball_speed[0] > 0 and ball_speed[1] > 0:
        if ball_position[0] - (ball_position[0] + ball_position[3] - board_position[0]) == 0:
            return False
        else:
            angle = (ball_position[1] + ball_position[3] - board_position[1]) / (ball_position[0] + ball_position[3] - board_position[0])
            if angle > 1.0:
                return False
            else:
                return True
    # ↙方向反弹
    elif ball_speed[0] < 0 and ball_speed[1] > 0:
        if ball_position[0] - (board_position[0] + ball_position[2]) == 0:
            return False
        else:
            angle = (ball_position[1] + ball_position[3] - board_position[1]) / (ball_position[0] - (board_position[0] + board_position[2]))
            if angle < -1.0:
                return False
            else:
                return True
     # ↗方向反弹
    elif ball_speed[0] > 0 and ball_speed[1] < 0:
        angle = (ball_position[1] - (board_position[1] + board_position[3])) / (ball_position[0] + ball_position[3] - board_position[0])
        if angle <= -1.0:
            return False
        else:
            return True

    # ↖方向反弹
    else:
        angle = (ball_position[1] - (board_position[1] + board_position[3])) / (ball_position[0] - (board_position[0] + board_position[2]))
        if angle >= 1.0:
            return False
        else:
            return True


# 小球反弹砖块方向判断
def brick_collide(ball_position, brick_position, ball_speed):
    # ↗方向反弹
    if ball_speed[0] > 0 and ball_speed[1] < 0:
        if ball_position[0] + 17 - brick_position[0] == 0:
            angle = -1
        else:
            angle = (ball_position[1] - (brick_position[1] + 22)) / (ball_position[0] + 17 - brick_position[0])
        if angle <= -1.0:
            return False
        else:
            return True
    # ↖方向反弹
    elif ball_speed[0] < 0 and ball_speed[1] < 0:
        angle = (ball_position[1] - (brick_position[1] + 22)) / (ball_position[0] - (brick_position[0] + 45))
        if angle >= 1.0:
            return False
        else:
            return True
    # ↘方向反弹
    elif ball_speed[0] > 0 and ball_speed[1] > 0:
        if ball_position[0] + 17 - brick_position[0] == 0:
            angle = 1
        else:
            angle = (ball_position[1] + 16 - brick_position[1]) / (ball_position[0] + 17 - brick_position[0])
        if angle >= 1.0:
            return False
        else:
            return True
    # ↙方向反弹
    else:
        angle = (ball_position[1] + 15 - brick_position[1]) / (ball_position[0] - (brick_position[0] + 45))
        if angle <= -1.0:
            return False
        else:
            return True


def main():
    score = 0
    is_remove = False
    running = True
    is_invincible = False
    is_lengthenboard = False
    score_font = pygame.font.Font("font/font.ttf", 36)
    creat_brick()
    creat_health()

    # 生成动画精灵
    boards = board.Board(bg_size)  # 生成挡板
    group_board.add(boards)
    balls = ball.Ball(boards)  # 生成球
    balls.ball_speed = [0, 0]
    is_moving = False
    group_ball.add(balls)


    # 定义计时器
    INVINCIBLE_TIME = USEREVENT #24
    LENGTHENBOARD_TIME = USEREVENT + 1
    SPEEDUPBALL_TIME = USEREVENT + 2

    # 设置循环播放
#    pygame.mixer.music.play(-1)

    # 开始主循环
    while running:
        for event in pygame.event.get():
            if event.type == QUIT:
                #pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and not is_moving:
                    is_moving = True
                    balls.ball_speed = [3,-3]
            if event.type == INVINCIBLE_TIME:
                is_invincible = False
                pygame.time.set_timer(INVINCIBLE_TIME, 0)
            if event.type == LENGTHENBOARD_TIME:
                boards.change_object(boards.rect.left)
                is_lengthenboard = False
                pygame.time.set_timer(LENGTHENBOARD_TIME, 0)
            # 球速恢复
            if event.type == SPEEDUPBALL_TIME:
                for balls in group_ball:
                    if balls.ball_speed not in ([3, 3], [3, -3], [-3, 3], [-3, -3]):
                        balls.ball_speed[0] //= 2
                        balls.ball_speed[1] //= 2
                pygame.time.set_timer(SPEEDUPBALL_TIME, 0)

        screen.blit(background, (0, 0))


        # 板与加长板的互相转化
        boardSpeed = 0
        if event.type == pygame.KEYDOWN and is_moving:
            if event.key == pygame.K_LEFT:
                boardSpeed = -8 if boards.rect.left   > 0 else 0
            elif event.key == pygame.K_RIGHT:
                boardSpeed = 8 if boards.rect.right  < width else 0
            boards.rect.left += boardSpeed
            group_board.add(boards)

        if not is_lengthenboard:
            screen.blit(boards.current_image, boards.rect)
        if is_lengthenboard:
            screen.blit(boards.current_image, boards.rect)


        # 对每个小球进行碰撞检测
        for balls in group_ball:
            # 球速加倍
            if balls.is_speedupball:
                balls.ball_speed[0] *= 2
                balls.ball_speed[1] *= 2
                balls.is_speedupball = False

            # 检测球与边界的碰撞
            if balls.rect.left < 0:
                ball_wall_sound.play()
                # 碰撞后赋值为0，防止反弹后仍然碰撞从而卡在边界上
                balls.rect.left = 0
                balls.ball_speed[0] = -balls.ball_speed[0]
                balls.is_hit = False
            elif balls.rect.right > width:
                ball_wall_sound.play()
                balls.rect.right = width
                balls.ball_speed[0] = -balls.ball_speed[0]
                balls.is_hit = False
            elif balls.rect.bottom > height:
                if is_invincible:
                    balls.rect.bottom = height
                    balls.ball_speed[1] = -balls.ball_speed[1]
                    balls.is_hit = False
                elif not is_invincible:
                    group_ball.remove(balls)
                    if len(group_ball ) == 0:
                        if len(group_healths) > 1:
                            is_remove = True
                            balls = ball.Ball(boards)
                            group_ball.add(balls)
                            is_moving = False
                            balls.ball_speed = [0, 0]
                            group_board.remove(boards)
                            group_board.add(boards)
                        else:
                            sys.exit()
                #balls.rect.bottom = height
                balls.ball_speed[1] = -balls.ball_speed[1]
                balls.is_hit = False
            elif balls.rect.top < 0:
                ball_wall_sound.play()
                balls.rect.top = 0
                balls.ball_speed[1] = -balls.ball_speed[1]
                balls.is_hit = False


            # 检测球与板的碰撞
            hit_ball = pygame.sprite.spritecollide(balls, group_board, False, pygame.sprite.collide_mask)
            if hit_ball:
                # 小球反弹木板碰撞方向检测
                board_hit_top = board_collide(balls.rect, boards.rect, balls.ball_speed)
                if not balls.is_hit:
                    ball_wall_sound.play()
                    if not board_hit_top:
                        balls.ball_speed[0] = -balls.ball_speed[0]
                        balls.ball_speed[1] = -balls.ball_speed[1]
                    else:
                        balls.ball_speed[1] = -balls.ball_speed[1]
                balls.is_hit = True

            # 检测球与方块的碰撞
            hit_board = pygame.sprite.spritecollide(balls, group_brick, False, pygame.sprite.collide_mask)
            if hit_board:
                for each in hit_board:
                    brick_hit_top = brick_collide(balls.rect, each.rect, balls.ball_speed)
                    if not brick_hit_top:
                        balls.ball_speed[0] = -balls.ball_speed[0]
                    else:
                        balls.ball_speed[1] = -balls.ball_speed[1]
                    ball_brick_sound.play()
                    if each.curimage == each.image1:
                        score += 10
                        group_brick.remove(each)
                        if len(group_brick) == 0:
                            pass
                        #new_game
                    elif each.curimage == each.image2:
                        score += 20
                        each.curimage = each.image1
                    elif each.curimage == each.image3:
                        score += 30
                        each.curimage = each.image2
                rewards = reward.Reward(bg_size)
                rewards.generate_reward()
                balls.is_hit = False
                if rewards.current_image != rewards.image5:
                    rewards.rect = balls.rect
                    group_reward.add(rewards)

            # 移动小球
            balls.rect = balls.rect.move(balls.ball_speed)

            screen.blit(balls.image1, balls.rect)

        # 奖励机制
        for rewards in group_reward:
            hit_reward = pygame.sprite.spritecollide(rewards, group_board, False, pygame.sprite.collide_mask)
            if hit_reward:
                # 无敌
                if rewards.current_image == rewards.image1:
                    is_invincible = True
                    pygame.time.set_timer(INVINCIBLE_TIME, 10 * 1000)
                # 板加长(10s)
                elif rewards.current_image == rewards.image2:
                    if is_lengthenboard == False:
                        boards.change_object(boards.rect.left)
                        is_lengthenboard = True
                    pygame.time.set_timer(LENGTHENBOARD_TIME, 10 * 1000)
                # 球数+1
                elif rewards.current_image == rewards.image3:
                    balls = ball.Ball(boards)
                    group_ball.add(balls)
                # 球速度+5(10s)
                elif rewards.current_image == rewards.image4:
                    for balls in group_ball:
                        if balls.ball_speed in ([3, 3], [3, -3], [-3, 3], [-3, -3]):
                            balls.is_speedupball = True
                            pygame.time.set_timer(SPEEDUPBALL_TIME, 10 * 1000)
                group_reward.remove(rewards)
            if rewards.rect.bottom > height:
                group_reward.remove(rewards)
            screen.blit(rewards.current_image, rewards.rect)
            rewards.rect = rewards.rect.move(reward_speed)

        #画生命值
        for healths in group_healths:
            if is_remove:
                group_healths.remove(healths)
                is_remove = False
            screen.blit(healths.image, healths.rect)
        # 画砖块
        for bricks in group_brick:
            if bricks.curimage == bricks.image4:
                group_brick.remove(bricks)
            screen.blit(bricks.curimage, bricks.rect)

        # 统计得分
        score_text = score_font.render("Score : %s" % str(score), True, (255, 255, 255))
        screen.blit(score_text, (5, 530))

        pygame.display.flip()
        clock.tick(FPS)


if __name__ == "__main__":
    try:
        main()
    except SystemExit:
        pass
    except:
        traceback.print_exc()
        pygame.quit()
        input()
