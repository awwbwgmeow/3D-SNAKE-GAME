# 3D-SNAKE-GAME
## Projection Name: 3D First-person Greedy Snake

## Description: 
This is a 3D First-person Greedy Snake game developed on python 3.10.7.
In the game, the part of map within the player's view will be displayed on the upper left corner, and the main game screen would be shown in 3D view.
The player would control a snake.
When it eats a fruit, it's length would +1, and score would +1;
when it crushes into walls or itself, it will dead and the game failed;
when it move into the portals, it would be transported to the otherside of the map;
when the fruit is within the player's view, it will be displayed on the upper left map.
The moving speed of the snake would increase as the score increases.


## How to run the project: 
You shall run the "main.py" in the folder.

## Libraries to install: 
pygame(2.1.2)

## Shortcut commands: 
Press any key or the "START" button in the upper right corner to start or continue the game.
Press the "PAUSE" button in the upper right corner to pause the game.
Press "left" key to rotate the snake head counterclockwise.
Press "right" key to rotate the snake head clockwise.
If failed, ress "RESTART" button to restart the game.

## Project Report
REPORT OF THE 3D GREEDY SNAKE PROJECT
### 1. Project Description
Name：3D First-person Greedy Snake
Discription: This is a 3D First-person Greedy Snake game developed on python 3.10.7.
In the game, the part of map within the player's view will be displayed on the upper left corner, and the main game screen would be shown in 3D view.
The player would control a snake. When it eats a fruit, it's length would +1, and score would +1; when it crushes into walls or itself, it will dead and the game failed; when it move into the portals, it would be transported to the otherside of the map; when the fruit is within the player's view, it will be displayed on the upper left map.
The moving speed of the snake would increase as the score increases.
### 2. Structural Plan
I will introduce how my project is organized by the order of files.
#### 1) main.py
This is the file that user should run. In the file, it defines the Game class and include the running logic of the game. For example, it defines in which cases the game would start, pause or fail. It decides how the game objects will be updated, when the snake would crush into the wall or meet with the fruit. It draws most of the game objects on the screen, and check the key pressing events which is used to move the snake.
#### 2) player.py
The file defines the Player class and include how the snake is moved, and how the camera(which is at the same place of snake head). In the file it would load all the snake image texture onto the the snake and draw the snake on the screen.
#### 3) settings.py
The file include all the constant setting values of the game, including the screen size, FPS, cell numbers, initial position/angle/speed/view size of the player, raycasting settings, texture size and so on.
#### 4) map.py
The file includes the game map in the two demensional list, where 0 represents passable floor, 1 represents wall and 3 represents portals. It would draw the part of map within the player's view.
#### 5) sprite_object.py
The file creates fruit which will be shown both in the 2D map and the 3D view.
#### 6) raycasting.py
The file creates a 3D engine by obtaining the view of the camera.
#### 7) renderer.py
The file renders all the game projects that will be shown in 3D view and load 3D texture images.
#### 8) buttons.py
The file creates the start, pause, restart buttons to control the game, and the scoreboard as well.
### 3. Algorithmic Plan
There’s many complex parts in my project. For example, how to achieve 3D displaying and raycasting. For short, I would just introduce how I manage to move my camera. I just make the position of camera equal to the snake head every 500ms, and in every period of time, the position of camera will change continuously according to the moving direction of the snake, and so that I need to check the position relationships between the snake body blocks to determine where the snake is going. And as the movement of snake is not continuous, I create two functions, in which I seperately make the snake and the camera move and rotates.
### References: 
#### 1) 3D pygame engine developing
The most diffcult part of my project is how to demonstrate the game in 3D view, and it’s beyond my competence, so I turn to the pro developer’s video for assistance.
Link:
https://www.youtube.com/watch?v=ECqUrT7IdqQ&list=PLi77irUVkDatlbulEY4Kz8O107HO8RGH8
Project file: 
https://github.com/StanislavPetrovV/DOOM-style-Game
#### 2) greedy snake based on pygame
Link:
https://www.youtube.com/watch?v=QFvqStqPCRU
### 4. Module List
In the project, the only external module I use is pygame 2.1.2.


本项目为个人python大作业。
## 演示视频地址：
https://www.bilibili.com/video/BV1Rg4y1P7w6/?spm_id_from=333.999.0.0&vd_source=52f6cccd463cdab4ff14d816afc809cc
## 参考项目：
### 1.pygame伪3D效果实现：
https://github.com/StanislavPetrovV/DOOM-style-Game
### 2.pygame贪吃蛇游戏制作：
https://www.youtube.com/watch?v=QFvqStqPCRU
