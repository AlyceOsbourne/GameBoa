import PyInstaller.__main__ as installer
from __paths__ import ico_path, src_path, resources, run_path, spec_path, dist_path, work_path
from __metadata__ import __version__

folders_to_include = ["src", "resources"]


def build():

    installer.run(
        [
            run_path.as_posix(),

            f'--name=GameBoa',
            f'--icon={ico_path}',
            f'--specpath={str(spec_path)}',
            f'--distpath={str(dist_path)}',
            f'--workpath={str(work_path)}',
            # '--log-level=DEBUG',
            # '--debug=all',
            '--clean',
            # '--noconfirm',
            '--onefile',
            # '--windowed',
            f'--add-data={src_path.as_posix()};src',
            f'--add-data={resources.as_posix()};resources',
            *[
                f'--add-data={path.as_posix()};{path.parent.name}'
                for path in resources.rglob("*") if path.is_file()
            ]
        ]
    )




if __name__ == '__main__':
    build()

