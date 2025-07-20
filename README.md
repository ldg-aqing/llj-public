# 🧠 基于AI的演讲互动智能出题系统

## 📌 What's it?

**PopQuiz（llj-public）** 是一个基于 Django 和 AI 的智能问答系统，旨在提升讲度、演讲、培训等场景下的互动性与反馈效率。

它解决的问题包括：

* 自动从 PDF/PPT 中提取文字内容；
* 结合 AI 模型自动生成选择题，节省人工出题时间；
* 让听众在讲度中通过答题和反馈即时参与；
* 提供多角色支持（组织者 / 演讲者 / 听众）；
* 提供答题数据与反馈结果的存储与统计。

---

## ⚙️ How to Use

### ✅ 1. 克隆项目

```bash
git clone https://github.com/ldg-aqing/llj-public.git
cd llj-public
```

### ✅ 2. 创建虚拟环境并安装依赖

```bash
python -m venv .venv
# Windows:
.venv\Scripts\activate
# macOS/Linux:
source .venv/bin/activate

pip install -r requirements.txt
```

### ✅ 3. 配置 `.env` 文件

在项目根目录下新建 `.env` 文件，填写你的配置信息：

```env
SECRET_KEY=your-secret-key
```


### ✅ 4. 初始化数据库

确保远程数据库已创建后执行：

```bash
python manage.py makemigrations
python manage.py migrate
```

### ✅ 5. 创建超级管理员（用于登录后台）

```bash
python manage.py createsuperuser
```

按提示设置用户名、密码、邮箱。

### ✅ 6. 启动服务

```bash
python manage.py runserver 0.0.0.0:8000
```

然后使用浏览器访问：

* `http://localhost:8000/`（本机）
* `http://<你的局域网IP>:8000/`（其他设备）

---

## 🧠 AI 出题支持

当前项目支持通过调用大型语言模型（如通义千问）进行选择题自动生成。AI 模块将自动分析上传内容并生成：

* 题干
* 4 个选项（A\~D）
* 正确答案
* 题目解析

---

## 🤝‍ Who Contributes?

| 姓名  | 角色    | 职责                         |
| --- | ----- | -------------------------- |
| 李俗杰 | 数据库/AI | AI 出题、数据库连接、远程部署 |
| 罗东果 | 后端开发  |       后端逻辑、接口设计            |
| 靖名成 | 前端开发  |    页面设计、美化与交互实现         |

---


## 📩 联系方式

欢迎通过 GitHub Issue 提问或提出建议，欢迎贡献代码和优化建议！
