import yaml
import utils
import os
from pathlib import Path
from fastapi import FastAPI, HTTPException
import uvicorn
from ament_index_python.packages import get_package_share_directory


app = FastAPI()

maps_pkg_name = 'test_building_maps'

try:
    MAPS_DIR = get_package_share_directory(maps_pkg_name)
except Exception as e:
    # На случай, если пакет ROS не засорсен в терминале
    MAPS_DIR = None 


@app.get("/coords/{map_name}")
def get_vertices(map_name:str):
 
    try:
        return utils.get_points(map_name, MAPS_DIR, maps_pkg_name)
    
    except utils.MapPackageNotFoundError as e:
        # Пакет не найден — это внутренняя ошибка сервера (500)
        raise HTTPException(
            status_code=500, 
            detail=str(e)
        )
        
    except utils.MapFileNotFoundError as e:
        # Карта не найдена — ошибка клиента (404)
        raise HTTPException(
            status_code=404, 
            detail=str(e)
        )

@app.get("/maps")
def get_maps():

    maps_path = Path(os.path.join(MAPS_DIR, 'maps'))
    maps = []
    for map in maps_path.iterdir():
        if map.is_dir() and map.name != 'assets':
            maps.append(map.name)

    return maps

def main():
    uvicorn.run(app, host="0.0.0.0", port=8080)

if __name__ == "__main__":
    main()