from datetime import datetime


class ScriptRunInterface():
    def get_last_run(self) -> datetime | None:
        raise NotImplementedError

    def get_next_run(self) -> datetime | None:
        raise NotImplementedError

    def set_last_run(cls, date: datetime):
        raise NotImplementedError