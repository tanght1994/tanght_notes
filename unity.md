C#热更：HyBridCLR

LUA热更：XLUA

# shader

## Tags语句

Tags { "RenderType"="Transparent" "Queue" = "Transparent"}

其中"Queue" = "Transparent"用于shader执行顺序排序，你写的透明相关的shader需要在非透明物体之后才能执行，如果你不将你的透明shader的设置为"Queue" = "Transparent"，那么你的透明物体的渲染顺序是随机的，有可能不是最后执行，所以有可能被非透明物体覆盖

## Blend语句

什么是颜色混合？对于透明图片才有颜色混合，不透明图片不存在颜色混合一说。

场景中A图片覆盖了B图片，如果A图片是非透明的，那么A图片占据的像素直接设置为A图片的颜色即可，无需颜色混合。

场景中A图片覆盖了B图片，如果A图片是透明的，现在我来模拟一下渲染流程：

1. 首先渲染B图片（透明图片最后才渲染，这是规则），间B图片占据的像素设置为B图片的颜色。
2. 然后渲染A图片，A图片占据的像素位置的颜色=A图片的颜色与此像素已经存在的颜色进行混合，混合的公式为：
3. 最终颜色 = A图颜色 x a + 已经存在的颜色 x b
4. 一半情况下我们将a设置为A透明度，a = A透明度
5. b设置为1 - A透明度， b = 1 - A透明度
6. 所以最终公式为：最终颜色=A图颜色 x A透明度 + 已经存在的颜色 x (1 - A透明度)
7. a和b的值要用Blend语句设置，格式为Blend a b
8. 如果不写Blend语句，默认为Blend Off，那就等于把A图片当成非透明图片来进行渲染

你在PS中画了一个透明背景的圆形，其实PS是给你画了一个矩形，然后将圆形外部的区域透明度设置为0，所以如果你将此图片当成非透明图片来处理的话，你看到的是一个矩形哦。你为什么要将它当成非透明图片来处理呢？因为你可能忘记写Blend语句了。



```
Pass
{
    Blend SrcAlpha OneMinusSrcAlpha
    CGPROGRAM
    ...
}
```

## 柏林噪声





# 相机遮挡关系

## Z轴

2d游戏中，对于正交相机，z轴没有任何意义，不管你如何设置Z轴，unity根本就不会读取Z轴的数据，所以直接忽略即可。

2d游戏中，对于透视相机，z轴只与显示有关，与物理引擎无关，物理引擎根本就不关心Z轴数据，即使两个物体的Z轴不一致，依然能够产生碰撞。

## 透视相机，遮挡关系优先级：

1. sprite render 中的 sorting layer
2. sorting layer 中的 order in layer
3. z轴
4. 也就是说先通过sorting layer确定遮挡关系，如果两个物体的sorting layer一样，再通过order in layer判断，如果order in layer也一样，再通过Z轴判断

## 正交相机，遮挡关系优先级：

1. sprite render 中的 sorting layer
2. order in layer





# Setting文件

Edit -> Project Settings 中的配置都保存在/ProjectSettings文件夹中

2D项目的设置在Physics 2D中，3D项目的设置在Physics中，主要为一些物理引擎相关的设置，比如碰撞矩阵，重力值等等。其它设置为2D 3D项目通用设置。

- /ProjectSettings/TagManager.asset文件：用户设置的 Tag，Layer，Sorting Layer（物体的order in layer在场景文件xxx.unity中，预制体的order in layer在预制体的xxx.prefab中）
- DynamicsManager.asset文件：3D物理引擎设置，重力，碰撞矩阵等，对应编辑器中的Edit -> Project Settings->Physics部分
- Physics2DSettings.asset文件：2D物理引擎设置，重力，碰撞矩阵等，对应编辑器中的Edit -> Project Settings->Physics2D部分
- InputManager.asset文件：手柄按键、键盘按键映射



# Input Manager

| 手柄按键 | Unity Input Manager 中的名字 |
| -------- | ---------------------------- |
| A        | joystick button 0            |
| B        | joystick button 1            |
| X        | joystick button 3            |
| Y        | joystick button 4            |
| LB       | joystick button 6            |
| RB       | joystick button 7            |
| LT       | joystick button 8            |
| RT       | joystick button 9            |
|          |                              |
|          |                              |
|          |                              |



# Trigger

碰撞矩阵中Layer设置对Trigger也生效

触发器与碰撞体可以触发，触发器与触发器也可以触发，触发的条件为双方有一方或双方有Rigidbody既可以触发，双发的父物体（爷爷物体，祖宗物体也行）有Rigidbody也算



# 事件函数

Awake，是第一个执行的函数，且只执行一次，不管物体当前是否是active，都会执行Awake

OnEnable，是第二个执行的函数，只要物体从inactive到active就会执行此函数

Start，如果当前物体是inactive，则不执行Start，等到物体被设置为active的时候再执行Start，一个物体不管active多少次，只会在第一次active的时候执行Start





# Sprite尺寸

一张图片在Unity的世界中长宽是多少？由两个参数控制：

- Pixels Per Unit：世界坐标中的1米对应多少像素
- Transform：Transform中的Scale

这两个参数一起，就可以确认一张图片在世界坐标中的大小了。比如说一张图片是1000 X 500的尺寸，图片的Pixels Per Unit设置为500，那么它在世界坐标中的尺寸为：

- 宽度：(1000 / 500) * Transform.Scale.x
- 高度：(500/ 500) * Transform.Scale.y

**SpriteRenderer.bounds.size**：获取的尺寸与Transform、Pixels Per Unit、所有祖宗的Transform相关

**SpriteRenderer.sprite.bounds.size**：只与图片的Pixels Per Unit有关

**注意：**SpriteRenderer.bounds.size可以获取到物体的在物理世界中的真实大小，Transform.Scale并不代表物体的真实大小，Scale只是缩放，因为有可能这张图片在Scale为1的时候就是5 X 5呢





# MaterialPropertyBlock

使用这个修改shader的参数，不会生成新的材质





# AssetBundle

## 加载



# 微信小游戏

微信的Unity SDK

https://gitee.com/wechat-minigame/minigame-tuanjie-transform-sdk.git
