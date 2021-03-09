"""
致力于Pr提高效率操作
2021.2.19
by littlefean
"""
import keyboard
from PIL import ImageGrab
import pyautogui
import winsound


class Data:
    # 时间轴面板上方的黄线颜色
    YELLOW = (240, 240, 0)

    # 时间轴面板上方的黄线的上方一点可点击的区域
    YELLOW_HEIGHT = -1

    # V1 视频轨道像素高度
    V1HEIGHT = 10

    # 自定义快捷键
    HOTKEY = "alt+q"


def isColorSame(c1, c2):
    return c1[0] == c2[0] and c1[1] == c2[1] and c1[2] == c2[2]


def getHeight():
    """
    获取时间轴面板上方的黄线在屏幕中的y高度
    更新 Data 中 YELLOW_HEIGHT 的数值
    :return:
    """
    im = ImageGrab.grab()
    x0 = 2130 - 1920
    y0 = 538
    w = 1506
    h = 403
    for x in range(x0, x0 + w):
        for dy in range(h):
            y = y0 + h - dy
            c = im.getpixel((x, y))
            if isColorSame(c, Data.YELLOW):
                Data.YELLOW_HEIGHT = y - 15
                print(f"yellow y: {y}")
                return


def quickRemove():
    """
    删去pr中某一个视频片段的连贯操作
    :return: 无返回
    """
    # 一定要保证是在主屏幕上
    keyboard.wait(Data.HOTKEY)
    p1 = pyautogui.position()
    winsound.Beep(3000, 300)

    keyboard.wait(Data.HOTKEY)
    p2 = pyautogui.position()
    winsound.Beep(3500, 300)

    # 假设鼠标两个点都是黄线上方
    pyautogui.click(p1.x, Data.YELLOW_HEIGHT)
    pyautogui.hotkey('ctrl', 'k')
    pyautogui.click(p2.x, Data.YELLOW_HEIGHT)
    pyautogui.hotkey('ctrl', 'k')

    pyautogui.click(p1.x + int(abs(p2.x - p1.x) / 2), Data.V1HEIGHT)
    pyautogui.hotkey('backspace')
    pyautogui.click(p1.x + int(abs(p2.x - p1.x) / 2), Data.V1HEIGHT + 2)
    pyautogui.hotkey('backspace')
    pyautogui.moveTo(p1)


def main():
    hello()
    keyboard.wait(Data.HOTKEY)
    getHeight()
    v1 = pyautogui.position()
    Data.V1HEIGHT = v1.y
    winsound.Beep(2500, 100)
    winsound.Beep(2700, 100)
    winsound.Beep(3000, 100)
    while True:
        quickRemove()


def hello():
    hi = f"""
    此程序使用方法：
    初始化：
        首先打开Pr界面
        V1轨道是要剪辑的轨道
        放到V1轨道上按 {Data.HOTKEY}，（只要保证鼠标y坐标是V1轨道高度就可以）
    使用：
        鼠标放到左端点，按{Data.HOTKEY}
        再到右侧端点，按{Data.HOTKEY}
        即可立刻删除这一段
    """
    print(hi)


if __name__ == '__main__':
    """
    让用户选中一个地方
    
    获取两个点的位置
    将磁头波动的左侧位置
    ctrlK
    将磁头波动到右位置
    ctrlK
    框选中间片段
    删除
    点击中间片段（不要让蓝线接近要点击的地方）
    删除
    """
    main()
