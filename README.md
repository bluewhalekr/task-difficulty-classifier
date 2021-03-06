# task-difficulty-classifier
AI-Assist 추론 결과를 활용한 BBOX 작업 난이도 분류 및 엑셀 추출 모듈



## Key Features

* 인스턴스 수: 파일 내 인스턴스의 수
* 평균 인스턴스 사이즈: 파일 내 인스턴스들의 이미지 사이즈 대비 비율(최대 5%로 Ceiling)
* 평균 폐색 정도: 파일 내 인스턴스들이 평균적으로 겹쳐진 수



## Example

<img width="920" alt="example" src="https://user-images.githubusercontent.com/69578563/156510750-989a2550-eb04-457b-8182-d3b1b4fc322e.png">

## Install

~~~bash
# git clone 후
pip install -r ./requirements.txt
~~~



## Usage

~~~bash
python classify.py -p ${root_path} -s ${width height} -d ${dst_path}
~~~



#### Options

* --root_path [-p] (str): AI-Assist 추론 결과 JSON 파일이 저장된 경로 Root (JSON per File)
* --task_size [-s] (int): 이미지 사이즈  
* --n_cpus [-n] (int): JSON Parsing 시 병렬처리에 사용할 CPU 수 (default: 1)
* --extract_ratio [-r] (float): 전체 파일 중 Difficulty & Easy Task의 비중 (default: 0.2)
* --dst_path [-d] (str): 엑셀파일 저장 경로 (ex. /home/project/project_title.xlsx)
* --title [-t] (str): 엑셀파일 제목 (default: Project Summary)