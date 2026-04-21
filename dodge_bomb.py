import os
import sys
import random
import pygame as pg
import time


WIDTH, HEIGHT = 1100, 650
DELTA = {  #じしょ
    pg.K_UP: (0,-5),
    pg.K_DOWN: (0,+5),
    pg.K_LEFT: (-5,0),
    pg.K_RIGHT: (+5,0),
         }
os.chdir(os.path.dirname(os.path.abspath(__file__)))

tmr = 0
bb_imgs = pg.Surface((20, 20))
def init_bb_imgs() -> tuple[list[pg.Surface], list[int]]:
    for r in range(1,11):
        bb_img = pg.Surface((20*r,20*r))
        bb_imgs = pg.Surface((20, 20))
        bb_rct = bb_img,get_rect()
        pg.draw.circle(bb_img,(255, 0, 0), (10*r, 10*r), 10*r)
        bb_imgs.append(bb_img)
        bb_accs = [a for a in range(1, 11)]
        avx = vx*bb_accs[min(tmr//500, 9)]
        bb_img = bb_imgs[min(tmr//500,9)]
        bb_rct.width = bb_img.get_rect().width

def gameover(screen: pg.Surface) -> None: #ゲームオーバー画面の関数
    # bs_img = pg.display.set_mode((WIDTH, HEIGHT))
    bb = pg.Surface((WIDTH, HEIGHT))
    pg.draw.rect(bb, (0,0,0),pg.Rect(0,0,WIDTH,HEIGHT))
    bb.set_alpha(200)
    
    screen.blit(bb, [0,0])
    img = pg.image.load("fig/8.png") #画像の読み込み
    fonto = pg.font.Font(None,80)
    txt = fonto.render("game over", 
                       True,(255,255,255)) #テキストの設定
    t_rct = txt.get_rect()
    t_rct.center = WIDTH/2, HEIGHT/2 #テキストの位置決め
    screen.blit(txt,t_rct)

    img_rct = img.get_rect()
    img_rct.center = WIDTH/2+200, HEIGHT/2 #左にずらしたこうかとんの画像
    screen.blit(img,img_rct)


    img_rct.center = WIDTH/2-200, HEIGHT/2 #右にずらしたこうかとんの画像
    screen.blit(img,img_rct)
    pg.display.update()
    time.sleep(5) #五秒待機
    return


def check_bound(rct:pg.rect) -> tuple[bool, bool]:
    """
    
    """

    yoko, tate = True, True
    if rct.left < 0 or WIDTH < rct.right:
        yoko = False
    if rct.top < 0 or HEIGHT < rct.bottom:
        tate = False
    return yoko, tate

def main():
    pg.display.set_caption("逃げろ！こうかとん")
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    bg_img = pg.image.load("fig/pg_bg.jpg")    
    kk_img = pg.transform.rotozoom(pg.image.load("fig/3.png"), 0, 0.9)
    kk_rct = kk_img.get_rect()
    kk_rct.center = 300, 200

    bb_img = pg.Surface((20, 20))  # 爆弾用の空のSurfaceを作る
    pg.draw.circle(bb_img, (255, 0, 0), (10, 10), 10)  # 爆弾円を描く
    bb_img.set_colorkey((0, 0, 0))  # 爆弾の黒い部分を透過させる
    bb_rct = bb_img.get_rect()  # 爆弾Rectを取得する
    bb_rct.centerx = random.randint(0, WIDTH)  # 爆弾の初期横座標を設定する
    bb_rct.centery = random.randint(0, HEIGHT)  # 爆弾の初期縦座標を設定する
    vx, vy = +5, +5  # 爆弾の速度

    clock = pg.time.Clock()
    tmr = 0
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT: 
                return
            
        #init_bb_imgs(list, list)
            
        if kk_rct.colliderect(bb_rct): #こうかとんと爆弾の衝突判定
            gameover(screen) #ゲームオーバー関数呼び出し
            return #ゲームオーバーで強制終了
        screen.blit(bg_img, [0, 0]) 

        key_lst = pg.key.get_pressed()
        sum_mv = [0, 0]
       # if key_lst[pg.K_UP]:
        #    sum_mv[1] -= 5
        #if key_lst[pg.K_DOWN]:
         #   sum_mv[1] += 5
        #if key_lst[pg.K_LEFT]:
         #   sum_mv[0] -= 5
        #if key_lst[pg.K_RIGHT]:
         #   sum_mv[0] += 5

        for key,mv in DELTA.items():
            if key_lst[key]:
                sum_mv[0] += mv[0]
                sum_mv[1] += mv[1]

        kk_rct.move_ip(sum_mv)
        if check_bound(kk_rct) != (True,True):#戻す処理
            kk_rct.move_ip(-sum_mv[0], -sum_mv[1])

        screen.blit(kk_img, kk_rct)
        bb_rct.move_ip(vx, vy)  # 爆弾を移動させる
        yoko , tate = check_bound(bb_rct)
        if not yoko: #横方向の判定
            vx *= -1
        if not tate: #横方向の判定
            vy *= -1
            
        screen.blit(bb_img, bb_rct)  # 爆弾を表示させる
        pg.display.update()
        tmr += 1
        clock.tick(50)


if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()
