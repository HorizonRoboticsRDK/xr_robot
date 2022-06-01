from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    return LaunchDescription([
        # 启动图片发布pkg
        # F37 mipi cam
        # Node(
        #     package='mipi_cam',
        #     executable='mipi_cam',
        #     output='screen',
        #     parameters=[
        #         {"out_format": "nv12"},
        #         {"image_width": 960},
        #         {"image_height": 544},
        #         {"io_method": "shared_mem"},
        #         {"video_device": "F37"}
        #     ],
        #     arguments=['--ros-args', '--log-level', 'error']
        # ),
        # usb cam
        Node(
            package='hobot_usb_cam',
            executable='hobot_usb_cam',
            output='screen',
            parameters=[
                {"image_width": 640},
                {"image_height": 480},
                {"video_device": "/dev/video8"}
            ],
            arguments=['--ros-args', '--log-level', 'error']
        ),

        # 启动jpeg图片编码&发布pkg
        Node(
            package='hobot_codec',
            executable='hobot_codec_republish',
            output='screen',
            parameters=[
                {"channel": 1},
                {"in_mode": "ros"},
                {"in_format": "jpeg"},
                {"out_mode": "shared_mem"},
                {"out_format": "nv12"},
                {"sub_topic": "/image"},
                {"pub_topic": "/hbmem_img"}
            ],
            arguments=['--ros-args', '--log-level', 'error']
        ),
        
        # 启动单目rgb人体、人头、人脸、人手框和人体关键点检测pkg
        Node(
            package='mono2d_body_detection',
            executable='mono2d_body_detection',
            output='screen',
            parameters=[
                {"ai_msg_pub_topic_name": "/hobot_mono2d_body_detection"}
            ],
            arguments=['--ros-args', '--log-level', 'error']
        ),
        # 启动人手关键点检测pkg
        Node(
            package='hand_lmk_detection',
            executable='hand_lmk_detection',
            output='screen',
            parameters=[
                {"ai_msg_sub_topic_name": "/hobot_mono2d_body_detection"},
                {"ai_msg_pub_topic_name": "/hobot_hand_lmk_detection"}
            ],
            arguments=['--ros-args', '--log-level', 'error']
        ),
        # 启动web展示pkg
        Node(
            package='websocket',
            executable='websocket',
            output='screen',
            parameters=[
                {"image_topic": "/image"},
                {"image_type": "mjpeg"},
                {"smart_topic": "/hobot_hand_gesture_detection"}
            ],
            arguments=['--ros-args', '--log-level', 'error']
        ),
        # 启动手势识别pkg
        Node(
            package='hand_gesture_detection',
            executable='hand_gesture_detection',
            output='screen',
            parameters=[
                {"ai_msg_sub_topic_name": "/hobot_hand_lmk_detection"},
                {"ai_msg_pub_topic_name": "/hobot_hand_gesture_detection"}
            ],
            arguments=['--ros-args', '--log-level', 'error']
        ),
        # 启动手势交互pkg
        Node(
            package='body_tracking',
            executable='body_tracking',
            output='screen',
            parameters=[
                {"ai_msg_sub_topic_name": "/hobot_hand_gesture_detection"},
                {"twist_pub_topic_name": "/cmd_vel"},
                {"activate_wakeup_gesture": 0},
                {"img_width": 960},
                {"img_height": 544},
                {"track_serial_lost_num_thr": 100},
                {"move_step": 0.3},
                {"rotate_step": 0.5},
                {"activate_robot_move_thr": 5},
                {"activate_robot_rotate_thr": 45}
            ],
            arguments=['--ros-args', '--log-level', 'warn']
        ),

        # 启动小R机器⼈小⻋
        Node(
            package='xrrobot',
            executable='xrrobot',
            output='screen',
            arguments=['--ros-args', '--log-level', 'warn']
        )
    ])
