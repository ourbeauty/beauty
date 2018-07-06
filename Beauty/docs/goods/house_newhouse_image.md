
### 新房源房屋图片上传接口

#### request 请求

    post /house/images/

#### params 参数

    house_image file 图片地址
    house_id int 房屋id

#### response 响应

##### 响应1：

    {'code': 900, 'msg': '数据库访问失败'}

##### 响应2：

    {'code': 200,'image_url':/static/upload/a1.jpg}



