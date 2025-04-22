import tkinter as tk
from tkinter import filedialog
import os

def process_chat(input_file_path, output_file_path):
    try:
        with open(input_file_path, 'r', encoding='utf-8') as file:
            lines = file.readlines()

        current_user = None
        messages = []
        formatted_chat = []

        for line in lines:
            line = line.strip()
            if not line:  # 빈 줄 건너뛰기
                continue

            # 시간 정보가 있는 줄 처리
            if line[:2].isdigit() and ':' in line[:5]:
                line = line[6:].strip()  # 시간 제거

            # 먼저 parts 정의
            parts = line.split(' ')

            # 이름과 식별자가 분리된 경우를 처리 (예: "홍길동 m32" 또는 "김철수 사원" 등)
            if len(parts) >= 2 and parts[1].startswith('m'):
                user = f"{parts[0]} {parts[1]}"
                message_start = len(user)
                message = line[message_start:].strip()
            else:
                if len(parts) >= 2:
                    user = parts[0]
                    message = ' '.join(parts[1:])
                else:
                    continue

            # 새로운 사용자의 메시지인 경우
            if current_user != user:
                # 이전 사용자의 메시지들 저장
                if messages:
                    formatted_chat.append(f"{current_user}\n{'\n'.join(messages)}\n")
                    formatted_chat.append("\n")  # 사용자 간 빈 줄로 구분
                current_user = user
                messages = []
            
            if message:  # 메시지가 비어있지 않은 경우만 추가하기
                messages.append(message)

        # 마지막 사용자의 메시지
        if messages:
            formatted_chat.append(f"{current_user}\n{'\n'.join(messages)}\n")

        # 결과 파일 저장
        with open(output_file_path, 'w', encoding='utf-8') as file:
            file.write(''.join(formatted_chat))

        print("대화 내용이 성공적으로 처리되었습니다!")
        
    except Exception as e:
        print(f"오류가 발생했습니다: {str(e)}")

def main():
    # GUI 창 숨기기
    root = tk.Tk()
    root.withdraw()

    # 입력 파일 선택
    print("처리할 대화 파일을 선택해주세요.")
    input_file = filedialog.askopenfilename(
        title="처리할 대화 파일 선택",
        filetypes=(("텍스트 파일", "*.txt"), ("모든 파일", "*.*"))
    )

    if input_file:
        # 출력 파일 경로 설정
        directory = os.path.dirname(input_file)
        filename = os.path.splitext(os.path.basename(input_file))[0]
        output_file = os.path.join(directory, f"{filename}_정리됨.txt")

        # 출력 파일 저장 위치 선택
        output_file = filedialog.asksaveasfilename(
            initialfile=f"{filename}_정리됨.txt",
            defaultextension=".txt",
            filetypes=(("텍스트 파일", "*.txt"), ("모든 파일", "*.*")),
            title="저장할 파일 선택"
        )

        if output_file:
            process_chat(input_file, output_file)
            print(f"파일이 저장되었습니다: {output_file}")
        else:
            print("저장이 취소되었습니다.")
    else:
        print("파일 선택이 취소되었습니다.")

    root.destroy()

if __name__ == "__main__":
    main()