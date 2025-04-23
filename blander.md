添加到集合：快捷键 m

隔离模式：只显示当前选中的物体，快捷键 /

衰减编辑：选择顶点，按G进入移动模式，鼠标滚轮调整衰减范围



快捷键

| 快捷键           | 作用                                                   | 备注 |
| ---------------- | ------------------------------------------------------ | ---- |
| shift+按住鼠标中 | 平移摄像机                                             |      |
| 按住鼠标中       | 旋转摄像机                                             |      |
| 滚动鼠标中       | 缩放摄像机                                             |      |
|                  |                                                        |      |
| 小键盘 1         | 正视图                                                 |      |
| 小键盘 3         | 侧视图                                                 |      |
| 小键盘 7         | 顶视图                                                 |      |
| 小键盘 9         | 当前角度的反面                                         |      |
| 小键盘 5         | 正交/透视                                              |      |
| 小键盘 .         | 聚焦到当前所选的物体                                   |      |
| 小键盘 /         | 独显当前物体（不显示其它物体）                         |      |
| 小键盘 0         | 摄像机视图                                             |      |
|                  |                                                        |      |
| G + 可选[X,Y,Z]  | 平移物体                                               |      |
| R + 可选[X,Y,Z]  | 旋转物体                                               |      |
| S + 可选[X,Y,Z]  | 缩放物体                                               |      |
| Alt + G          | 将选中的物体回到世界中心                               |      |
|                  |                                                        |      |
| Shift + A        | 创建物体                                               |      |
| Shift + D        | 复制并移动                                             |      |
| Shift + S        | 选择圆环                                               |      |
|                  |                                                        |      |
| H                | 隐藏当前物体（眼睛图标）                               |      |
| Shift + H        | 隐藏非当前物体（眼睛图标）                             |      |
| Alt + H          | 显示所有物体（眼睛图标）                               |      |
|                  |                                                        |      |
| ~                | 圆环菜单（顶视图、俯视图等）                           |      |
| Shift + S        | 圆环菜单（编辑模式、顶点绘制、物体模式、雕刻模式、等） |      |
| Ctrl + Tab       | 圆环菜单（选中项->游标、游标->原点、等）               |      |
|                  |                                                        |      |
| Shift + 鼠标右   | 移动游标                                               |      |

## 物体原点

可以修改

缩放，旋转都是以原点为中心进行的

## 偏好设置

围绕选择物体旋转

缩放至鼠标位置

## 变换轴心点

旋转物体的时候，以哪个点为基准点，可以选则物体原点或游标等等








# AnyIO 教学大纲：掌握统一的异步编程接口

# 一：初识 AnyIO (为何需要它？)

* **背景介绍：** Python 异步编程的演进（`asyncio` 的诞生）。
* **面临的问题：** 存在多个异步库（如 `asyncio`, `trio`）及其生态，导致库开发者和使用者面临选择和兼容性难题。
* **AnyIO 的定位：** 一个异步编程的 *抽象层* 或 *兼容层*。目标是让你编写的异步代码可以无缝运行在不同的异步后端（如 `asyncio` 或 `trio`）之上。
* **核心优势：**
    * **代码可移植性：** 编写一次，可在 `asyncio` 或 `trio` 上运行。
    * **统一 API：** 提供一致的 API 来处理常见的异步操作（任务、同步、流等）。
    * **结构化并发：** 借鉴并推广 `trio` 的优秀理念——任务组（Task Groups）。
* **基本概念：**
    * **后端 (Backend)：** 底层实际执行异步操作的库（`asyncio` 或 `trio`）。AnyIO 会自动检测或允许你指定。
    * **异步函数 (`async def`)：** 定义协程的基础。
    * **`await` 关键字：** 用于暂停协程执行，等待异步操作完成。

# 二：运行第一个 AnyIO 程序 (入口与基础)

* **最简结构：** 如何定义一个简单的异步函数。
* **核心入口：`anyio.run()`**
    * 作用：启动 AnyIO 的事件循环，并执行指定的异步函数。这是所有 AnyIO 应用的起点。
    * 基本用法：`anyio.run(async_function, *args)`。
    * 演示：运行一个打印 "Hello, AnyIO!" 的简单异步函数。
* **简单的异步操作：`anyio.sleep()`**
    * 作用：异步地暂停当前任务指定的时间（秒）。期间事件循环可以处理其他任务。
    * 对比：与 `time.sleep()` 的区别（`time.sleep` 会阻塞整个线程）。
    * 演示：在 `anyio.run` 中调用 `anyio.sleep()`。

# 三：并发执行：任务组 (结构化并发的核心)

* **并发的需求：** 同时执行多个独立的异步操作，而不是按顺序等待。
* **传统 `asyncio` 的方式 (对比)：** `asyncio.create_task()` 和 `asyncio.gather()`（引出管理复杂性的问题）。
* **AnyIO 的解决方案：任务组 (`TaskGroup`)**
    * **理念：** 结构化并发。确保在一个代码块内启动的所有任务，在该代码块结束前要么全部成功完成，要么在出错时能被妥善取消和处理。
    * **创建任务组：`async with anyio.create_task_group() as tg:`**
        * 使用 `async with` 确保任务组资源的正确管理。
    * **启动任务：`tg.start_soon(async_function, *args)`**
        * 在任务组中启动一个新的后台任务，不会阻塞当前任务。
        * 函数签名要求：第一个参数是异步函数，后续是传递给该异步函数的参数。
    * **等待所有任务完成：** `async with` 块结束时，会自动等待该组内所有 `start_soon` 启动的任务完成。
    * **错误处理：** 如果组内任何任务抛出未处理的异常，任务组会取消所有其他正在运行的任务，然后将异常（可能是 `MultiError`）重新抛出到 `async with` 语句之外。
* **演示：**
    * Demo 1: 使用任务组并发运行多个 `anyio.sleep()` 任务。
    * Demo 2: 演示任务组的错误处理机制（一个任务失败导致其他任务被取消）。

# 四：任务间的同步与协调 (锁、事件、信号量)

* **为何需要同步：** 当多个并发任务需要访问共享资源或需要相互协调执行顺序时，避免竞态条件和保证数据一致性。
* **AnyIO 提供的同步原语 (Primitives)：**
    * **锁 (`anyio.Lock`)**
        * 概念：一次只允许一个任务获取锁，用于保护临界区代码。
        * API：`lock = anyio.Lock()`, `async with lock: ...`
        * 演示：多个任务尝试修改共享变量，使用锁来保证操作的原子性。
    * **事件 (`anyio.Event`)**
        * 概念：一个任务可以等待某个事件发生（由另一个任务触发）。
        * API：`event = anyio.Event()`, `await event.wait()`, `event.set()`
        * 演示：一个任务等待另一个任务完成某个计算或初始化后才继续执行。
    * **信号量 (`anyio.Semaphore`)**
        * 概念：允许多个任务（达到指定数量上限）同时访问某个资源或代码段。
        * API：`semaphore = anyio.Semaphore(value)`, `async with semaphore: ...`
        * 演示：限制同时执行某个资源密集型操作的任务数量（例如，并发的网络请求数量）。
    * **(可选) 条件变量 (`anyio.Condition`)**
        * 概念：更复杂的同步机制，允许任务等待某个特定条件变为真，通常与锁配合使用。
        * API：`condition = anyio.Condition()`, `async with condition: await condition.wait()`, `async with condition: condition.notify() / condition.notify_all()`

# 五：超时与取消 (控制执行时间与中断)

* **重要性：** 防止任务无限期等待，以及在不再需要时能够主动停止任务。
* **AnyIO 的取消机制：取消作用域 (`CancelScope`)**
    * 概念：控制一组异步操作的取消。可以设置超时，超时后自动取消作用域内的操作。
    * **超时控制：**
        * `anyio.move_on_after(seconds)`：创建一个取消作用域，在指定时间后自动取消。即使超时，`async with` 块也会正常退出（不抛异常，但 `scope.cancel_called` 会是 `True`）。
        * `anyio.fail_after(seconds)`：类似 `move_on_after`，但在超时后会抛出 `TimeoutError`。
        * API：`async with anyio.move_on_after(5) as scope: ...`, `if scope.cancel_called: ...`
        * API：`async with anyio.fail_after(5): ...`
    * **手动取消：**
        * `anyio.CancelScope()`：创建普通取消作用域。
        * `scope.cancel()`：手动触发作用域的取消。
        * API：`with anyio.CancelScope() as scope: ... scope.cancel()`
    * **屏蔽取消 (`shield=True`)**
        * 概念：在 `move_on_after` 或 `fail_after` 中设置 `shield=True`，可以保护该代码块不受外部取消作用域的影响（但自身的超时仍然有效）。
        * API：`async with anyio.move_on_after(10, shield=True): ...`
* **演示：**
    * Demo 1: 使用 `move_on_after` 给一个可能长时间运行的操作设置超时。
    * Demo 2: 使用 `fail_after` 在超时后捕获 `TimeoutError`。
    * Demo 3: 嵌套的取消作用域，演示手动取消和屏蔽效果。

# 六：异步 I/O：流 (Streams)

* **概念：** AnyIO 提供统一的流 API 来处理各种 I/O 操作（网络、文件等），隐藏了不同后端的具体实现差异。
* **TCP 网络编程：**
    * **连接到服务器 (`anyio.connect_tcp`)**
        * API：`async with await anyio.connect_tcp(host, port) as client_stream:`
    * **创建服务器 (`anyio.create_tcp_listener`)**
        * API：`async with await anyio.create_tcp_listener(local_port) as listener:`
        * API：`await listener.accept()` 返回 `(client_stream, remote_address)`
    * **流操作 (通用 API)：**
        * `await stream.send_all(data)`：发送字节数据。
        * `await stream.receive(max_bytes)`：接收字节数据。
        * `await stream.aclose()`：异步关闭流（通常由 `async with` 自动处理）。
* **演示：**
    * Demo 1: 简单的 TCP 客户端，连接到现有服务并收发数据。
    * Demo 2: 简单的 TCP 回显服务器 (Echo Server)。
* **(可选) 异步文件 I/O (`anyio.open_file`)**
    * API：`async with await anyio.open_file(path, mode) as f:`
    * 流操作：`await f.read()`, `await f.write()`, `await f.seek()`, `await f.tell()`
    * 演示：异步读取或写入本地文件。

# 七：任务间通信：内存对象流 (Memory Object Streams)

* **需求：** 在同一进程的不同异步任务之间安全地传递 Python 对象。
* **AnyIO 的方案：内存对象流**
    * 概念：类似队列，但提供了流的接口，用于在生产者和消费者任务之间传递对象。支持背压（当流满时发送者会阻塞）。
    * **创建流：`anyio.create_memory_object_stream(max_buffer_size)`**
        * 返回一对 `(SendStream, ReceiveStream)`。
        * `max_buffer_size`: 缓冲区大小，控制背压。0 表示无限制，1 表示每次只能放一个对象。
    * **发送端 (`SendStream`)**
        * API：`await send_stream.send(object)`
        * API：`await send_stream.aclose()` (通知接收端发送完成)
    * **接收端 (`ReceiveStream`)**
        * API：`await receive_stream.receive()`
        * API：`async for object in receive_stream:` (常用，直到发送端关闭)
        * API：`await receive_stream.aclose()`
* **演示：** 创建一个生产者任务不断生成数据并通过内存流发送，一个消费者任务接收并处理数据。

# 八：与同步代码交互 (桥接阻塞操作)

* **挑战：** 在异步代码中调用阻塞的同步函数（如某些库的函数、CPU密集型计算）会阻塞整个事件循环。
* **AnyIO 的解决方案：在工作线程中运行同步代码**
    * **`anyio.to_thread.run_sync(sync_function, *args, cancellable=False, limiter=None)`**
        * 作用：将同步函数 `sync_function` 及其参数 `args` 交给一个独立的线程执行，并异步等待其结果。
        * `cancellable=True`：允许该操作响应 AnyIO 的取消请求（可能需要同步函数内部配合）。
        * `limiter`：一个 `anyio.CapacityLimiter` 对象，用于限制并发运行的线程数量。
    * **(可选) 从工作线程调用异步代码 (`anyio.from_thread.run`)**
        * 作用：允许在由 `run_sync` 启动的工作线程中，反过来调用主事件循环中的异步函数。
* **演示：**
    * Demo 1: 在异步函数中使用 `run_sync` 调用一个耗时的同步函数（如 `time.sleep` 或一个计算密集函数），同时运行其他异步任务以展示事件循环未被阻塞。
    * Demo 2: (可选) 使用 `CapacityLimiter` 限制同时运行的同步任务线程数。

# (可选) 模块九：后端选择与探测

* **自动检测：** 通常 AnyIO 会自动检测环境中安装的 `asyncio` 或 `trio` 并选择一个作为后端。
* **手动指定后端：**
    * API：`anyio.run(async_function, backend='asyncio'/'trio')`
* **检查当前后端：**
    * API：`backend_name = anyio.get_current_backend()`
* **使用特定后端的原生 API (`current_async_library`)**
    * API: `asyncio_module = anyio.current_async_library()` (如果后端是 asyncio)
    * 用途：当需要调用 `anyio` 未封装的底层库特性时（应谨慎使用，会降低可移植性）。
* **演示：** 显式指定后端运行，并打印当前使用的后端名称。

# 总结与后续学习

* 回顾 AnyIO 的核心价值和主要 API。
* 强调结构化并发的重要性。
* 鼓励学生查阅 AnyIO 官方文档，探索更高级的特性（如 UDP、Unix Domain Sockets、进程运行等）。
* 讨论在实际项目中如何选择和应用 AnyIO。