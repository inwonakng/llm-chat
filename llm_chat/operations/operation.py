from dataclasses import dataclass


@dataclass
class Operation:
    name: str
    func: callable
    help_text: str

    def __call__(self, **kwargs):
        return self.func(**kwargs)
