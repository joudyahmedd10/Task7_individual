import rclpy
from rclpy import Node
from geometry_msgs.msg import Twist
from turtlesim.msg import Color
from std_msgs.msg import String
import sys
import select
import termios
import tty


class TurtleControl(Node):
    def __init__(self):
        super().__init__('major_node')
        #declaring the values so its not hard coded 
        self.declare_parameter('cmd_vel_topic','/cmd_vel')
        cmd_vel_topic= self.get_parameter('cmd_vel_topic').value
        self.declare_parameter('color_sensor_topic','/turtle1/color_sensor')
        color_sensor_topic = self.get_parameter('color_sensor_topic').value
        self.declare_parameter('dominant_color_topic','/dominant_color')
        dominant_color_topic = self.get_parameter('dominant_color_topic').value

        self.publisher= self.create_publisher(Twist,cmd_vel_topic,10) #puplishing velocity topic
        self.timer = self.create_timer(0.1,self.keyboard_callback)
        self.settings = termios.tcgetattr(sys.stdin)
        self.get_logger().info('Use W for forward,A for backward,S to turn right,D to turn left')
    #subscriping to color sensor
        self.subscription = self.create_subscription( Color, color_sensor_topic, self.color_callback, 10)
    # publishing the dominant colour to another topic
        self.color_publisher = self.create_publisher(String,dominant_color_topic,10)


    

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
