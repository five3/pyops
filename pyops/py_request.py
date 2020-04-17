
class PyRequest:
    def __init__(self, req):
        # 原生的pytest request对象
        self.req = req
        # 保存单个测试类中的全局变量
        self.env_config = req.config.ah_class_config

    def get_global(self, key):
        return self.env_config.get(key)

    def set_global(self, key, value):
        self.env_config[key] = value

    def del_global(self, key):
        if key in self.env_config:
            del self.env_config[key]

    def clear_global(self):
        self.env_config = {}
