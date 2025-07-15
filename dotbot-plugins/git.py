import subprocess
from copy import deepcopy
from dotbot import Plugin
from dotbot.context import Context as Context
from functools import cached_property
from pathlib import Path
from shutil import rmtree
from shutil import which
from typing import Any, TypedDict


class Params(TypedDict):
    destination: str
    repository: str
    depth: int | None
    force: bool
    create_parents: bool
    base_dir: str | None


class Git(Plugin):

    supports_dry_run: bool = True

    def __init__(self, context: Context):
        super().__init__(context)
        self._directive: str = 'git'

    def can_handle(self, directive: str) -> bool:
        return directive == self._directive

    def handle(
        self,
        directive: str,
        data: dict[str, str | Params | Any] | list[Any] | str | bool | float,
    ) -> bool:
        if not self.can_handle(directive):
            raise ValueError(
                f'{self._directive} cannot handle directive {directive}'
            )
        success = True
        git_executable = which('git')
        if git_executable is None:
            self._log.error('git executable not found')
            return False
        if not isinstance(data, dict):
            self._log.error(f'{self._directive} data should be dict')
            return False
        for destination, value in data.items():
            params = deepcopy(self._defaults)
            params['destination'] = destination
            if not value:
                self._log.error('Should pass params')
                return False
            if isinstance(value, str):
                params['repository'] = value
            elif isinstance(value, dict):
                for k in [
                    'destination',
                    'repository',
                    'depth',
                    'force',
                    'create_parents',
                    'base_dir',
                ]:
                    if k in value:
                        params[k] = value[k]
            else:
                success = False
                self._log.error(f'Invalid params to {destination}')
            clone_success = self._clone(git_executable, params)
            success = success and clone_success
        return success

    def _clone(self, git_executable: str, params: Params) -> bool:
        args: list[str] = [git_executable, 'clone']
        destination = self._base_dir.joinpath(
            Path(
                params['base_dir'] if params['base_dir'] else '.'
            ).expanduser()
        )
        destination = destination.joinpath(
            Path(params['destination']).expanduser(),
        ).resolve()
        if destination.exists():
            if params['force']:
                self._log.action(
                    f'Will delete {destination} before clone'
                )
                if not self._dry_run:
                    if destination.is_dir():
                        rmtree(destination)
                    else:
                        destination.unlink(missing_ok=True)
            else:
                self._log.info(f'{destination} already exists')
                return True
        if params['create_parents']:
            if not self._dry_run:
                destination.parent.mkdir(parents=True, exist_ok=True)
            else:
                self._log.action(f'Would create {destination.parent}')
        if params['depth'] is not None:
            args.append(f"--depth={params['depth']}")
        args.append(params['repository'])
        args.append(str(destination))
        if self._dry_run:
            self._log.action(f"Would run {' '.join(args)}")
            return True
        completed = subprocess.run(
            args=args,
            capture_output=True,
        )
        if completed.returncode == 0:
            self._log.info(f"Cloned {params['repository']} to {destination}")
            return True
        else:
            self._log.error(completed.stderr.decode())
            return False

    @cached_property
    def _dry_run(self) -> bool:
        return self._context.dry_run()

    @cached_property
    def _defaults(self) -> Params:
        defaults: Params = {
            'destination': '',
            'repository': '',
            'depth': None,
            'force': False,
            'create_parents': False,
            'base_dir': None,
        }
        return defaults | self._context.defaults().get(self._directive, {})

    @cached_property
    def _base_dir(self) -> Path:
        return Path(self._context.base_directory(True)).expanduser()
