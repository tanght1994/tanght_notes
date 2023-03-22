代码创建Mesh



```typescript
let mesh = cc.utils.MeshUtils.createMesh({
　　positions: [0, 10, 0, 0, 0, 0, 10, 0, 0, 10, 0, 0, 10, 10, 0, 0, 10, 0],
　　indices: [],
　　uvs: [0, 0, 0, 1, 1, 1, 1, 1, 1, 0, 0, 0],
});
```



# 属性检查器可见性

字段在检查器中的可见性规则如下：

如果设置了`@property({visible: true | false})`，那么就根据visible参数来控制。这个规则的优先级最高。

如果没有设置`@property({visible: true | false})`，则通过字段是否以下划线开头来判断，下划线开头的不在属性检查器中显示。

```typescript
// 即便以_开头，属性检查其中依然可见
@property({visible: true})
_mystring: string = ''

// 即便不是_开头，属性检查其中依然不可见
@property({visible: false})
mystring: string = ''
```

set方法永远不用@property修饰

get方法可以用@property修饰，来控制其在属性检查器中的可见性

！！！属性检查器中的可见与否，与此字段是否被序列化，毫无关系！！！

# 序列化

- 在场景中设置完属性检查器中的参数之后，按ctrl+s保存场景，这时，刚刚设置的那些参数就被保存到scene文件中了。关闭cocos编辑器，下次再打开的时候，编辑器中的值就是你上次设置的值。
- 将属性检查器中的参数，保存到scene中的功能是property装饰器提供的，property的serializable参数控制是否将此字段序列化。

下面三个property的用法是完全一样的，都是使用默认参数

```typescript
@property
myvar: string = ''

@property()
myvar: string = ''

@property({})
myvar: string = ''
```



