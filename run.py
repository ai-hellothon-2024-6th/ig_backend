# run.py
import uvicorn
import sys

if __name__ == "__main__":
    port = 8000  # 기본 포트
    if len(sys.argv) > 1:
        try:
            port = int(sys.argv[1])  # 명령줄 인수로 포트를 전달받음
        except ValueError:
            print("포트는 정수여야 합니다. 기본 포트 8000을 사용합니다.")

    uvicorn.run("src.app:app", host="0.0.0.0", port=port, reload=True)