# Share Challenge
## Team: 윤연철표류기
### Members : 
[류태훈(Taehun Ryu)](https://github.com/taehun-ryu), [박하윤](https://github.com/parkhy0106), [유연철](https://github.com/YouYCJS), [이기검](https://github.com/geegum), 김민표

---

# Abstract
&emsp;현재 시장에 있는 무인카트는 카트 자체에 대부분의 소프트웨어 시스템이 구현되어 있다. 즉, <span style='color:red'>카트 한 대당 비용이 굉장히 비싸다.</span> 사람이 많은 대형마트의 경우 필요한 카트가 많기 때문에 무인매장 시스템을 도입하는데 있어 가격적인 면에서 부담이 높다. 우리는 이 부분에서 해결책을 제시하고자 했다. <span style="color:gray"><i>기본적으로 B2B를 지향, 대형마트기업을 우리 로봇의 주 고객층으로 설정.</i></span>

&emsp;기본적으로 무인카트의 핵심은 **Human following**과 **Dynamic obstacle avoidance**다. 따라서 우리는 Computer Vision(Object detecting)을 담당할 하나의 main system을 독립적으로 구축하고, 다른 많은 카트들은 main system에서 필요한 정보만을 받아 움직이게 한다. 즉, **<span style="color:green">로봇(무인 카트)의 컴퓨팅 능력을 낮춰 로봇 한 대 당 가격을 최대한 낮추는 것이 목표이다.</span>**

&emsp;결과적으로, 로봇이(무인 카트) 한 대만 있을경우에는 main system 비용 때문에 비용적 이득이 크진 않을지라도 로봇이 많아지면 경제적 이익이 보장 될 것이다.<span style="color:gray"><i> 지원받은 500만원 중 무인카트에 쓰인 비용을 80만원 아래로 맞추었다.</i></span>

<img src="https://github.com/taehun-ryu/ShareChallenge_team_yycprg/assets/73813854/7e4b99e4-14e0-4f3a-ac48-fdcf78d72e49" width="70%" align="center">

---

# Implementation Method
## Vision System
각 카메라 coordinate에서 사람의 좌표를 추출한 뒤, 각 카메라 coordinate system을 global system위에서의 좌표로 통일하였다.

<img src="https://github.com/taehun-ryu/ShareChallenge_team_yycprg/assets/73813854/bbd7e052-47c2-411c-927b-4b2215ebd25d" width="70%">



## Communication System
&emsp;우선 로봇의 컴퓨팅 능력이 그리 좋지 않더라도 real-time delay없이 구현해야 했다. 그래서 우리는 **<span style="color:red">ROS를 사용하지 않고</span>** 직접 일일이 통신을 뚫어주기로 결정하였다. Human detecting & validation을 진행하고 있는 main system과 로봇과는 <span style="color:green">socket 통신</span>을 활용하여 네트워크 시스템을 구현하였고, 모터제어를 담당하는 Arduino와 SBC(Single Board Computer)는 Serial통신의 한 종류인 <span style="color:green">UART통신</span>으로 연결하였다.

&emsp;전반적인 시스템 구조는 다음과 같다.

<center><img src ="https://github.com/taehun-ryu/ShareChallenge_team_yycprg/assets/73813854/99d5c3f0-509f-417f-899f-f8602c784beb" width="70%"></center>

## Obstacle Avoidance
&emsp;장애물 회피의 경우 Lidar센서를 활용하였다. 로봇의 앞, 뒤로 Lidar센서를 2개를 부착하여 로봇의 Pillar(프로파일)에 의해 생기는 사각지대를 없앴다. 우리는 따로 Mapping을 하지 않기 때문에 Global Plan 자체가 Goal을 향한 유클리드 거리 주행이다. 따라서 Local Plan을 **<span style="color:red">동적 장애물에 대한 완벽한 회피알고리즘으로 구현하기에 어려움이 있었다.</span>** 결국 큰 모션을 <span style="color:green">정지 or MovoToGoal</span>로 나누어 단순히 구현했다.

## Localization
&emsp;기본적으로 **Encoder Odometry**를 중심으로 한다. 추가로 ArUco Marker를 이용하여 오차를 보정하였다.

---

![main_poster](https://github.com/taehun-ryu/ShareChallenge_team_yycprg/assets/73813854/00c48584-a122-489c-a6c1-02cdc49323f0)

