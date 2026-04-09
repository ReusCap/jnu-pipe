import unittest
from unittest.mock import Mock
from account import Account

class TestAccountWithMock(unittest.TestCase):
    def setUp(self):
        self.mock_logger = Mock()  # Mock으로 대체
        self.account = Account(self.mock_logger)

    def test_deposit_calls_logger(self):
        self.account.deposit(200)
        # assert_called_with(인자) = 마지막 호출 시 인자와 동일한지 확인
        self.mock_logger.log.assert_called_with("Deposited 200")

    def test_withdraw_calls_logger(self):
        self.account.deposit(100)
        self.account.withdraw(50)
        # assert_any_call(인자) = 여러 번 호출됐을 때, 호출 내역 중 인자가 일치하는지
        self.mock_logger.log.assert_any_call("Withdrew 50")

if __name__ == "__main__":
    unittest.main(verbosity=2)