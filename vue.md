# hello world

```vue
<!DOCTYPE html>
<html>

<head>
    <title>My first Vue app</title>
    <script src="https://cdn.jsdelivr.net/npm/vue/dist/vue.js"></script>
</head>

<body>
    
    <div id="app">
        {{ message }}
    </div>

    <script>
        var app = new Vue({
            el: '#app',
            data: {
                message: 'Hello Vue!'
            }
        })
    </script>
    
</body>

</html>
```

# 文本插值{{}}

使用{{message}}进行插值

```vue
<div id="app">
    {{ message }}
</div>

<script>
    var app = new Vue({
        el: '#app',
        data: {
            message: 'Hello Vue!'
        }
    })
</script>
```

如果message是一个html怎么办？使用v-html

```vue
<div id="app">
    <p v-html="message"></p>
</div>

<script>
    var app = new Vue({
        el: '#app',
        data: {
            message: '<span>一个span标签</span>'
        }
    })
</script>
```

# 属性插值v-bind

属性插值：`<span title={{message}}>tanght</span>`错！

属性插值：`<span v-bind:title="message">tanght</span>`对！

属性插值：`<span :title="message">tanght</span>`对！

属性插值不能像普通文本中那样用{{}}语法，需要使用v-bind:

```vue
<div id="app">
    <span v-bind:title="message">tanght</span>
</div>

<script>
    var app = new Vue({
        el: '#app',
        data: {
            message: 'Hello Vue!'
        }
    })
</script>
```

# 条件v-if

```vue
<div id="app">
    <p v-if="seen">tanght</p>
</div>

<script>
    var app = new Vue({
        el: '#app',
        data: {
            seen: true
        }
    })
</script>
```

# 循环v-for

```vue
<div id="app">
    <ol>
        <li v-for="name in names">{{name}}</li>
    </ol>
</div>

<script>
    var app = new Vue({
        el: '#app',
        data: {
            names: ["tanght1", "tanght2", "tanght3", "tanght4"]
        }
    })
</script>
```

注意v-for中取出的值要用{{}}来显示

# 事件监听v-on

```vue
    <div id="app">
        <p>{{message}}</p>
        <button v-on:click="rmessage">反转消息</button>
    </div>

    <script>
        var app = new Vue({
            el: '#app',
            data: {
                message: "123456"
            },
            methods: {
                rmessage: function () {
                    this.message = this.message.split('').reverse().join('')
                }
            }
        })
    </script>
```

# 双向绑定v-model

