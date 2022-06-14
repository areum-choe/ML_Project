# todo [Fast API] Fast API 배우기 15부 - Request Files
from typing import List
import uvicorn as uvicorn
from fastapi import FastAPI, File, UploadFile
from fastapi.responses import HTMLResponse

app = FastAPI()

# File클래스는 앞서배운 Form 클래스를 상속한다.
# File 클래스를 이용하면 클라이언트가 업로드하는 file을 다룰 수 있다. 그러므로 file들은 form data로 업로드 된다.
# file 을 bytes로 받아서 그 길이를 알려주는 것
# 경로 작업 함수 매개변수의 유형을 바이트로 선언하면 FastAPI가 파일을 읽고 내용을 바이트로 받게 됩니다.

# @app.post("/files/")
# async def create_file(file: bytes = File(...)):
#     return {"file_size": len(file)}
#
#
# #TODO UploadFile다음과 같은 속성이 있습니다.
# # filename(파일 이름), content_type(유형),
# # 이미지나 비디오혹은 큰사이즈의 파일들을 메모리를 전부다 사용하지 않고 처리할 수 있다
#
# @app.post("/uploadfile/")
# async def create_upload_file(file: UploadFile):
#     return {"filename": file.filename}

# todo 파일 여러개
# @app.post("/files/")
# async def create_files(files: List[bytes] = File(...)):
#     return {"file_sizes": [len(file) for file in files]}


# @app.post("/uploadfiles/")
# async def create_upload_files(files: List[UploadFile] = File(...)):
#     return {"filenames": [file.filename for file in files]}

@app.get("/")
async def main():
    content = """
<body>
<form action="/files/" enctype="multipart/form-data" method="post">
<input name="files" type="file" multiple>
<input type="submit">
</form>
<form action="/uploadfiles/" enctype="multipart/form-data" method="post">
<input name="files" type="file" multiple>
<input type="submit">
</form>
</body>
    """
    return HTMLResponse(content=content)

if __name__ == '__main__':
        uvicorn.run('main:app',
                    host='192.168.19.125',
                    port=4300,
                    )


