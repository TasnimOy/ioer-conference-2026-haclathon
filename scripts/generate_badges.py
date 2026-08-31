import anybadge
from pathlib import Path

BADGE_DIR = Path("_static/badges")
BADGE_DIR.mkdir(parents=True, exist_ok=True)

# 1. Chapter Type Badges
anybadge.Badge(label='Type', value='Interactive Code', default_color='blue').write_badge(str(BADGE_DIR / 'type_interactive.svg'), overwrite=True)
anybadge.Badge(label='Type', value='Workflow Tutorial', default_color='darkgreen').write_badge(str(BADGE_DIR / 'type_tutorial.svg'), overwrite=True)
anybadge.Badge(label='Type', value='Data Story', default_color='orange').write_badge(str(BADGE_DIR / 'type_story.svg'), overwrite=True)

# 2. Execution Badges
anybadge.Badge(label='Colab', value='Tested', default_color='yellow').write_badge(str(BADGE_DIR / 'colab_tested.svg'), overwrite=True)
anybadge.Badge(label='Jupyter4NFDI', value='Ready', default_color='darkorange').write_badge(str(BADGE_DIR / 'nfdi_ready.svg'), overwrite=True)
anybadge.Badge(label='Software', value='QGIS 3.x', default_color='green').write_badge(str(BADGE_DIR / 'qgis_required.svg'), overwrite=True)