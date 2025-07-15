import subprocess
from dotbot import Plugin
from dotbot.context import Context as Context
from functools import cached_property
from pathlib import Path
from shutil import which
from typing import Any, TypedDict


class Params(TypedDict):
    package: str
    preserve_installed: bool
    batch_mode: bool


class NixEnv(Plugin):

    supports_dry_run: bool = True

    def __init__(self, context: Context):
        super().__init__(context)
        self._directive: str = 'nixenv'

    def can_handle(self, directive: str) -> bool:
        return directive == self._directive

    def handle(
        self,
        directive: str,
        data: list[str] | dict[str, str | None] | str | bool | float,
    ) -> bool:
        if not self.can_handle(directive):
            raise ValueError(
                f'{self._directive} cannot handle directive {directive}'
            )
        success = True
        nix_executable = which('nix-env')
        if nix_executable is None:
            self._log.error('apt-get executable not found')
            return False
        if not isinstance(data, list) or not isinstance(data, dict):
            self._log.error(f'{self._directive} data should be list or dict')
            return False
        if not self._defaults['batch_mode']:
            for package in data:
                install_success = self._install(
                    nix_executable=nix_executable,
                    packages=[package],
                    preserve_installed=self._defaults['preserve_installed'],
                )
                success = success and install_success
        else:
            install_success = self._install(
                nix_executable=nix_executable,
                packages=data,
                preserve_installed=self._defaults['preserve_installed'],
            )
        return success

    def _install(
        self,
        nix_executable: str,
        packages: dict[str, str | None],
        *,
        preserve_installed: bool = True
    ) -> bool:
        self._log.info(f"Installing {', '.join(packages)} nix packages")
        args: list[str] = [nix_executable, '--install']
        if preserve_installed:
            args.append('--preserve_installed')
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
            'preserve_installed': True,
            'batch_mode': False,
        }
        return defaults | self._context.defaults().get(self._directive, {})
