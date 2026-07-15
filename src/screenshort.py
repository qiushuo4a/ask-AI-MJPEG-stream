import requests
from PIL import Image
from io import BytesIO

def extract_mjpeg_frame_no_ffmpeg(stream_url, output_path="~/"):

    # 1. 建立流连接，禁用缓存确保获取最新帧
    response = requests.get(stream_url, stream=True, headers={"Cache-Control": "no-cache"})
    response.raise_for_status()  # 若连接失败直接抛异常

    # 2. 解析MJPEG流边界（HTTP响应头中获取）
    content_type = response.headers.get("Content-Type", "")
    if "multipart/x-mixed-replace" not in content_type:
        raise ValueError("目标地址非标准MJPEG流")
    # 提取分隔符（如 boundary=--abc123），去掉前缀
    boundary = content_type.split("boundary=")[-1].encode("utf-8")

    # 3. 逐段读取数据，提取第一帧JPEG
    frame_data = b""
    for chunk in response.iter_content(chunk_size=1024):
        if chunk:
            frame_data += chunk
            # 检测到边界分隔符，说明已获取完整一帧
            if boundary in frame_data:
                # 截取JPEG数据（去掉分隔符及头部信息）
                jpeg_start = frame_data.find(b"\xff\xd8")  # JPEG文件起始标识
                jpeg_end = frame_data.find(b"\xff\xd9")    # JPEG文件结束标识
                if jpeg_start != -1 and jpeg_end != -1:
                    jpeg_data = frame_data[jpeg_start:jpeg_end + 2]
                    # 4. 用PIL解析JPEG并保存为PNG
                    # with Image.open(BytesIO(jpeg_data)) as img:
                    #     img.save(output_path, "PNG")
                    # print(f"成功保存帧至：{output_path}")
                    break  # 只取第一帧，跳出循环
    response.close()  # 关闭连接
    return jpeg_data  # type: ignore

def get_image_by_adb():
    pass

if __name__ == "__main__" :
    img_data= extract_mjpeg_frame_no_ffmpeg("http://192.168.31.112:8080/stream.mjpeg")
    with Image.open(BytesIO(img_data)) as img:
        img.save("~", "PNG")

