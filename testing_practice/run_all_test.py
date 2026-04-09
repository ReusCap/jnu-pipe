import unittest
from test_add import TestAdd
from test_subtract import TestSubtract

# 테스트 스위트 생성
suite = unittest.TestSuite()

# 테스트 클래스 전체 추가
loader = unittest.TestLoader()
suite.addTest(loader.loadTestsFromTestCase(TestAdd))
suite.addTest(loader.loadTestsFromTestCase(TestSubtract))

# 테스트 실행기 생성
runner = unittest.TextTestRunner()
runner.run(suite)