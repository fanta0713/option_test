import pytest
from utils.logging_config import logger


@pytest.mark.T21_P1876
@pytest.mark.smoke
def test_graphics_card(get_graphics_card, get_hdm_client, vendor_info):
    # STEP 1: 通过lspci -vvvxxxs获取显卡bus_ids
    logger.info("STEP 1: 通过lspci -vvvxxxs获取显卡bus_ids")
    bus_ids = get_graphics_card.api_get_gpu_bus_ids()
    logger.info(f"bus_ids: {bus_ids}")
    # STEP 2: 通过lspci -vvvxxxs获取显卡slot
    logger.info("STEP 2: 通过lspci -vvvxxxs获取显卡slot")
    for bus_id in bus_ids:
        slot = get_graphics_card.api_get_gpu_slot(bus_id)
        logger.info(f"bus_id: {bus_id}, slot: {slot}")
    # STEP 3: 通过lspci -vvvxxxs获取显卡速度和带宽，并检查带宽状态
    logger.info("STEP 3: 通过lspci -vvvxxxs获取显卡速度和带宽，并检查带宽状态")
    for bus_id in bus_ids:
        try:
            speed_and_bandwidth = get_graphics_card.api_get_gpu_speed_and_width(bus_id)
            logger.info(f"bus_id: {bus_id}, speed_and_bandwidth: {speed_and_bandwidth}")
        except Exception as e:
            logger.error(f"带宽异常 {bus_id}: {e}")
    # STEP 4: 通过dmidecode -t 9获取显卡bus_ids、slot和current_usage
    logger.info("STEP 4: 通过dmidecode -t 9获取显卡bus_ids、slot和current_usage")
    gpu_dmi = get_graphics_card.api_get_gpu_dmi(bus_ids)
    logger.info(f"gpu_dmi: {gpu_dmi}")
    # STEP 5: 比对lspci获取的gpu_bus_ids和dmidecode获取的bus_ids，并检查bus_ids和slot是否一致以及所有slot是否InUse
    logger.info("STEP 5: 比对lspci获取的gpu_bus_ids和dmidecode获取的bus_ids，并检查bus_ids和slot是否一致以及所有slot是否InUse")
    for gpu in gpu_dmi:
        bus_id = gpu["bus_id"]
        slot = gpu["slot"]
        current_usage = gpu.get("current_usage", "Unknown")
        
        # 检查 slot 是否一致
        expected_slot = get_graphics_card.api_get_gpu_slot(bus_id)
        assert slot == expected_slot, f"slot不一致: {slot} not equal to {expected_slot}"
        logger.info(f"slot一致: {slot} equal to {expected_slot}")
        
        # 检查 slot 是否为 InUse
        assert current_usage == "In Use", f"slot状态异常: {slot} is {current_usage}, expected 'In Use'"
        logger.info(f"slot状态正常: {slot} is {current_usage}")
    # STEP 6: 通过hdm获取显卡vendor是否符合预期
    logger.info("STEP 6: 通过hdm获取显卡vendor是否符合预期")
    for bus_id in bus_ids:
        vendor = get_hdm_client.get_hdm_gpu_vendor(bus_id)
        assert vendor == vendor_info, f"vendor不一致: {vendor} not equal to {vendor_info}"
        logger.info(f"vendor一致: {vendor} equal to {vendor_info}")

