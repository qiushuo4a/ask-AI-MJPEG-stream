# __Author__ = "Qiushuo4a"
"""
更新计划
1.添加对剪切板图片的支持
2.支持本地图片并支持拖拽动作
3.加入对ADB截屏/SCRAPY的支持
"""
import flet as ft
import requests
from PIL import Image
import PIL.Image
from io import BytesIO
import io
from screenshort import extract_mjpeg_frame_no_ffmpeg
import utils
import base64
import doubaoAI
from flet import (
    Page, Column, Row, Container, Text, TextField, ElevatedButton,
    Dropdown, dropdown, Image, TextButton, alignment, Colors,
    MainAxisAlignment, CrossAxisAlignment, padding, margin
)

def Homepage_view(page:ft.Page) -> ft.View:



    def update_image(e):
        if stream_url_field.value == "":
            stream_url_field.label = " 请输入一个连接"
            stream_url_field.border_color = Colors.PINK_800
            stream_url_field.update()
            return None
        

        try :
            if stream_url_field.value != None:
                image_data = extract_mjpeg_frame_no_ffmpeg(stream_url_field.value) 
                image_data_base64 = base64.b64encode(image_data).decode("utf-8")
                print("已下载")
               
                f = open("C:\\Windows\\Temp\\screenview.jpeg","wb")
                f.write(image_data)
                f.close()

                image_container.content = image_display
                image_display.src = None
                image_display.src_base64 = image_data_base64
                image_container.update()

            else:
                Exception (ValueError)
        except :
            print("get图片时出错")
            image_container.content = Image(src="src\\assets\\image_error.jpg") 
            image_container.update()
            pass
            

    # 左侧区域
    # 视频流地址输入框
    stream_url_field =TextField(
                label="请输入MJPEG视频流地址",
                hint_text="例如: http://192.168.1.100:8080/stream.mjpeg",
                width=400,
                filled=True,
                bgcolor=Colors.WHITE,
                )
    def setDefaultURI(e):
        stream_url_field.value = "http://192.168.1.100:8080/stream.mjpeg"
        stream_url_field.update()

    #旋转图像功能的实现
    def rotateImg(e) :
        try:
            if image_display.src_base64:
                print("尝试base64旋转")
                # 去掉前缀，只解码纯 base64 部分
                img_base64 = image_display.src_base64
                image = PIL.Image.open(io.BytesIO(base64.b64decode(img_base64))).convert("RGB")
                image = image.rotate(90, expand=True)
                buf = io.BytesIO()
                image.save(buf, format="JPEG")
                image_base64 = base64.b64encode(buf.getvalue()).decode("utf-8")
                image_display.src_base64 = image_base64
                image_display.update()
                print("base64旋转成功")
            elif image_display.src:
                print("尝试src旋转")
                image = PIL.Image.open(image_display.src)
                image = image.rotate(90, expand=True)
                buf = io.BytesIO()
                image.save(buf, format="JPEG")
                image_base64 = base64.b64encode(buf.getvalue()).decode("utf-8")
                image_display.src_base64 = image_base64
                image_display.update()
                print("src旋转成功")
            else:
                print("旋转失败")
        except Exception as ex:
            print(f"旋转图片时出错: {ex}")
        pass

    #旋转图像的按钮
    btn_rotateImg =TextButton (
        content = Container(
                    content=Column(
                        [
                            ft.Icon(name=ft.Icons.ROTATE_90_DEGREES_CCW,),# size = ?
                            Text(
                                value="旋转",
                                size=12,
                                # width=100,
                                no_wrap=True,
                                text_align="center", # type: ignore
                                color=Colors.ON_SURFACE_VARIANT,
                            ),
                        ],
                        alignment="center",# type: ignore
                        horizontal_alignment="center",# type: ignore
                        ),
                        alignment=alignment.center,
                        
                    ),
                on_click=rotateImg,
                expand=False
                )
    

        #使用默认地址的按钮
    btn_using_default_uri =TextButton (
        content = Container(
                    content=Column(
                        [
                            ft.Icon(name=ft.Icons.TEXT_SNIPPET_OUTLINED,),# size = ?
                            Text(
                                value="默认值",
                                size=12,
                                # width=100,
                                no_wrap=True,
                                text_align="center",# type: ignore
                                color=Colors.ON_SURFACE_VARIANT,
                            ),
                        ],
                        alignment="center",# type: ignore
                        horizontal_alignment="center",# type: ignore
                        ),
                        alignment=alignment.center,
                        
                    ),
                on_click=setDefaultURI,
                )

    uri_controller=Row(
        controls=[
            stream_url_field,
            btn_using_default_uri,
            btn_rotateImg
        ]
    )



            # ft.CupertinoButton(
            #     text = "用默认",
            #     on_click = setDefaultURI,
            #     bgcolor=ft.Colors.GREY_100,
            #     width=60
            # ),


    image_display = Image()

    # 图片展示区（默认空白，使用与背景相近的颜色）
    image_container = Container(
        content=Container( # 内部容器用于占位
            
            content=Text("等待加载视频流...", color=Colors.GREY_500, size=16),
            alignment=alignment.center,
        ),
        width=540,
        height=400,
        bgcolor=Colors.GREY_200,  # 与背景相近但略有区别
        border_radius=8,
        alignment=alignment.center,
        expand=True,
    )

    left_column = Column(
        controls=[
            uri_controller,
            ft.Container(height=20),  # 间距
            image_container,
        ],
        expand=True,
    )


    # 右侧按钮区域
    # 创建带图标和文字的按钮
    def create_icon_button(icon_name, text, on_click=None):
        return ElevatedButton(
            content=Row(
                controls=[
                    ft.Icon(icon_name, size=18),
                    Text(text, size=14),
                ],
            ),
            on_click=on_click,
        )
    
    # 按钮点击事件处理函数
    def button_click_handler(e):
        print(f"按钮 '{e.control.content.controls[1].value}' 被点击")
    
    def askAI(e):
        # 拼接 Ark API 支持的 base64 格式
        if image_display.src_base64:
            img_base64_with_prefix = f"data:image/jpeg;base64,{image_display.src_base64}"
            answer = doubaoAI.aiAsk(img_base64_with_prefix)
            answer_text.value = str(answer)
            right_column.update()
        else:
            answer_text.value = "未获取到图片，请先获取图像。"
            right_column.update()
        pass

    def getAndUpload(e):
        update_image(0)
        askAI(0)

    def gotoSettingPage(e):
        page.go("/settings")

    # 创建普通按钮
    btn_get_img = ft.Button(icon=ft.Icons.PLAY_ARROW,text="获取图像",on_click=update_image) 
    btn_upload_img = ft.Button(icon=ft.Icons.FILE_UPLOAD,text="上传图像",on_click=askAI) 
    btn_get_and_upload_img = ft.Button(icon=ft.Icons.SEARCH,text="获取并上传",on_click=getAndUpload) 
    btn_goto_setting_page = ft.Button(icon=ft.Icons.SETTINGS,text="软件设置",on_click=gotoSettingPage) 
    
    right_buttons_row = Row(
        controls=[
            btn_get_img,
            btn_upload_img,
            btn_get_and_upload_img,
            btn_goto_setting_page
        ],
        
        wrap=True,
    )
    
    answer_text = ft.Text("等待操作...",size=20, color=Colors.GREY_700,selectable=True)

    # 右侧文本展示框
    # 创建第一行（标题行）和其余行的不同样式
    text_display = ft.ListView(
        controls=[
            # 第一行 - 标题样式
            Text(
                "识别结果",
                size=16,
                weight=ft.FontWeight.BOLD,
                color=Colors.BLUE_800,
                bgcolor=Colors.BLUE_50,
                text_align="center", # type: ignore
                expand=True,
            ),
            # 其余行 - 普通样式
            answer_text,
        ],
        height=300,
        spacing=2,
        auto_scroll=True,
        expand=True,
    )

    audio_play_controller = ft.Column(
        controls=[
            ft.Button(icon=ft.Icons.PLAYLIST_PLAY,text="播放",on_click=utils.audioPlayControl )
        ]
    )

    right_column = Column(
        controls=[
            right_buttons_row,
            ft.Container(height=20),  # 间距
            Container(
                content=text_display,
                border=ft.border.all(1, Colors.GREY_300),
                border_radius=8,
                padding=10,
                expand=True,
                bgcolor=Colors.WHITE,
            ),
            audio_play_controller,
        ],
        expand=True,
    )

    main_layout = Row(
        controls=[
            Container(
                content=left_column,
                expand=1,
                padding=10,
            ),
            Container(
                content=right_column,
                expand=1,
                padding=10,
            ),
        ],
        expand=True,
        spacing=20,
    )

    #页面总布局
    display_view= ft.View(
        "/",
        controls=[ main_layout

        ]
    )

    return display_view


def main(page: ft.Page):


    def mix_change_route(route):
        utils.change_route(page,route.route)

    
    page.on_route_change = mix_change_route


    page.go("/")

if __name__ == "__main__" :
    ft.app(main)

