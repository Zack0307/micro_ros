#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from std_msgs.msg import Float64
import sys, select, termios, tty

# 儲存終端機的原始設定，用來讀取單一按鍵
settings = termios.tcgetattr(sys.stdin)

def get_key():
    tty.setraw(sys.stdin.fileno())
    select.select([sys.stdin], [], [], 0)
    key = sys.stdin.read(1)
    termios.tcsetattr(sys.stdin, termios.TCSADRAIN, settings)
    return key

class CameraTeleop(Node):
    def __init__(self):
        super().__init__('camera_teleop')
        # 建立 Publisher，對應你剛才在 URDF 中設定的 Topic 名稱
        self.pan_pub = self.create_publisher(Float64, '/camera_pan_cmd', 10)
        self.tilt_pub = self.create_publisher(Float64, '/camera_tilt_cmd', 10)
        
        # 初始角度 (0.0 代表正前方)
        self.pan_angle = 0.0
        self.tilt_angle = 0.0
        
        # 每次按鍵轉動的角度大小 (約 5.7 度)
        self.step = 0.1 
        
        # 關節極限 (URDF 設定為 1.57，約 90 度)
        self.limit = 1.57 

    def publish_angles(self):
        pan_msg = Float64()
        pan_msg.data = self.pan_angle
        tilt_msg = Float64()
        tilt_msg.data = self.tilt_angle
        
        self.pan_pub.publish(pan_msg)
        self.tilt_pub.publish(tilt_msg)
        
        # 在終端機印出目前角度 (覆寫同一行)
        print(f"\r目前角度 -> 左右(Pan): {self.pan_angle:.2f} | 上下(Tilt): {self.tilt_angle:.2f}   ", end="")

def main(args=None):
    rclpy.init(args=args)
    node = CameraTeleop()

    print("🎥 相機雲台控制器已啟動！")
    print("---------------------------")
    print("使用以下按鍵控制相機:")
    print("   T : 向上抬頭")
    print(" A S D : 向左 / 向下 / 向右")
    print("   R : 重置回正前方 (0, 0)")
    print(" Ctrl+C : 退出程式")
    print("---------------------------")

    try:
        while True:
            key = get_key()
            if key == '\x03':  # 按下 Ctrl+C
                break
            elif key == 'a':
                node.pan_angle = min(node.pan_angle + node.step, node.limit)
            elif key == 'd':
                node.pan_angle = max(node.pan_angle - node.step, -node.limit)
            elif key == 't':
                # 注意：如果實際往上是負值，請把 + 改成 -
                node.tilt_angle = min(node.tilt_angle + node.step, node.limit)
            elif key == 's':
                node.tilt_angle = max(node.tilt_angle - node.step, -node.limit)
            elif key == 'r':
                node.pan_angle = 0.0
                node.tilt_angle = 0.0
            
            node.publish_angles()

    except Exception as e:
        print(e)
    finally:
        # 清理並關閉節點
        termios.tcsetattr(sys.stdin, termios.TCSADRAIN, settings)
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()