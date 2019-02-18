import redis
from flask import Flask, render_template
from flask_script import Manager
from flask_session import Session

from app.home_views import home_blue
from app.models import db
from app.order_vierws import order_blue
from app.user_views import user_blue, login_manage

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


app.register_blueprint(blueprint=user_blue, url_prefix='/user')
app.register_blueprint(blueprint=home_blue, url_prefix='/home')
app.register_blueprint(blueprint=order_blue, url_prefix='/order')

# 初始化数据库配置
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:123456@127.0.0.1:3306/ihome'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

# 设置加密的复杂程度
app.secret_key = '789123adswetyjv'

# 配置存储的数据库:
app.config['SESSION_TYPE'] = 'redis'
app.config['SESSION_REDIS'] = redis.Redis(host='47.106.233.124', port=6379, password=123456)
se = Session()
se.init_app(app)

# 配置login
login_manage.login_view = 'user.login'
login_manage.init_app(app)

# 管理flask应用对象
manager = Manager(app)

if __name__ == '__main__':
    manager.run()
