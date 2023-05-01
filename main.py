import datetime
from controllers.MainController import MainController
from controllers.XbetController import XbetController
from misc.datetime_run_managment.ScriptRun import ScriptRun
from misc.datetime_run_managment.ScriptRunInterface import ScriptRunInterface
from misc.logger import logger
import asyncio

from misc.scheduler import scheduler


async def run_planned_process():
    try:
        script_run_manager: ScriptRunInterface = ScriptRun()
        scheduler.add_job(run_planned_process, 'date', run_date=script_run_manager.get_next_run())
        main_controller = MainController([XbetController()])
        await main_controller.parse_bookmakers()
    except Exception as e:
        logger.critical('Script dont parse sports' + str(e), exc_info=e)


def is_need_planned(func_name) -> bool:
    job_list = scheduler.get_jobs()
    for job in job_list:
        if job.name == func_name:
            return False
    return True


async def main():
    if is_need_planned('run_planned_process'):
        try:
            script_run_manager = ScriptRun()
            next_run = script_run_manager.get_next_run()
            if next_run is None or next_run + datetime.timedelta(minutes=30) < datetime.datetime.now():
                next_run: datetime = script_run_manager.set_last_run(datetime.datetime.now())
            scheduler.add_job(run_planned_process, 'date', run_date=next_run + datetime.timedelta(minutes=2))
        except Exception as e:
            logger.critical('Script did not run.\n' + str(e), exc_info=e)


if __name__ == '__main__':
    try:
        scheduler.add_job(main)
        scheduler.start()
        asyncio.get_event_loop().run_forever()
    except Exception as e:
        logger.critical('Script has been fallen!!!\n' + str(e), exc_info=e)
