# account.py

# 사용자 정의 예외
class InsufficientFundsError(Exception):
    pass

# 계좌 클래스
class Account:
    def __init__(self, logger):
        self.balance = 0
        self.logger = logger  # 거래 기록기 (개발 안됨)

    def deposit(self, amount):
        self.balance += amount
        self.logger.log(f"Deposited {amount}")
        return self.balance

    def withdraw(self, amount):
        if self.balance < amount:
            self.logger.log("Withdrawal failed: insufficient funds")
            raise InsufficientFundsError("잔액 부족")
        
        self.balance -= amount
        self.logger.log(f"Withdrew {amount}")
        return self.balance