#CH.23 SQL 데이터베이스
import uvicorn as uvicorn

if __name__ == '__main__':
        uvicorn.run('main:app',
                    host='192.168.19.125',
                    port=4300,
                    )