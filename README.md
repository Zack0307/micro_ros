```markdown
# 🚗 Yahboom MicroROS Robot - Distributed Control System

This repository contains the configuration, scripts, and documentation for operating a Yahboom MicroROS robot using a **Distributed ROS 2 Architecture**. 

By offloading highly computational tasks (like SLAM, Navigation, or Joystick processing) to a more powerful PC, the Raspberry Pi can focus purely on hardware interfacing (Edge Node), resulting in a highly efficient and scalable robotic system.

## 🏗️ System Architecture

* **Robot Edge Device:** Raspberry Pi (Running Yahboom ROS 2 Humble Docker container) + MicroROS Control Board.
* **Commander Unit:** Powerful PC/Laptop (Running native ROS 2 or Docker).
* **Communication:** Standard Wi-Fi Network via ROS 2 DDS.

---

## ⚙️ 1. Environment & Network Setup

To allow the PC and Raspberry Pi to communicate seamlessly, they **must be connected to the same Wi-Fi network** and share the same `ROS_DOMAIN_ID`.

Run the following command on **both** the PC and the Raspberry Pi (you can add this to your `~/.bashrc` to make it permanent):

```bash
export ROS_DOMAIN_ID=20
```

---

## 🐳 2. Raspberry Pi Setup (Edge Node)

The Yahboom system runs inside a Docker container. To prevent losing your custom code when the container restarts, we use Volume Mounting (`-v`) to share a folder between the Pi and the container.

**Start the Docker Container:**
Run this modified startup script to ensure the USB gamepad and your custom code directory are mapped correctly:

```bash
docker run -it \
  --privileged=true \
  --net=host \
  --env="DISPLAY" \
  --env="QT_X11_NO_MITSHM=1" \
  -v /tmp/.X11-unix:/tmp/.X11-unix \
  --security-opt apparmor:unconfined \
  -v /dev/input:/dev/input \
  -v /dev/video0:/dev/video0 \
  -v /root/my_ros2_code:/root/my_ros2_code \
  yahboomtechnology/ros-humble:4.1.2 /bin/bash
```
*(Note: Change `/root/my_ros2_code` to the actual path where you store your scripts on the Raspberry Pi.)*


---

## 💻 3. PC Setup (Commander Node)

The PC handles the user input (Gamepad) and runs the python control logic.

**Install Required Packages:**
Install the ROS 2 Joy package to read gamepad inputs:
```bash
sudo apt update
sudo apt install ros-humble-joy*
```

**Run the Control System:**
1. Connect your USB Gamepad to the PC.
2. Start the joy node:
   ```bash
   ros2 run joy joy_node
   ```
3. Run the custom python teleop script (e.g., `joy_ctrl.py`):
   ```bash
   ros2 run micro_ros joy
   ```
4. **Unlock the Robot:** Press the **Start Button (Button 7)** on your gamepad to enable motor control, then use the joysticks to drive!
5. **You can open single terminal to launch file**
   ```bash
   ros2 launch micro_ros micro_ros.launch.py
   ```

---
**Launch the all system(IN the Test.....)**
1. Start all the simulator 
   ```bash
   ros2 launch micro_ros micro_ros.launch.py 
   ```
2. Start part of e.g rviz2,urdf
   ```bash
   ros2 launch micro_ros display.launch.py 
   ```
## 🛠️ Troubleshooting & Tips

### Fixing "Zombie Nodes" and Duplicate Topics
If you incorrectly stop a program (e.g., using `Ctrl + Z` instead of `Ctrl + C`), or if background processes fail to terminate, you may see duplicate topics when running `ros2 topic list`.

To force-kill all lingering ROS and Python processes, run:
```bash
pkill -f ros
pkill -f python
```
*(Warning: This will terminate all active ROS 2 nodes and Python scripts on the device.)*

### Saving Docker State
If you install new packages (`apt-get install`) inside the Raspberry Pi's Docker container, remember to commit the state to a new image so you don't lose them after a reboot:
```bash
docker commit <container_id> my_yahboom_ros:v1
```

---

## 🚀 Future Roadmap (To-Do List)

- [x] Establish PC-to-Pi distributed control via `ROS_DOMAIN_ID`.
- [x] Configure Gamepad Teleop using `ros-humble-joy`.
- [ ] Connect and configure the onboard webcam.
- [ ] Implement 2D Lidar for map generation (Gmapping / Cartographer).
- [ ] Connect another powerful edge device (e.g., NVIDIA Jetson) to run complex 3D SLAM algorithms.