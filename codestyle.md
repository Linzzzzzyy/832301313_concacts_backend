技术栈：Python + Flask + SQLAlchemy + SQLite

目录结构示例：

|-832301313_concacts_backend

 
​ |- src

​ |- concacts..py...
 
|- README.md

 
|- codestyle.md

一、总体原则

遵循 PEP 8 Python 代码风格。

使用 Flask 官方推荐实践。

保持单一职责：每个函数只处理一类业务逻辑。

使用自动化工具（Black、Flake8）在提交或 CI 中统一风格。

二、文件与命名规范

文件名：全部小写，使用下划线分隔 (snake_case)。

类名：首字母大写的 PascalCase（如 User、Contact）。

函数/方法名：snake_case。

变量名：snake_case，常量全部大写（如 DB_URI）。

模块划分：

app.py：程序入口，注册路由和初始化扩展。

models/：存放 SQLAlchemy 模型。

controller/：路由逻辑处理。

utils/：工具函数，如 CSV 导出、加密、通用验证。

tests/：单元测试。

三、代码风格

缩进：4 个空格。

行长度：不超过 79 个字符。

空行：

顶级函数和类之间使用两行空行。

类内方法之间使用一行空行。

导入顺序：

Python 标准库

第三方库（Flask, SQLAlchemy）

本地模块（models, utils, controller）

使用 type hint 增加可读性，例如：

def add_contact(name: str, phone: str, user_id: int) -> dict:

四、Flask 特定约定

使用蓝图（Blueprints）组织路由，如果项目增大。

路由函数尽量短小，复杂逻辑应放在 models 或 utils 中。

使用 @app.route(..., methods=[...]) 明确 HTTP 方法。

对 JSON 请求使用 request.get_json()，对响应使用 jsonify()。

API 返回规范：

{
    "success": true/false,
    "message": "描述信息",
    "data": {...}  # 可选
}

五、数据库与模型

使用 SQLAlchemy ORM。

类名 PascalCase，字段命名 snake_case。

外键字段使用 ForeignKey，命名形如 <related_table>_id。

不在路由函数中直接写复杂查询，使用模型方法或服务层封装。

六、错误处理与日志

避免打印敏感信息（密码、Token）。

使用统一返回格式展示错误信息。

可使用 Python logging 模块记录错误：

import logging
logging.basicConfig(level=logging.INFO)
logging.error("错误信息")

七、CSV 导出与文件处理

使用 with open(...) as f 语句，确保文件正确关闭。

文件名与用户 ID 相关，避免覆盖其他用户数据。

使用 send_file() 直接返回浏览器下载。

八、测试

使用 pytest 进行单元测试。

路由测试可使用 Flask 提供的 test_client()。

测试文件存放在 tests/，文件命名 test_*.py。

测试内容包括：注册、登录、联系人增删改查、导出功能。

九、工具链与格式化

格式化工具：

Black：black .

Flake8：flake8 .

在 CI / Git 提交前运行格式化和 lint 检查。

十、代码审查重点

命名是否清晰，函数职责是否单一？

是否处理异常和错误情况？

是否有单元测试覆盖主要功能？

是否遵循 PEP 8 和 Flask 最佳实践？

十一、参考资料

PEP 8 Python 风格指南
https://peps.python.org/pep-0008/

Flask 官方文档
https://flask.palletsprojects.com/

SQLAlchemy 官方文档
https://docs.sqlalchemy.org/
Python Logging 文档
https://docs.python.org/3/library/logging.html
