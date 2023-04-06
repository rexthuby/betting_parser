import asyncio

from misc.Logger import Logger



async def main():
    pass



if __name__ == '__main__':
    try:
        asyncio.run(main())
    except Exception as e:
        Logger.get_logger().critical('Script has been fallen!!!' + '\n' + str(e))