# 数据库表及接口的设计文档

# 1.用户模块
## 1.1存储设计
### 1.1.1存储方式
Mysql+Redis。用户基本数据存储在Mysql，手机验证码存储在Redis。
### 1.1.2用户表设计
```
create table user
(
  id int auto_increment primary key,      -- 自增id  主键
  phone_num char(11) NOT NULL,            -- 用户手机号
  device_id varchar(20) NOT NULL,         -- 用户注册设备号
  create_time timestamp NOT NULL,         -- 注册时间
  user_token varchar(50),           -- token(用户的唯一私钥)
  user_id char(32),                       -- 用户唯一标识userid
  user_password varchar(20),              -- 密码
  last_login_time timestamp,              -- 上次登录时间
  user_name varchar(20)                   -- 用户名
);
```
### 1.1.3用户验证码字段设计
用户验证码字段存储在Redis里。key为手机号+"_phone_code"，value为手机验证码，超时时间为60s。

## 1.2业务流程

## 1.3接口
### 1.3.1获取验证码接口
/register/phone_num
为输入的手机号生成验证码。
#### 1.3.1.1输入参数
<table>
  <tr>
    <th>节点</th>
    <th>节点路径</th>
    <th>节点类型</th>
    <th>后台类型</th>
    <th>是否必须</th>
    <th>说明</th>
  </tr>
  <tr>
    <td>phone_num</td>
    <td>phone_num</td>
    <td>STRING</td>
    <td>String</td>
    <td>是</td>
    <td>手机号</td>
  </tr>
</table>

#### 1.3.1.2输出参数
<table>
  <tr>
    <th>节点</th>
    <th>节点路径</th>
    <th>节点类型</th>
    <th>后台类型</th>
    <th>说明</th>
  </tr>
  <tr>
    <td>error_code</td>
    <td>error_code</td>
    <td>STRING</td>
    <td>String</td>
    <td>错误码</td>
  </tr>
  <tr>
    <td>error_message</td>
    <td>error_message</td>
    <td>STRING</td>
    <td>String</td>
    <td>错误信息</td>
  </tr>
</table>


### 1.3.2验证验证码接口
/validate/phone_num
验证app输入的验证码是否和服务器保存的验证码一致。
#### 1.3.2.1输入参数
<table>
  <tr>
    <th>节点</th>
    <th>节点路径</th>
    <th>节点类型</th>
    <th>后台类型</th>
    <th>是否必须</th>
    <th>说明</th>
  </tr>
  <tr>
    <td>phone_num</td>
    <td>phone_num</td>
    <td>STRING</td>
    <td>String</td>
    <td>是</td>
    <td>手机号</td>
  </tr>
  <tr>
    <td>phone_code</td>
    <td>phone_code</td>
    <td>STRING</td>
    <td>String</td>
    <td>是</td>
    <td>验证码</td>
  </tr>
</table>

#### 1.3.2.2输出参数
<table>
  <tr>
    <th>节点</th>
    <th>节点路径</th>
    <th>节点类型</th>
    <th>后台类型</th>
    <th>说明</th>
  </tr>
  <tr>
    <td>error_code</td>
    <td>error_code</td>
    <td>STRING</td>
    <td>String</td>
    <td>错误码</td>
  </tr>
  <tr>
    <td>error_message</td>
    <td>error_message</td>
    <td>STRING</td>
    <td>String</td>
    <td>错误信息</td>
  </tr>
</table>

### 1.3.3注册接口
/register/user
根据输入注册用户。
#### 1.3.3.1输入参数
<table>
  <tr>
    <th>节点</th>
    <th>节点路径</th>
    <th>节点类型</th>
    <th>后台类型</th>
    <th>是否必须</th>
    <th>说明</th>
  </tr>
  <tr>
    <td>phone_num</td>
    <td>phone_num</td>
    <td>STRING</td>
    <td>String</td>
    <td>是</td>
    <td>手机号</td>
  </tr>
  <tr>
    <td>device_id</td>
    <td>device_id</td>
    <td>STRING</td>
    <td>String</td>
    <td>是</td>
    <td>设备号</td>
  </tr>
  <tr>
    <td>password</td>
    <td>password</td>
    <td>STRING</td>
    <td>String</td>
    <td>是</td>
    <td>密码</td>
  </tr>
</table>

#### 1.3.3.2输出参数
<table>
  <tr>
    <th>节点</th>
    <th>节点路径</th>
    <th>节点类型</th>
    <th>后台类型</th>
    <th>说明</th>
  </tr>
  <tr>
    <td>error_code</td>
    <td>error_code</td>
    <td>STRING</td>
    <td>String</td>
    <td>错误码</td>
  </tr>
  <tr>
    <td>error_message</td>
    <td>error_message</td>
    <td>STRING</td>
    <td>String</td>
    <td>错误信息</td>
  </tr>
  <tr>
    <td>user_id</td>
    <td>user_id</td>
    <td>NUMBER</td>
    <td>Integer</td>
    <td>用户id</td>
  </tr>
</table>

# 2.商品模块
## 2.1存储设计
### 2.1.1存储方式
Mysql。
### 2.1.2商品类别表设计
```
create table product_category
(
  id int auto_increment primary key,       -- 自增id  主键       
  name varchar(20),                        -- 分类名称
  code varchar(20),                        -- 分类编码
  category_order varchar(50),              -- 分类排序（order与数据库关键字冲突）
  parent_id int,                           -- 父级分类id 0父类 其他子类
  show_in_nav char(1)                      -- 是否显示在导航内 y显示 n不显示
);
```

### 2.1.3商品表设计
```
create table product
(
  id int auto_increment primary key,      -- 自增id  主键       
  status tinyint,                         -- 商品状态 1 新增 2 已上架 3 已下架
  category_id int,                        -- 商品类别id
  name varchar(50),               		-- 商品名称
  introduction varchar(50),               -- 商品简介
  price decimal(6,2),                     -- 商品定价
  now_price decimal(6,2),                  -- 商品现价
  picture varchar(50),                    -- 商品图片
  create_time timestamp,                  -- 商品创建时间
  sale int,                               -- 商品销售数量
  stock int                               -- 商品库存
);
```
## 2.2业务流程
## 2.3接口
### 2.3.1获取商品种类接口
/product_category/category
查询所有商品种类并返回。

#### 2.3.1.1输入参数
<table>
  <tr>
    <th>节点</th>
    <th>节点路径</th>
    <th>节点类型</th>
    <th>后台类型</th>
    <th>是否必须</th>
    <th>说明</th>
  </tr>
</table>

#### 2.3.1.2输出参数
<table>
  <tr>
    <th>节点</th>
    <th>节点路径</th>
    <th>节点类型</th>
    <th>后台类型</th>
    <th>说明</th>
  </tr>
  <tr>
    <td>catagory</td>
    <td>catagory</td>
    <td>Object</td>
    <td>List&lt;Product_category&gt;</td>
    <td>商品类列表</td>
  </tr>
  <tr>
    <td>id</td>
    <td>catagory.id</td>
    <td>NUMBER</td>
    <td>Integer</td>
    <td>商品类id</td>
  </tr>
  <tr>
    <td>name</td>
    <td>catagory.name</td>
    <td>STRING</td>
    <td>String</td>
    <td>商品类名称</td>
  </tr>
  <tr>
    <td>category_order</td>
    <td>catagory.category_order</td>
    <td>STRING</td>
    <td>String</td>
    <td>商品类顺序</td>
  </tr>
  <tr>
    <td>children</td>
    <td>catagory.children</td>
    <td>Object</td>
    <td>List&lt;Product_category&gt;</td>
    <td>商品类的子类列表</td>
  </tr>
  <tr>
    <td>id</td>
    <td>catagory.children.id</td>
    <td>NUMBER</td>
    <td>Integer</td>
    <td>商品子类id</td>
  </tr>
  <tr>
    <td>name</td>
    <td>catagory.children.name</td>
    <td>STRING</td>
    <td>String</td>
    <td>商品子类名称</td>
  </tr>
  <tr>
    <td>category_order</td>
    <td>catagory.children.category_order</td>
    <td>STRING</td>
    <td>String</td>
    <td>商品子类顺序</td>
  </tr>
  <tr>
    <td>children</td>
    <td>catagory.children.children</td>
    <td>Object</td>
    <td>List&lt;Product_category&gt;</td>
    <td>商品子类的子类列表</td>
  </tr>
  <tr>
    <td>......</td>
    <td>......</td>
    <td>......</td>
    <td>......</td>
    <td>......</td>
  </tr>
</table>



### 2.3.2获取商品接口
/product_category/product
根据输入的商品种类id返回该类别下的所有商品。
#### 2.3.2.1输入参数
<table>
  <tr>
    <th>节点</th>
    <th>节点路径</th>
    <th>节点类型</th>
    <th>后台类型</th>
    <th>是否必须</th>
    <th>说明</th>
  </tr>
  <tr>
    <td>category_id</td>
    <td>category_id</td>
    <td>NUMBER</td>
    <td>Integer</td>
    <td>是</td>
    <td>商品类id</td>
  </tr>
</table>

#### 2.3.2.2输出参数
<table>
  <tr>
    <th>节点</th>
    <th>节点路径</th>
    <th>节点类型</th>
    <th>后台类型</th>
    <th>说明</th>
  </tr>
  <tr>
    <td>product</td>
    <td>product</td>
    <td>Object</td>
    <td>List&lt;Product&gt;</td>
    <td>商品列表</td>
  </tr>
  <tr>
    <td>id</td>
    <td>product.id</td>
    <td>Number</td>
    <td>Integer</td>
    <td>商品类id</td>
  </tr>
  <tr>
    <td>name</td>
    <td>product.name</td>
    <td>STRING</td>
    <td>String</td>
    <td>商品名称</td>
  </tr>
  <tr>
    <td>price</td>
    <td>product.price</td>
    <td>Number</td>
    <td>Decimal</td>
    <td>商品类价格</td>
  </tr>
  <tr>
    <td>picture</td>
    <td>product.picture</td>
    <td>STRING</td>
    <td>String</td>
    <td>商品图片地址</td>
  </tr>
  <tr>
    <td>stock</td>
    <td>product.stock</td>
    <td>Number</td>
    <td>Integer</td>
    <td>商品库存</td>
  </tr>
</table>


# 3.购物车模块
## 3.1存储设计
### 3.1.1存储方式
Redis。key为手机号+"_cart_info"，value为Cart_info对象。
### 3.1.2购物车字段设计
```
# 定义Cart_info对象，Redis里的购物车类:
class Cart_info:
    def __init__(self, product_list, amount):
        self.product_list = product_list     # 购物车中商品列表
        self.amount = amount            # 合计总金额
```

## 3.2接口
### 3.2.1获取购物车
/cart/cart
根据输入的手机号返回该用户的购物车里的商品。
#### 3.2.1.1输入参数
<table>
  <tr>
    <th>节点</th>
    <th>节点路径</th>
    <th>节点类型</th>
    <th>后台类型</th>
    <th>是否必须</th>
    <th>说明</th>
  </tr>
  <tr>
    <td>phone_num</td>
    <td>phone_num</td>
    <td>STRING</td>
    <td>String</td>
    <td>是</td>
    <td>手机号</td>
  </tr>
</table>

#### 1.3.1.2输出参数
<table>
  <tr>
    <th>节点</th>
    <th>节点路径</th>
    <th>节点类型</th>
    <th>后台类型</th>
    <th>说明</th>
  </tr>
  <tr>
    <td>product</td>
    <td>product</td>
    <td>Object</td>
    <td>List&lt;Product&gt;</td>
    <td>商品列表</td>
  </tr>
  <tr>
    <td>id</td>
    <td>product.id</td>
    <td>Number</td>
    <td>Integer</td>
    <td>商品类id</td>
  </tr>
  <tr>
    <td>name</td>
    <td>product.name</td>
    <td>STRING</td>
    <td>String</td>
    <td>商品名称</td>
  </tr>
  <tr>
    <td>price</td>
    <td>product.price</td>
    <td>Number</td>
    <td>Decimal</td>
    <td>商品类价格</td>
  </tr>
  <tr>
    <td>buyCount</td>
    <td>product.buyCount</td>
    <td>Number</td>
    <td>Integer</td>
    <td>商品购买数</td>
  </tr>
</table>

### 3.2.2往购物车增加商品
/cart/add_to_cart
根据输入的手机号往该用户的购物车里增加商品。

#### 3.2.2.1输入参数
<table>
  <tr>
    <th>节点</th>
    <th>节点路径</th>
    <th>节点类型</th>
    <th>后台类型</th>
    <th>是否必须</th>
    <th>说明</th>
  </tr>
  <tr>
    <td>phone_num</td>
    <td>phone_num</td>
    <td>STRING</td>
    <td>String</td>
    <td>是</td>
    <td>手机号</td>
  </tr>
  <tr>
    <td>product_id</td>
    <td>product_id</td>
    <td>STRING</td>
    <td>String</td>
    <td>是</td>
    <td>商品id</td>
  </tr>
</table>

#### 3.2.2.2输出参数
<table>
  <tr>
    <th>节点</th>
    <th>节点路径</th>
    <th>节点类型</th>
    <th>后台类型</th>
    <th>说明</th>
  </tr>
  <tr>
    <td>error_code</td>
    <td>error_code</td>
    <td>STRING</td>
    <td>String</td>
    <td>错误码</td>
  </tr>
  <tr>
    <td>error_message</td>
    <td>error_message</td>
    <td>STRING</td>
    <td>String</td>
    <td>错误信息</td>
  </tr>
</table>



# 4.订单模块
## 4.1存储设计
### 4.1.1存储方式
Mysql。
### 4.1.2订单表设计
```
create table t_order
(
	id int auto_increment primary key,		-- 自增id  主键
	user_id int,							-- 用户id
	status tinyint,                         -- init:未审核,pass:已审核,send:已发货,sign:已签收,cancel:已取消,file:已归档
	quantity int,							-- 商品总数量
	amount decimal(6,2),                   -- 订单总金额
	ptotal decimal(6,2),   				    -- 商品总金额
	fee decimal(6,2)	                    -- 运费总金额
)
```

### 4.1.3订单明细表设计
```
create table order_detail
(
	id int auto_increment primary key,      -- 自增id  主键      
	order_id  int,                          -- 订单编号
	product_id  int,                        -- 商品id
	price decimal(6,2),						-- 价格
	quantity int,							-- 数量
	total decimal(6,2),						-- 总金额（数量*价格）
	fee decimal(6,2),  		                -- 配送费
	isComment char(1)                       -- 是否评价过                    
)
```
## 4.2业务流程
## 4.3接口
### 4.3.1创建订单接口
/order/pay
根据用户的购物车的商品列表创建订单表和订单明细表。

#### 4.3.1.1输入参数
<table>
  <tr>
    <th>节点</th>
    <th>节点路径</th>
    <th>节点类型</th>
    <th>后台类型</th>
    <th>是否必须</th>
    <th>说明</th>
  </tr>
  <tr>
    <td>user_id</td>
    <td>user_id</td>
    <td>NUMBER</td>
    <td>Integer</td>
    <td>用户id</td>
  </tr>
</table>

#### 2.3.1.2输出参数
<table>
  <tr>
    <th>节点</th>
    <th>节点路径</th>
    <th>节点类型</th>
    <th>后台类型</th>
    <th>说明</th>
  </tr>
  <tr>
    <td>catagory</td>
    <td>catagory</td>
    <td>Object</td>
    <td>List&lt;Product_category&gt;</td>
    <td>商品类列表</td>
  </tr>
  <tr>
    <td>id</td>
    <td>catagory.id</td>
    <td>NUMBER</td>
    <td>Integer</td>
    <td>商品类id</td>
  </tr>
  <tr>
    <td>name</td>
    <td>catagory.name</td>
    <td>STRING</td>
    <td>String</td>
    <td>商品类名称</td>
  </tr>
  <tr>
    <td>category_order</td>
    <td>catagory.category_order</td>
    <td>STRING</td>
    <td>String</td>
    <td>商品类顺序</td>
  </tr>
  <tr>
    <td>children</td>
    <td>catagory.children</td>
    <td>Object</td>
    <td>List&lt;Product_category&gt;</td>
    <td>商品类的子类列表</td>
  </tr>
  <tr>
    <td>id</td>
    <td>catagory.children.id</td>
    <td>NUMBER</td>
    <td>Integer</td>
    <td>商品子类id</td>
  </tr>
  <tr>
    <td>name</td>
    <td>catagory.children.name</td>
    <td>STRING</td>
    <td>String</td>
    <td>商品子类名称</td>
  </tr>
  <tr>
    <td>category_order</td>
    <td>catagory.children.category_order</td>
    <td>STRING</td>
    <td>String</td>
    <td>商品子类顺序</td>
  </tr>
  <tr>
    <td>children</td>
    <td>catagory.children.children</td>
    <td>Object</td>
    <td>List&lt;Product_category&gt;</td>
    <td>商品子类的子类列表</td>
  </tr>
  <tr>
    <td>......</td>
    <td>......</td>
    <td>......</td>
    <td>......</td>
    <td>......</td>
  </tr>
</table>
