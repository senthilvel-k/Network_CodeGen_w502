from distutils.core import setup
import py2exe,glob

#DATA=[('C:\\Python27/Lib/site-packages/PyQt4/plugins/imageformats/qgif4.dll')]
DATA=[('html',glob.glob(r'.\html\*.*')),\
        ('data',glob.glob(r'.\data\*.*')),\
       ('js',glob.glob(r'.\js\*.*')),\
       ('style',glob.glob(r'.\style\*.*')),\
       (r'.\batman.ico') ]


#setup(console=['gen_xls.py','vnim_app_signals_c_file.py','vnim_app_bcan_fcan_signal_h_final.py','bcan_cfg.py','bcan_il_par_c.py','bcan_il_par_h.py','fcan_cfg.py','fcan_il_par_c_file.py','fcan_il_par_h.py'])
setup(windows = [{'script':'CoGeNT.pyw','icon_resources': [(004,'batman.ico')]}],options = {'py2exe': {"skip_archive":True, 'optimize': 1}}, data_files = DATA)

#copy binder.js file
#copy binder.js file

import shutil
shutil.copy2(r'.\binder.js', r'.\htmlPy\binder.js')
print '---binder.js copied check in htmlPy folder ----'
