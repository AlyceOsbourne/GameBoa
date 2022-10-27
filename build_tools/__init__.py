from pathlib import Path

import PyInstaller.__main__ as installer


def build():

    installer.run(
        [
            '__main__.py',
            '--name=GameBoa',
            f'--icon={Path(__file__).parent.parent / "project" / "resources" / "gui" / "icons" / "icon.ico"}',
            f'--distpath={Path(__file__).parent.parent / "dist" / "windows"}',
            # '--windowed',
            '--onefile',
            '--clean',
            '--add-data=project/resources;resources',
        ]
    )




if __name__ == '__main__':
    build()

