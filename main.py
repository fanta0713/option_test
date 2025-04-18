import pytest
import os
# import logger

# 获取项目根目录
project_root = os.path.dirname(os.path.abspath(__file__))
test_file = os.path.join(project_root, 'testcase\gpu', 'test_01_gpu_state_infomation_check.py')

if __name__ == "__main__":
    pytest.main(["-s", test_file])