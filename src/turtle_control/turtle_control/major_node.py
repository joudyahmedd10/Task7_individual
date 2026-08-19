import rclpy
from rclpy import Node
from geometry_msgs.msg import Twist
import sys
import select
import termios
import tty


class TurtleControl(Node):
    def __init__(self):
        super().__init__('major_node')
        self.declare_parameter('cmd_vel_topic','/cmd_vel')
        cmd_vel_topic= self.get_parameter('cmd_vel_topic').value

        self.publisher= self.create_publisher(Twist,cmd_vel_topic,10)
        self.timer = self.create_timer(0.1,self.keyboard_callback)
        self.settings = termios.tcgetattr(sys.stdin)
        self.get_logger().info('Use W for forward,A for backward,S to turn right,D to turn left')



    

    def get_key(self):
        tty.setcbreak(sys.stdin.fileno())
        key = None
        if select.select([sys.stdin], [], [], 0)[0]:
            key = sys.stdin.read(1)

        termios.tcsetattr(
            sys.stdin,
            termios.TCSADRAIN,
            self.settings
        )

        return key
    def keyboard_callback(self):

        key = self.get_key()
   
        if key is None:
            return
  
        msg = Twist()
 
        if key.lower() == 'w':
            msg.linear.x = 2.0
            msg.angular.z = 0.0

        elif key.lower() == 'a':
            msg.linear.x = -2.0
            msg.angular.z = 0.0

        elif key.lower() == 's':
            msg.linear.x = 0.0
            msg.angular.z = 2.0

        elif key.lower() == 'd':
            msg.linear.x = 0.0
            msg.angular.z = -2.0

        else:
            return
        self.publisher.publish(msg)



def main():
    rclpy.init()
    node = TurtleControl()


    rclpy.spin(node)
    try:
        rclpy.spin(node)

    except KeyboardInterrupt:
        pass

    finally:
        termios.tcsetattr(
            sys.stdin,
            termios.TCSADRAIN,
            node.settings
        )


    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
