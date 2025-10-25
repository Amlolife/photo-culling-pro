import PyInstaller.__main__
import os

def build_exe():
    # Get the directory of this script
    script_dir = os.path.dirname(os.path.abspath(__file__))

    # Paths
    app_py = os.path.join(script_dir, 'app.py')
    templates_dir = os.path.join(script_dir, 'templates')
    static_dir = os.path.join(script_dir, 'static')

    # PyInstaller command
    PyInstaller.__main__.run([
        '--onefile',  # Single executable
        '--windowed',  # No console window (since it's a web app, but we want it to run server)
        '--name=PhotoCullPro',
        '--add-data', f'{templates_dir};templates',
        '--add-data', f'{static_dir};static',
        app_py
    ])

if __name__ == '__main__':
    build_exe()
