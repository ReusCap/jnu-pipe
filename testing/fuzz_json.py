# fuzz_json.py
from hypothesis import given, strategies as st
import json

# 테스트할 대상 함수 (예: 외부 입력을 JSON으로 파싱하고 특정 키를 기대)
def process_input(s: str):
    # 실제 코드에서는 여기서 더 복잡한 처리(데이터베이스, 파일쓰기 등)가 들어갈 수 있음
    obj = json.loads(s)  # -> 여기가 취약점(예외 발생) 지점이 될 수 있음
    
    # if "action" not in obj:
    #     raise ValueError("no action")
    
    if obj.get("action") == "divide":
        # 잘못된 타입으로 인해 ZeroDivisionError 등 발생 가능
        a = obj.get("a", 1)
        b = obj.get("b", 1)
        return a / b
    return obj

# Hypothesis가 다양한 문자열을 생성해서 process_input에 넣음
@given(st.text())
def test_process_input(s):
    try:
        # print(s) # 필요 시 주석 해제하여 생성된 문자열 확인
        process_input(s)
    except (json.JSONDecodeError, ValueError, ZeroDivisionError, TypeError):
        # 예외 자체를 실패로 취급하지 않고, 어떤 예외가 나는지 확인하는 용도
        # 실제 퍼징 목적: 예외가 발생했을 때 원치 않는 크래시(예: interpreter crash)가 있는지 확인
        pass

if __name__ == "__main__":
    # Hypothesis 테스트는 일반 함수 호출이 아니라 pytest나 
    # unittest와 연동하거나, 직접 실행 시 내부 로직을 통해 구동됩니다.
    test_process_input()  # Hypothesis가 자동으로 여러 사례를 생성하여 실행