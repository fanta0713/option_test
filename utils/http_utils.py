import requests
import json as complexjson
from utils.logging_config import logger


class ApiClient():

    def __init__(self, api_root_url, login_url, user_info):
        self.api_root_url = api_root_url
        self.session = requests.session()
        self.token = None
        self.login(login_url, user_info)

    def login(self, login_url, user_info):
        """
        登录方法，用于获取 token
        :param login_url: 登录接口的 URL
        :param user_info: 登录所需的用户信息
        """
        url = f"{self.api_root_url}/{login_url}"
        data = complexjson.dumps(user_info)
        headers = {
            "content-type": "application/json"
        }
        response = self.session.post(url, data=data, verify=False, headers=headers)
        logger.info("xxxxxxxxxxxxxxxxxxxxxx")
        logger.info(response.text)
        try:
            response.raise_for_status()
            self.token = response.json().get('Oem', {}).get('Public', {}).get('X-Auth-Token')
            if self.token:
                # 将 token 添加到 session 的请求头中
                self.session.headers.update({"X-Auth-Token": self.token})
            else:
                logger.error("未获取到有效的 token")
        except requests.RequestException as e:
            logger.error(f"登录请求发生错误: {e}")
        except ValueError as e:
            logger.error(f"解析响应 JSON 数据时发生错误: {e}")

    def get(self, url, **kwargs):
        return self.request(url, "GET", **kwargs)

    def post(self, url, data=None, json=None, **kwargs):
        return self.request(url, "POST", data, json, **kwargs)

    def delete(self, url, **kwargs):
        return self.request(url, "DELETE", **kwargs)

    def patch(self, url, data=None, **kwargs):
        return self.request(url, "PATCH", data, **kwargs)

    def request(self, url, method, data=None, json=None, **kwargs):
        headers = kwargs.get("headers", {})
        params = kwargs.get("params")
        files = kwargs.get("files")
        cookies = kwargs.get("cookies")
        self.request_log(url, method, data, json, params, headers, files, cookies)
        if method == "GET":
            return self.session.get(url, headers=headers, params=params, verify=False, **kwargs)
        if method == "POST":
            return self.session.post(url, data=data, json=json, headers=headers, params=params, verify=False, **kwargs)
        if method == "DELETE":
            return self.session.delete(url, headers=headers, params=params, verify=False, **kwargs)
        if method == "PATCH":
            if json:
                data = complexjson.dumps(json)
                headers.setdefault("Content-Type", "application/json")
            return self.session.patch(url, data=data, headers=headers, params=params, verify=False, **kwargs)

    def request_log(self, url, method, data=None, json=None, params=None, headers=None, files=None, cookies=None, **kwargs):
        logger.info("接口请求地址 ==>> {}".format(url))
        logger.info("接口请求方式 ==>> {}".format(method))
        logger.info("接口请求头 ==>> {}".format(complexjson.dumps(headers, indent=4, ensure_ascii=False)))
        logger.info("接口请求 params 参数 ==>> {}".format(complexjson.dumps(params, indent=4, ensure_ascii=False)))
        logger.info("接口请求体 data 参数 ==>> {}".format(complexjson.dumps(data, indent=4, ensure_ascii=False)))
        logger.info("接口请求体 json 参数 ==>> {}".format(complexjson.dumps(json, indent=4, ensure_ascii=False)))
        logger.info("接口上传附件 files 参数 ==>> {}".format(files))
        logger.info("接口 cookies 参数 ==>> {}".format(complexjson.dumps(cookies, indent=4, ensure_ascii=False)))
    