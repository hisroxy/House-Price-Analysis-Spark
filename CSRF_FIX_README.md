[//]: # (# CSRF验证失败问题修复说明)

[//]: # ()
[//]: # (## 问题描述)

[//]: # (用户在提交个人信息修改时遇到403 Forbidden错误，提示"CSRF verification failed. Request aborted."，具体原因是CSRF令牌缺失或不正确。)

[//]: # ()
[//]: # (## 问题分析)

[//]: # (1. **根本原因**：Django启用了CSRF保护中间件，但前端发送PUT请求时未正确携带CSRF令牌)

[//]: # (2. **影响范围**：用户无法保存个人信息修改)

[//]: # (3. **错误表现**：403 Forbidden响应，CSRF token missing or incorrect)

[//]: # ()
[//]: # (## 解决方案)

[//]: # ()
[//]: # (### 方案一：前端配置修复（主要方案）)

[//]: # (**文件**：`frontend/src/main.js`)

[//]: # ()
[//]: # (**修改内容**：)

[//]: # (```javascript)

[//]: # (// 配置CSRF令牌)

[//]: # (axios.defaults.xsrfCookieName = 'csrftoken')

[//]: # (axios.defaults.xsrfHeaderName = 'X-CSRFToken')

[//]: # ()
[//]: # (// 请求拦截器 - 自动添加CSRF令牌)

[//]: # (axios.interceptors.request.use&#40;)

[//]: # (  config => {)

[//]: # (    // 从cookie中获取CSRF令牌)

[//]: # (    const csrfToken = getCookie&#40;'csrftoken'&#41;)

[//]: # (    if &#40;csrfToken&#41; {)

[//]: # (      config.headers['X-CSRFToken'] = csrfToken)

[//]: # (    })

[//]: # (    return config)

[//]: # (  },)

[//]: # (  error => {)

[//]: # (    return Promise.reject&#40;error&#41;)

[//]: # (  })

[//]: # (&#41;)

[//]: # ()
[//]: # (// 获取cookie的辅助函数)

[//]: # (function getCookie&#40;name&#41; {)

[//]: # (  let cookieValue = null)

[//]: # (  if &#40;document.cookie && document.cookie !== ''&#41; {)

[//]: # (    const cookies = document.cookie.split&#40;';'&#41;)

[//]: # (    for &#40;let i = 0; i < cookies.length; i++&#41; {)

[//]: # (      const cookie = cookies[i].trim&#40;&#41;)

[//]: # (      if &#40;cookie.substring&#40;0, name.length + 1&#41; === &#40;name + '='&#41;&#41; {)

[//]: # (        cookieValue = decodeURIComponent&#40;cookie.substring&#40;name.length + 1&#41;&#41;)

[//]: # (        break)

[//]: # (      })

[//]: # (    })

[//]: # (  })

[//]: # (  return cookieValue)

[//]: # (})

[//]: # (```)

[//]: # ()
[//]: # (### 方案二：后端视图修复（备用方案）)

[//]: # (**文件**：`user/views.py`)

[//]: # ()
[//]: # (**修改内容**：)

[//]: # (```python)

[//]: # (@csrf_exempt  # 添加此装饰器)

[//]: # (@login_required)

[//]: # (@require_http_methods&#40;["PUT"]&#41;)

[//]: # (def update_user_info&#40;request&#41;:)

[//]: # (    # ... 原有代码 ...)

[//]: # (```)

[//]: # ()
[//]: # (## 技术原理)

[//]: # ()
[//]: # (### CSRF保护机制)

[//]: # (1. **Django CSRF中间件**：自动为每个用户会话生成CSRF令牌)

[//]: # (2. **令牌存储**：令牌存储在名为`csrftoken`的cookie中)

[//]: # (3. **令牌验证**：对于非GET请求，Django要求在请求头中包含`X-CSRFToken`)

[//]: # ()
[//]: # (### 前端实现要点)

[//]: # (1. **自动获取**：通过请求拦截器自动从cookie中提取CSRF令牌)

[//]: # (2. **自动添加**：将令牌添加到每个请求的headers中)

[//]: # (3. **兼容性**：同时配置axios的xsrf选项确保各种场景都能正常工作)

[//]: # ()
[//]: # (## 验证方法)

[//]: # ()
[//]: # (### 前端验证)

[//]: # (1. 打开浏览器开发者工具)

[//]: # (2. 查看Network面板中的请求头)

[//]: # (3. 确认请求包含`X-CSRFToken`头)

[//]: # ()
[//]: # (### 后端验证)

[//]: # (1. 检查Django日志中不再出现CSRF验证错误)

[//]: # (2. 用户能够正常保存个人信息修改)

[//]: # ()
[//]: # (## 测试步骤)

[//]: # ()
[//]: # (1. **登录系统**：使用有效账户登录)

[//]: # (2. **访问用户页面**：进入个人信息编辑页面)

[//]: # (3. **修改信息**：更改任意字段（如昵称、手机号等）)

[//]: # (4. **保存修改**：点击"保存修改"按钮)

[//]: # (5. **验证结果**：确认保存成功，无403错误)

[//]: # ()
[//]: # (## 注意事项)

[//]: # ()
[//]: # (1. **安全性**：此修复保持了CSRF保护的有效性)

[//]: # (2. **兼容性**：适用于所有类型的HTTP请求)

[//]: # (3. **维护性**：集中配置，便于后续维护)

[//]: # (4. **性能**：cookie读取开销极小，不影响性能)

[//]: # ()
[//]: # (## 相关文件)

[//]: # (- `frontend/src/main.js` - 前端axios配置)

[//]: # (- `user/views.py` - 后端用户信息更新视图)

[//]: # (- `user/models.py` - 用户数据模型)

[//]: # ()
[//]: # (## 版本信息)

[//]: # (- Django版本：3.2)

[//]: # (- Vue版本：2.6.14)

[//]: # (- Axios版本：0.24.0)