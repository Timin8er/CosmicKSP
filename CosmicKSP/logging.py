"""logger for the Cosmic KSP project"""

import os
from pyqt_data_framework.core.logging import get_logger

logger = get_logger(name='CosmicKSP',
    dir=os.path.expanduser(os.path.join('~', 'Documents', 'CosmicKSP')))
