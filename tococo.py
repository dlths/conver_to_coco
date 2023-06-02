import json
import os


def get_all_files_in_directory(directory, extension=".json"):
    file_list = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith(extension):
                file_path = os.path.join(root, file)
                file_list.append(file_path)
    return file_list

# 주어진 폴더에서 파일 목록 가져오기
folder_path = "datasets/weed/JPEGImages"  # 실제 폴더 경로로 수정해야 합니다.
file_list = get_all_files_in_directory(folder_path, extension=".json")
#print(file_list)

# 변환된 COCO 형식의 딕셔너리
coco_data = {
    "info": {},
    "licenses": [],
    "images": [],
    "annotations": [],
    "categories": []
}

category_mapping = {
    0 : "정상", 
    1 : "고추탄저병", 
    2 : "고추흰가루병", 
    3 : "무검은무늬병",
    4 : "무노균병",
    5 : "배추검음썩음병",
    6 : "배추노균병",
    7 : "애호박노균병",
    8 : "애호박흰가루병", 
    9 : "양배추균핵병",
    10 : "양배추무름병",
    11 : "오이노균병", 
    12 : "오이흰가루병", 
    13 : "콩불마름병", 
    14 : "콩점무늬병",
    15 : "토마토잎마름병", 
    16 : "파검은무늬병",
    17 : "파노균병", 
    18 : "파녹병", 
    19 : "호박노균병", 
    20 : "호박흰가루병"
}

image_id = 1  # 이미지의 고유 ID 초기값
annotation_id = 1  # 주석의 고유 ID 초기값

# 파일 목록에 대해 변환 작업 수행
for file_path in file_list:
    # 파일 내용을 읽어와서 json_data 변수에 저장
    with open(file_path, "r") as file:
        json_data = file.read()

    try:
        # JSON 데이터를 딕셔너리로 로드
        data = json.loads(json_data)

        # 이미지 정보 추가
        image_info = {
            "id": image_id,
            "file_name": data["description"]["image"],
            "date_captured": data["description"]["date"],
            "height": data["description"]["height"],
            "width": data["description"]["width"],
            "task": data["description"]["task"],
            "type": data["description"]["type"],
            "region": data["description"]["region"]
        }
        coco_data["images"].append(image_info)

        # 주석(어노테이션) 정보 추가
        annotation_info = {
            "id": annotation_id,
            "image_id": image_id,
            "category_id": category_mapping.get(data["annotations"]["disease"], 0),
            "segmentation": [],
            "area": data["annotations"]["area"],
            "bbox": [
                data["annotations"]["points"][0]["xtl"],
                data["annotations"]["points"][0]["ytl"],
                data["annotations"]["points"][0]["xbr"] - data["annotations"]["points"][0]["xtl"],
                data["annotations"]["points"][0]["ybr"] - data["annotations"]["points"][0]["ytl"]
            ],
            "iscrowd": 0
        }
        coco_data["annotations"].append(annotation_info)

        # 카테고리 정보 추가
        category_info = {
            "id": category_mapping.get(data["annotations"]["disease"], 0),
            "name": category_mapping.get(data["annotations"]["disease"], 0),
            "supercategory": "plant"
        }
        coco_data["categories"].append(category_info)

        image_id += 1
        annotation_id += 1

    except KeyError as e:
        print(f"KeyError: {e} - Invalid JSON format in file: {file_path}")

    except json.JSONDecodeError as e:
        print(f"JSONDecodeError: {e} - Unable to decode JSON in file: {file_path}")

    except Exception as e:
        print(f"Error: {e} - An error occurred while processing file: {file_path}")

# 변환된 COCO 형식의 딕셔너리를 JSON 파일로 저장
output_file_path = "weed_coco_data_new.json"  # 저장할 파일 경로와 이름 지정
with open(output_file_path, "w", encoding="utf-8") as outfile:
    json.dump(coco_data, outfile, ensure_ascii=False)
