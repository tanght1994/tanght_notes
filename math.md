# 线性代数

## 行列式

行列式用于解方程，例如2个未知数，2个方程，这两个未知数可以用D1/D2求出来，D1和D2是行列式
$$
\left \{
\begin{array}{c}
1x+2y=5 \\
3x+4y=6 \\
\end{array}
\right.
$$
系数行列式为：
$$
\left|
\begin{array}{c}
1&2 \\
3&4 \\
\end{array}
\right|
$$

## Cramer（克莱姆法则）

余子式

代数余子式

按行展开求行列式的值：某一行的各元素与其代数余子式的乘积之和

# 曲线

B样条曲线：曲线不保证经过控制点，曲线首先保证自然度，其次保证经过控制点

贝塞尔曲线：

CatmullRoom曲线：曲线会经过所有控制点，曲线优先保证经过所有控制点，其次保证曲线的弯曲自然度。https://en.wikipedia.org/wiki/Centripetal_Catmull%E2%80%93Rom_spline

样条插值：一次样条、二次样条、三次样条