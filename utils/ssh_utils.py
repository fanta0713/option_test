import paramiko
from utils.logging_config import logger

class SSHClient:
    def __init__(self, ssh_info):
        self.hostname = ssh_info['hostname']
        self.port = ssh_info['port']
        self.username = ssh_info['username']
        self.password = ssh_info['password']
        self.ssh = paramiko.SSHClient()
        self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    def connect(self):
        try:
            self.ssh.connect(self.hostname, port=self.port, username=self.username, password=self.password)
            logger.info(f"成功连接到 {self.hostname}")
            return True
        except Exception as e:
            logger.error(f"连接失败: {e}")
            return False

    def execute_command(self, command):
        if self.connect():
            try:
                stdin, stdout, stderr = self.ssh.exec_command(command)
                output = stdout.read().decode()
                error = stderr.read().decode()
                if error:
                    logger.error(f"命令执行出错: {error}")
                self.ssh.close()
                logger.debug(f"执行命令：{command}")
                logger.debug(f"返回信息：{output}")
                return output
            except Exception as e:
                logger.error(f"执行命令时出错: {e}")
        return None