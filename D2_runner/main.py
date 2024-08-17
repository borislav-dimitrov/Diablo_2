from gui import App
from managers import DataMgr

def main_func():
    data_mgr = DataMgr()
    app = App(data_manager=data_mgr)
    app.run()

if __name__ == '__main__':
    main_func()
