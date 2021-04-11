import shutil
import modules.analytics
from precipy.main import render_file

render_file('config.json', [modules.analytics], storages=[])

# Copy file to top level for gh-pages deployment
shutil.copy('precipy/acs.html', 'index.html')
