import aiohttp
from PIL import Image, ImageFile
import cv2
import io
import numpy as np
import time
import logging
import asyncio
from app.models import db, DBfunc, Filefunc
from config.config import FPS, WANTED_TIME, VIDEO_DIR, W, H, TIME_BEFORE_START
from app.compress_video import compress_video
import os
ImageFile.LOAD_TRUNCATED_IMAGES = True

fFunc = Filefunc()
dbFunc = DBfunc()
logger = logging.getLogger(__name__)

def get_time_format():
    localtime = time.localtime()
    return f"[{localtime.tm_year}_{localtime.tm_mon}_{localtime.tm_mday} - {localtime.tm_hour}_{localtime.tm_min}_{localtime.tm_sec}]"

async def capture(bot):
    await asyncio.sleep(2)
    while 1:
        try:
            #r = requests.get("http://192.168.31.7/rr_connect?password=")
            printer_url = await dbFunc.get_root()
            id = printer_url.chat_id
            url = printer_url.camera_ip
            printer_url = printer_url.printer_ip
            async with aiohttp.ClientSession() as session:
                async with session.get(printer_url+"/rr_connect?password=") as resp:
                    ...          
                async with session.get(printer_url+"/rr_model?key=state") as resp:
                    r = await resp.json()
                    status = r['result']["status"]
                async with session.get(printer_url+"/rr_fileinfo") as resp:    
                    r = await resp.json()
                a = r['printTime'] - r['printDuration'] + TIME_BEFORE_START
                if(status != "processing"):
                    raise Exception("Not printing")
                name = (r['fileName'].split("/")[-1]).split('.')[0]
                logger.info(f"Start timelapse for {name}")
                frames = FPS * WANTED_TIME
                time_to_sleep = a/frames
                img_url = f"{url}/shot.jpg"
                output_file = f"{get_time_format()}{name}_{str(frames)}.mp4"
                fourcc = cv2.VideoWriter_fourcc(*'mp4v')
                out = cv2.VideoWriter(VIDEO_DIR+output_file, fourcc, FPS, (W, H))
                for i in range(frames):
                    async with session.get(printer_url+"/rr_model?key=state") as resp:
                        r = await resp.json()
                        status = r['result']["status"]
                        if(status != "processing"):
                            break
                    st = time.time()
                    async with session.get(img_url) as resp:
                        image_bytes = await resp.read()
                        image = Image.open(io.BytesIO(image_bytes))
                        frame = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
                        out.write(frame)
                    en = time.time() - st
                    if time_to_sleep > en:
                        await asyncio.sleep(time_to_sleep - en)
                    logger.info(f"Captured {i} frame")
            
                # Release the VideoWriter
                out.release()
                logger.info(f"Wideo dumped")
                try:
                    filename = await compress_video(VIDEO_DIR+output_file, 50*1000)
                    os.remove(VIDEO_DIR+output_file)
                    output_file = filename.split(VIDEO_DIR)[-1]
                except Exception as e:
                    logger.info(f"Error: {e}")
                await fFunc.add(output_file)

        except Exception as e:
            logger.debug(f"Waiting print")
            await asyncio.sleep(5)