import pytest
from utils.logging_config import logger


@pytest.mark.T21_P1876
@pytest.mark.smoke
def test_graphics_card(get_graphics_card, get_hdm_client):
    graphics_card = get_graphics_card
    bus_ids = graphics_card.api_get_gpu_bus_ids()
    logger.info(bus_ids)
    bdf_slot_dic = {}
    """for bus_id in bus_ids:
        gpu_slot_id = get_graphics_card.api_get_gpu_slot(bus_id)
        bdf_slot_dic[bus_id] = gpu_slot_id
    
    logger.info(f"GPU的BDF和slot对应关系：{bdf_slot_dic}")

    speed_and_bandwidth = get_graphics_card.api_get_gpu_speed_and_bandwidth(bus_ids[0])
    logger.info(speed_and_bandwidth)
    logger.info("------------------")
    logger.info(get_graphics_card.api_get_gpu_dmi(bus_ids))"""

    logger.info("------------------------------")
    logger.info(get_hdm_client.get_hdm_gpu_width(bus_ids[0]))

    