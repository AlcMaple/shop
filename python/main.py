from register import app
from flask_cors import CORS

if __name__ == '__main__':
    # 通过CORS，所有的来源都允许跨域访问
    CORS(app, resources=r'/*')
    # 接受任何ip地址的访问，并且使用多线程，设置接口为8081，不启动debug模式
    # 通过调用Flask应用的实例app的run方法来启动
    app.run(host="0.0.0.0", threaded=True, port=8081, debug=False)