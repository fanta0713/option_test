from utils.logging_config import logger


def test_graphics_card(get_graphics_card):
    graphics_card = get_graphics_card
    bus_ids = graphics_card.get_gpu_bus_ids()
    print(bus_ids)