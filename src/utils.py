import softwareSettings
import flet as ft
import json


#页面跳转用的函数
def change_route(page:ft.Page, route):
    page.views.clear()
    if route == "/settings":
        page.views.append(softwareSettings.Settings_page(page))
    elif route == "/":
        # 延迟导入，避免循环依赖
        from home import Homepage_view
        page.views.append(Homepage_view(page))
    page.update()
    pass

class SoftwareSettings :
    #初始化，尝试读取设置
    def __init__(self) -> None:
        try :
            with open("config.json","r") as f:
                app_config = json.load (f)
            pass
        except:
          pass 
        

    def loadSettings(self):
        with open("config.json","r") as f:
            app_config = json.load (f)
    
    pass

def audioPlayControl(e):
    pass

class AppTTSModule ():
#tts模块

    def ttsOutput(self, text: str) :
        pass