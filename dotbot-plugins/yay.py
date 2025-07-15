import subprocess
from dotbot import Plugin
from dotbot.context import Context as Context
from functools import cached_property
from pathlib import Path
from shutil import which
from typing import Any, TypedDict


class Params(TypedDict):
    needed: bool
    batch_mode: bool


class Yay(Plugin):

    supports_dry_run: bool = True

    def __init__(self, context: Context):
        super().__init__(context)
        self._directive: str = 'yay'

    def can_handle(self, directive: str) -> bool:
        return directive == self._directive

    def handle(
        self,
        directive: str,
        data: list[str] | dict[str, Any] | str | bool | float,
    ) -> bool:
        if not self.can_handle(directive):
            raise ValueError(
                f'{self._directive} cannot handle directive {directive}'
            )
        success = True
        yay_executable = which('yay')
        if yay_executable is None:
            self._log.error('yay executable not found')
            return False
        if not isinstance(data, list):
            self._log.error(f'{self._directive} data should be list')
            return False
        if not self._defaults['batch_mode']:
            for package in data:
                install_success = self._install(
                    yay_executable=yay_executable,
                    packages=[package],
                    needed=self._defaults['needed'],
                )
                success = success and install_success
        else:
            install_success = self._install(
                yay_executable=yay_executable,
                packages=data,
                needed=self._defaults['needed'],
            )
        return success

    def _install(
        self,
        yay_executable: str,
        packages: list[str],
        *,
        needed: bool = True
    ) -> bool:
        self._log.info(f"Installing {', '.join(packages)} yay packages")
        args: list[str] = [yay_executable, '--sync', '--noconfirm']
        if needed:
            args.append('--needed')
        args.extend(packages)
        if self._dry_run:
            self._log.action(f"Would run {' '.join(args)}")
            return True
        completed = subprocess.run(
            args=args,
            capture_output=True,
        )
        if completed.returncode == 0:
            self._log.info(f"Packages {', '.join(packages)} installed")
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
            'needed': True,
            'batch_mode': False,
        }
        return defaults | self._context.defaults().get(self._directive, {})
