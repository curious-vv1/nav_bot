#! /usr/bin/env python3
import rclpy
from rclpy.duration import Duration
from geometry_msgs.msg import PoseStamped
from nav2_simple_commander.robot_navigator import BasicNavigator, TaskResult

def get_user_goal():
    """Prompts the user for goal coordinates."""
    try:
        x = float(input("Enter goal X coordinate: "))
        y = float(input("Enter goal Y coordinate: "))
        w = float(input("Enter orientation W (default 1.0, press Enter to skip): ") or 1.0)
        return x, y, w
    except ValueError:
        print("Invalid input! Please enter numeric values.")
        return get_user_goal()

def main():
    rclpy.init()
    navigator = BasicNavigator()

    # Set initial pose
    initial_pose = PoseStamped()
    initial_pose.header.frame_id = 'map'
    initial_pose.header.stamp = navigator.get_clock().now().to_msg()
    initial_pose.pose.position.x = 0.0
    initial_pose.pose.position.y = 0.0
    initial_pose.pose.orientation.w = 1.0
    navigator.setInitialPose(initial_pose)

    # Wait for Nav2 to become active
    navigator.waitUntilNav2Active()

    try:
        while True:
            # Get user input for goal
            x, y, w = get_user_goal()

            # Set the goal pose
            goal_pose = PoseStamped()
            goal_pose.header.frame_id = 'map'
            goal_pose.header.stamp = navigator.get_clock().now().to_msg()
            goal_pose.pose.position.x = x
            goal_pose.pose.position.y = y
            goal_pose.pose.orientation.w = w

            print(f"Navigating to X: {x}, Y: {y}, W: {w}...")
            navigator.goToPose(goal_pose)

            while not navigator.isTaskComplete():
                feedback = navigator.getFeedback()
                if feedback:
                    print(f"ETA: {Duration.from_msg(feedback.estimated_time_remaining).nanoseconds / 1e9:.0f} seconds")

            result = navigator.getResult()
            if result == TaskResult.SUCCEEDED:
                print("Goal reached! Enter a new goal.")
            elif result == TaskResult.CANCELED:
                print("Goal was canceled!")
            elif result == TaskResult.FAILED:
                print("Goal failed!")
            else:
                print("Goal has an invalid return status!")

    except KeyboardInterrupt:
        print("Navigation stopped by user.")
        navigator.lifecycleShutdown()

if __name__ == '__main__':
    main()
